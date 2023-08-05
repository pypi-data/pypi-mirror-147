# -*- coding: utf-8 -*-
"""
    :author: Dabai
    :url: samuelbaizg.github.io
    :copyright: © 2018 Dabai <zhgbai@163.com>
    :license: MIT, see LICENSE for more details.
"""
import logging
import sys
import time

import sqlalchemy

from btoolkit import xfunc, xtype, error, xglobal
from btoolkit.asynch.message_queue import Message, Conduit
from btoolkit.database import rdb_alchemy, rdb_table


class SqlConduit(Conduit):
    """
    SqlAlchemy conduit implements.
    """

    logger = logging.getLogger(__name__)

    def __init__(self, conduit_name, asynch, message_max_length=512 * 1024, message_proc_num=10,
                 process_pool=False, pull_interval=1, pull_max_attempts=3,
                 **kwargs):
        """
        :param int message_max_length: the unit is byte
        :param int message_proc_num:  the worker quantity to process message in xfunc.
        :param bool process_pool: using ProcessPoolExecutor if True else ThreadPoolExecutor.
        :param float pull_interval: the message pull interval and the unit is seconds
        :param int pull_max_attempts:
        """
        super(SqlConduit, self).__init__(conduit_name, asynch, message_max_length=message_max_length, **kwargs)
        self._message_t = MessageT(conduit_name)
        self._pull_max_attempts = pull_max_attempts
        self._pull_interval = pull_interval
        self._message_proc_num = message_proc_num
        self._process_pool = process_pool

        self.__stopped = True
        self.__lock = xfunc.create_lock(False)
        self.__message_proc = None

    def send(self, message):
        if message.id is None:
            message.id = xtype.uuid_short()
        return self._message_t.send(message)

    def start_consumer(self):

        def process(msg):
            try:
                self.process(msg)
                self._message_t.complete(msg.id)
            except Exception as e1:
                err = "failed to process message '%i' due to %s." % (msg.id, e1)
                self._message_t.error(msg.id, "%s: %s" % (err, error.format_exc_info(sys.exc_info())))

        try:
            self.__lock.acquire()
            if not self.__stopped:
                self.logger.warning("The consumer of the conduit '%s' was already started." % self.name)
                return

            self.__stopped = False
            self.__message_proc = xfunc.NoWaitCall(max_workers=self._message_proc_num, process=self._process_pool)
            self._message_t.create_table(self.name)
            while not self.__stopped:
                try:
                    time.sleep(self._pull_interval)
                    messages = self._message_t.next(self._message_proc_num, self._pull_max_attempts)
                    for message in messages:
                        self._message_proc.submit(process, None, None, message)
                except Exception as e:
                    self.logger.exception("failed to run SqlConduit.start_consumer due to %s." % e)
        finally:
            self.__lock.release()

    def shutdown_consumer(self):
        self.__stopped = True
        if self.__message_proc is not None:
            self.__message_proc.shutdown(wait=True)
            self.__message_proc = None
        self.logger.info("succeed to stop SqlConduit %s." % self.name)


def get_message_db_bind_key():
    return xglobal.get_app_info().get_flask_config("ASYNC_SQLALCHEMY_BIND_KEY")


class MessageT(rdb_table.TableSplitMixin, rdb_table.TableBase):
    __table_name__ = "async_message_t"
    __table_dec__ = rdb_alchemy.table(__table_name__,
                                      rdb_alchemy.metadata(get_message_db_bind_key()),
                                      rdb_alchemy.column('msg_id', sqlalchemy.String(10), primary_key=True,
                                                         autoincrement=False,
                                                         comment="主键"),
                                      rdb_alchemy.column('msg_type', sqlalchemy.String(20), comment="消息类型"),
                                      rdb_alchemy.column('payload', sqlalchemy.Text, nullable=False, comment="消息内容"),
                                      rdb_alchemy.column('pull_flag', sqlalchemy.SmallInteger, nullable=False,
                                                         default=0, comment="拉取标志 0-未拉取 1-已拉取"),
                                      rdb_alchemy.column('pull_time', sqlalchemy.DateTime, comment="拉取时间"),
                                      rdb_alchemy.column('process_flag', sqlalchemy.SmallInteger, nullable=False,
                                                         default=0, comment="处理标识 0-未处理 1-处理成功 2-处理失败"),
                                      rdb_alchemy.column('process_time', sqlalchemy.DateTime, comment="处理时间"),
                                      rdb_alchemy.column('process_remark', sqlalchemy.String(4000), comment="处理备注"),
                                      rdb_alchemy.column('pull_attempts', sqlalchemy.Integer, nullable=False, default=3,
                                                         comment="拉取次数"),
                                      rdb_alchemy.column('locked_by', sqlalchemy.String(10), comment="加锁对象"),
                                      created_at=False, created_by=False, last_updated_at=False, last_updated_by=False,
                                      tenant_id=False,
                                      info={'bind_key': get_message_db_bind_key()}
                                      )

    def __init__(self, conduit_name):
        """
        :param str conduit_name: conduit name
        """
        rdb_table.TableBase.__init__(self)
        rdb_table.TableSplitMixin.__init__(self)
        self._conduit_name = conduit_name
        self._table = self.__table_dec__

    @property
    def conduit_name(self):
        return self._conduit_name

    def send(self, message):
        """
        Create a message.
        :param Message message: message
        :return:
        """
        stmt = self.insert(self._conduit_name)
        row = xtype.ValueObj()
        row.msg_id = message.id
        row.msg_type = message.type
        row.payload = xtype.obj_to_json(message.to_dict())
        stmt = stmt.values(**row)
        result = rdb_alchemy.execute_stmt(self.engine, stmt)
        return result.rowcount == 1

    def next(self, limit, max_attempts, message_type=None):
        """
        Return next message
        :param int limit: the quantity to pull.
        :param int max_attempts: the max pull attempts.
        :param str message_type: message type
        :return: None if no message is found.
        """
        locked_by = xtype.uuid_short()
        stmt = self.update(self._conduit_name)

        stmt = stmt.values(pull_flag=1, pull_time=xtype.tz_utcnow(), process_flag=0,
                           process_time=rdb_alchemy.bindparam('pt', null=True),
                           process_remark=rdb_alchemy.bindparam('pr', null=True), locked_by=locked_by)
        stmt = stmt.where(self.column.locked_by == None)
        stmt = stmt.where(self.column.pull_flag == 0)
        stmt = stmt.where(self.column.pull_attempts <= max_attempts)
        if message_type is not None:
            stmt = stmt.where(self.column.msg_type == message_type)
        sql = rdb_alchemy.literal(stmt, self.engine)
        sql = "%s LIMIT %i" % (sql, limit)
        stmt = rdb_alchemy.text(sql)
        rdb_alchemy.execute_stmt(stmt)
        stmt = self.select(self._conduit_name)
        stmt = stmt.column(self.column.payload)
        stmt = stmt.where(self.column.locked_by == locked_by)
        stmt = stmt.limit(limit)
        rows = rdb_alchemy.execute_stmt(self.engine, stmt).fetchall()
        messages = []
        for row in rows:
            payload = row[self.column.payload]
            messages.append(Message.from_json(payload))
        return messages

    def complete(self, msg_id):
        """
        Mark a message as complete.
        :param long msg_id: message id
        """
        stmt = self.delete(self._conduit_name)
        stmt = stmt.where(self.column.msg_id == msg_id)
        rdb_alchemy.execute_stmt(stmt)
        return True

    def error(self, msg_id, error_msg=None):
        """
        Note an error processing a job, and return it to the queue.
        :param long msg_id: message id
        :param str error_msg: error message
        """
        stmt = self.update(self._conduit_name, preserve_parameter_order=True)
        stmt = stmt.values([(self.column.process_flag, 0), (self.column.process_time, xtype.tz_utcnow()),
                            (self.column.process_remark, error_msg), (self.column.locked_by, None),
                            (self.column.pull_attempts, self.column.pull_attempts + 1)])
        stmt = stmt.where(self.column.msg_id == msg_id)
        rdb_alchemy.execute_stmt(self.engine, stmt)
        return True

    def get(self, msg_id):
        """
        Get message by msg_id
        :param long msg_id: message id
        :return: instance of Message
        """
        stmt = self.select(self._conduit_name)
        stmt = stmt.column(self.column.payload)
        stmt = stmt.where(self.column.msg_id == msg_id)
        result = rdb_alchemy.execute_stmt(self.engine, stmt).first()
        return Message.from_json(result[self.column.payload]) if result is not None else None

    def retry(self, msg_id):
        """
        Release a message back to the pool. The attempts counter is set to zero.
        :param long msg_id: message id
        """
        stmt = self.update(self._conduit_name, preserve_parameter_order=True)
        stmt = stmt.values(pull_flag=0, pull_time=None, process_flag=0, process_time=None, process_remark=None,
                           pull_attempts=0)
        stmt = stmt.where(self.column.msg_id == msg_id)
        rdb_alchemy.execute_stmt(self.engine, stmt)
        return True

# -*- coding: utf-8 -*-
"""
    :author: Dabai
    :url: samuelbaizg.github.io
    :copyright: © 2018 Dabai <zhgbai@163.com>
    :license: MIT, see LICENSE for more details.
"""
import logging

from btoolkit import error
from btoolkit import xfunc
from btoolkit import xtype

"""
    Async utilities
"""


class Asynch(object):
    SECTION_CONDUIT = "conduit"
    SECTION_PROCESSOR = "processor"

    def __init__(self, config, process_pool=False, **kwargs):
        """
        This method must be called to init conduit and processor before using other asyn methods.
         :param dict config: sample is like,
         {
             "conduit": {
                     "testConduit1": {
                            "clazz": "chassis.asyn.SqlConduit",
                            "arguments": {
                                "message_max_length": 524288,
                                "message_proc_num": 10,
                                "process_pool": false,
                                "pull_max_attempts": 3,
                                "pull_interval": 1   # unit is second
                            }
                     }
              },
              "processor": {
                    "message_type_1": {
                        "conduit_name": "testdbConduit",
                        "clazz": "test.chassis.test_asyn.Processor1"
                    }
              }

        }
        :param bool process_pool: using ProcessPoolExecutor if True else ThreadPoolExecutor.
        :param dict kwargs:
            'engine' must be passed if this config includes SqlConduit.
        :return: void
        """
        self._conduits = {}
        self._processors = {}
        self._process_pool = process_pool

        def parse_conduit(c_cfg):
            for name, value in c_cfg.items():
                if name in self._conduits:
                    raise error.InvalidError("conduit %s" % name, " it has been configured.")
                else:
                    vo = xtype.ValueObj()
                    for k, v in value.items():
                        vo[k] = v
                    vo.clazz = xfunc.import_module(vo['clazz'])
                    if vo.clazz is None:
                        raise error.NoFoundError("Conduit", value['clazz'])
                    dicts = xtype.dict_merge(vo.arguments, kwargs) if kwargs is not None else vo.arguments
                    vo.instance = vo.clazz(name, self, **dicts)
                    self._conduits[name] = vo

        def parse_processor(p_cfg):
            for msg_type, value in p_cfg.items():
                if msg_type in self._processors:
                    raise error.InvalidError("Processor %s" % msg_type, " it has been configured.")
                else:
                    vo = xtype.ValueObj()
                    for k, v in value.items():
                        vo[k] = v
                    vo.clazz = xfunc.import_module(vo['clazz'])
                    if vo.clazz is None:
                        raise error.NoFoundError("Processor", value['clazz'])
                    conduit_name = vo['conduit_name']
                    if conduit_name not in self._conduits:
                        raise error.NoFoundError("Conduit with the name", conduit_name)
                    conduit = self._conduits[conduit_name]
                    vo.conduit = conduit
                    vo.instance = vo.clazz(conduit.instance)
                    self._processors[msg_type] = vo

        conduit_cfg = config[self.SECTION_CONDUIT]
        processor_cfg = config[self.SECTION_PROCESSOR]
        parse_conduit(conduit_cfg)
        parse_processor(processor_cfg)
        self.__no_wait_call = xfunc.NoWaitCall(max_workers=len(self._conduits), process=self._process_pool)

    def get_processor(self, message_type):
        """
        Return message processor
        :param str message_type:
        """
        if not message_type in self._processors:
            raise error.NoFoundError('message_type', message_type, 'processor configuration.')
        return self._processors[message_type].instance

    def get_conduit(self, conduit_name):
        """
        Return conduit instance
        :param str conduit_name: conduit name
        """
        if not conduit_name in self._conduits:
            raise error.NoFoundError('conduit_name', conduit_name, 'conduit configuration.')
        return self._conduits[conduit_name].instance

    def send_message(self, message_type, content):
        """
        Send asynchronous message
        :param str message_type: message type
        :param object content: the object can be converted to json format.
        """
        processor = self.get_processor(message_type)
        msg = Message(message_type)
        msg.id = xtype.uuid_short()
        msg.content = content
        return processor.conduit.produce(msg)

    def start_conduit_consumer(self, conduit_name):
        """
        Start consumer for listening the specific conduit.
        :param conduit_name:
        :return:
        """
        conduit = self.get_conduit(conduit_name)
        if self.__no_wait_call is None:
            self.__no_wait_call = xfunc.NoWaitCall(max_workers=len(self._conduits), process=self._process_pool)
        self.__no_wait_call.submit(conduit.start_consumer, None, None)

    def shutdown_conduit_consumers(self):
        """
        Shutdown all conduit consumers.
        :return:
        """
        for key in self._conduits.keys():
            conduit = self.get_conduit(key)
            conduit.shutdown_consumer()
        self.__no_wait_call.shutdown(wait=True)
        self.__no_wait_call = None


class Message(xtype.JsonMixin):
    """
        The message object that is sent to the conduit
    """

    def __init__(self, message_type):
        self.__type = message_type
        self.__content = None
        self.__id = None  # this property is set in Conduit

    @staticmethod
    def from_json(cls, json):
        """
        Construct Message object from json str.
        :param Message cls:
        :param str json:
        :return: instance of Message
        """
        obj = xtype.json_to_object(json)
        message = cls(obj['message_type'])
        message.content = obj['content']
        message.id = obj['id']
        return message

    @property
    def type(self):
        return self.__type

    @property
    def content(self):
        return self.__content

    @property
    def id(self):
        return self.__id

    @content.setter
    def content(self, content):
        """
            :param json object content: object can be jsoned using json.dumps(obj, ensure_ascii=False, cls=ExtJsonEncoder)
        """
        self.__content = content

    @id.setter
    def id(self, id1):
        self.__id = id1

    def to_dict(self):
        dic = {'type': self.__type, 'content': self.__content, 'id': self.__id}
        return dic


class Processor(object):
    """
    The message processor must extend this class
    """

    def __init__(self, conduit):
        """
        :param conduit: instance of Conduit
        """
        self._conduit = conduit

    @property
    def conduit(self):
        return self._conduit

    def process(self, message):
        """
            Process the message
            :param conduit.Message message:
            :rtype void
        """
        raise NotImplementedError("Processor.process")


class Conduit(object):

    def __init__(self, conduit_name, asynch, message_max_length=512 * 1024, **kwargs):
        """
        :param conduit_name: Conduit name
        :param asynch: Instance of Asynch
        :param int message_max_length:  max message length
        """
        self._conduit_name = conduit_name
        self._asynch = asynch
        self._message_max_length = message_max_length
        self._kwargs = kwargs

    @property
    def name(self):
        return self._conduit_name

    def produce(self, message):
        """
        Produce the message to this conduit
        :param conduit.Message message:
        :return bool: True if success else False
        """
        length = len(message.content)
        if length > self._message_max_length:
            raise error.LengthError(self._conduit_name, 0, self._message_max_length)
        return self.send(message)

    def process(self, message):
        """
        process message
        :param Conduit.Message message:
        """
        processor = self._asynch.get_processor(message.type)
        return processor.process(message)

    def send(self, message):
        """
        Send message to this conduit
        :param conduit.Message message:
        :return bool: True if success else False
        """
        raise NotImplementedError("Conduit.send")

    def start_consumer(self):
        """
        Start the consumer of this conduit.
        :return:
        """
        raise NotImplementedError("Conduit.start_consumer")

    def shutdown_consumer(self):
        """
        Shutdown the consumer for this conduit.
        :return:
        """
        raise NotImplementedError("Conduit.shutdown_consumer")

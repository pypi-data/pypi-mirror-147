# -*- coding: utf-8 -*-
"""
    :author: Dabai
    :url: samuelbaizg.github.io
    :copyright: © 2018 Dabai <zhgbai@163.com>
    :license: MIT, see LICENSE for more details.
"""

from __future__ import with_statement

import logging
from logging.config import fileConfig

import click
from alembic import context as alembic_context
from alembic.operations import ops

from btoolkit.database import rdb_alchemy

rdb_alchemy.TableBase.sub_classes()

# this is the Alembic Config object, which provides access to the values within the .ini file in use.
config = alembic_context.config

# Interpret the config file for Python logging.
fileConfig(config.config_file_name)

logger = logging.getLogger('alembic.env')

context = click.get_current_context().obj

bind_names = [key for key in context.get_config_holder().get_flask_config("SQLALCHEMY_BINDS").keys()]


def include_object(object, name, type_, reflected, compare_to):
    """Don’t generate any DROP TABLE directives with autogenerate
        and don’t emit CREATE TABLE statements for Views."""
    if type_ == "table" and reflected and compare_to is None:
        return False
    else:
        return not object.info.get('is_view', False)


def process_revision_directives(context, revision, directives):
    """
    this callback is used to prevent an auto-migration from being generated
    when there are no changes to the schema
    reference: http://alembic.zzzcomputing.com/en/latest/cookbook.html
    """

    script = directives[0]

    # process both "def upgrade()", "def downgrade()"
    for directive in (script.upgrade_ops, script.downgrade_ops):

        # make a set of tables that are being dropped within the migration function
        tables_dropped = set()
        for op in directive.ops:
            if isinstance(op, ops.DropTableOp):
                tables_dropped.add((op.table_name, op.schema))

        # now rewrite the list of "ops" such that DropIndexOp is removed for those tables.
        directive.ops = list(
            _filter_drop_indexes(directive.ops, tables_dropped)
        )


def _filter_drop_indexes(directives, tables_dropped):
    """given a set of (tablename, schemaname) to be dropped, filter
     out DropIndexOp from the list of directives and yield the result."""

    for directive in directives:
        # ModifyTableOps is a container of ALTER TABLE types of commands.
        if isinstance(directive, ops.ModifyTableOps) and \
                (directive.table_name, directive.schema) in tables_dropped:
            directive.ops = list(
                _filter_drop_indexes(directive.ops, tables_dropped)
            )

            # if we emptied out the directives, then skip the container altogether.
            if not directive.ops:
                continue
        elif isinstance(directive, ops.DropIndexOp) and \
                (directive.table_name, directive.schema) in tables_dropped:
            # we found a target DropIndexOp.   keep looping
            continue

        # otherwise if not filtered, yield out the directive
        yield directive


def run_migration(bind_name):
    """
    Run migration for a schema.
    :param bind_name: Key of SQLALCHEMY_BINDS
    :return:
    """
    if bind_name is None or len(str(bind_name).strip()) == 0:
        logger.error("bind name is empty.")
        return

    logger.info("Migrating database %s" % (bind_name or '<default>'))
    alembic_context.configure(
        connection=rdb_alchemy.get_sql_engine(bind_name).connect(),
        upgrade_token="%s_upgrades" % bind_name,
        downgrade_token="%s_downgrades" % bind_name,
        target_metadata=rdb_alchemy.metadata(bind_name),
        process_revision_directives=process_revision_directives,
        include_object=include_object
    )
    with alembic_context.begin_transaction():
        alembic_context.run_migrations(engine_name=bind_name)


def run_migrations():
    for bind_name in bind_names:
        run_migration(bind_name)


run_migrations()

# -*- coding: utf-8 -*-
"""
    :author: Dabai
    :url: samuelbaizg.github.io
    :copyright: © 2018 Dabai <zhgbai@163.com>
    :license: MIT, see LICENSE for more details.
"""

EXTENSION_SQL_ALCHEMY = 'sqlAlchemy'
EXTENSION_AP_SCHEDULER = 'apScheduler'

APP_INFO = 'appInfo'


class _GlobalVar(object):
    """Global variables holder."""

    def __init__(self):
        self.__g_object = dict()

    def set_object(self, name, obj):
        """Set global object."""
        if name in self.__g_object:
            raise ValueError('%s is already in GlobalVar.' % name)
        self.__g_object[name] = obj

    def get_object(self, name):
        """Get global object."""
        return self.__g_object.get(name)


_global_var = _GlobalVar()


def set_extension(name, obj):
    """Set global object."""
    _global_var.set_object(name, obj)


def get_extension(name):
    """Get global object."""
    return _global_var.get_object(name)


def set_app_info(app_info):
    """Set app info"""
    _global_var.set_object(APP_INFO, app_info)


def get_app_info():
    """Return current app info."""
    return _global_var.get_object(APP_INFO)


def get_sql_alchemy():
    """Get SqlAlchemy object."""
    return get_extension(EXTENSION_SQL_ALCHEMY)


def set_sql_alchemy(sql_alchemy):
    """Set SqlAlchemy object."""
    set_extension(EXTENSION_SQL_ALCHEMY, sql_alchemy)


def get_ap_scheduler():
    """Get ApScheduler object."""
    return get_extension(EXTENSION_AP_SCHEDULER)


def set_ap_scheduler(ap_scheduler):
    """Set ApScheduler object."""
    set_extension(EXTENSION_AP_SCHEDULER, ap_scheduler)

# -*- coding: utf-8 -*-
"""
    :author: Dabai
    :url: samuelbaizg.github.io
    :copyright: © 2018 Dabai <zhgbai@163.com>
    :license: MIT, see LICENSE for more details.
"""
from btoolkit import xtype


class ConstantBase(object):
    """Base Constant definition."""

    __hide__ = list()  # the constant names that are not used in UI,should be override by sub-class.

    @staticmethod
    def sub_classes():
        scs = []
        for sc in ConstantBase.__subclasses__():
            scs.append(sc)
        return scs

    @classmethod
    def all_consts(cls, qualifier=False, for_ui=False):
        """Return all constants."""
        consts = dict()
        for k, v in cls.__dict__.items():
            if k.startswith('_') or isinstance(v, (classmethod, staticmethod)):
                continue
            if for_ui and k in cls.__hide__:
                continue
            if qualifier:
                k = '{}.{}'.format(cls.__name__, k)
            consts[k] = v
        return consts


class CommonConstant(ConstantBase):

    YES = 'Y'
    NO = 'N'

    DEFAULT = 'default'
    LOGGING = 'logging'
    FLASK = 'flask'
    GUNICORN = 'gunicorn'

    LOG_TYPE_ADD = "A"
    LOG_TYPE_UPDATE = "U"
    LOG_TYPE_DELETE = "D"


def fetch_all_consts(qualifier=False, for_ui=False):
    """fetch all constants.
    :param bool qualifier: attaching the complete class name to CONSTANT NAME or not.
    :param bool for_ui: True just fetch constants for UI.
    """
    constants = dict()
    for clazz in ConstantBase.sub_classes():
        consts = clazz.all_consts(qualifier=qualifier, for_ui=for_ui)
        xtype.dict_merge(constants, consts)
    return constants

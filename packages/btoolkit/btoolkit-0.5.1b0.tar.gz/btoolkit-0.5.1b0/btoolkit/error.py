# -*- coding: utf-8 -*-
"""
    :author: Dabai
    :url: samuelbaizg.github.io
    :copyright: © 2018 Dabai <zhgbai@163.com>
    :license: MIT, see LICENSE for more details.
"""

import re
import traceback
import types

"""
Error Code Range:
error: [A-Z]01 ~ [A-Z]99
success: A00
"""


class BaseError(Exception):
    def __init__(self, **kwargs):
        self.__kwargs = kwargs

    @staticmethod
    def code():
        """To be implemented by sub-class"""
        raise NotImplementedError("Error.code is not implemented by sub-class.")

    @staticmethod
    def template():
        raise NotImplementedError("Error.template is not implemented by sub-class.")

    @property
    def message(self):
        message = self.template()

        if message is not None and (self.__kwargs is not None and len(self.__kwargs) > 0):
            for key, value in self.__kwargs.items():
                message = message.replace("{{%s}}" % key, str(value))
        return message

    @property
    def arguments(self):
        return self.__kwargs

    def get_argument(self, key):
        return self.arguments[key]

    @property
    def data(self):
        return self.arguments['data'] if self.arguments is not None and 'data' in self.arguments else None

    @property
    def alias(self):
        return error_alias(self)

    def __str__(self):
        return self.message

    @staticmethod
    def sub_classes():
        scs = []
        for sc in BaseError.__subclasses__():
            scs.append(sc)
        return scs


def error_alias(error_class_or_inst):
    """Return alias of exception."""
    e_alias = error_class_or_inst.__class__.__name__ if isinstance(error_class_or_inst,
                                                                   BaseException) else error_class_or_inst.__name__
    e_alias = re.sub('[A-Z]', lambda x: " " + x.group(0), e_alias)
    return e_alias[1:]


def get_error(code):
    for err in BaseError.sub_classes():
        if err.code == code:
            return err
    return None


class InternalError(BaseError):
    """
        Error is to define the error.
    """

    def __init__(self, message, data=None):
        super(InternalError, self).__init__(message=message, data=data)

    @staticmethod
    def code():
        return 'A01'

    @staticmethod
    def template():
        return "{{message}}"


class NoDoError(BaseError):
    def __init__(self, action, what, data=None):
        super(NoDoError, self).__init__(action=action, what=what, data=data)

    @staticmethod
    def code():
        return 'A02'

    @staticmethod
    def template():
        return "No support to {{action}} {{what}}."


class NoFoundError(BaseError):
    def __init__(self, it, something, where=None, data=None):
        super(NoFoundError, self).__init__(it=str(it),
                                           something=str(something), where=str(where), data=data)

    @staticmethod
    def code():
        return 'A03'

    @staticmethod
    def template():
        return "{{it}} {{something}} is not found in {{where}}."


class ReferredError(BaseError):
    def __init__(self, it, referred, data=None):
        super(ReferredError, self).__init__(it=it, referred=referred, data=data)

    @staticmethod
    def code():
        return 'A04'

    @staticmethod
    def template():
        return "{{it}} is referred by {{referred}}."


class InvalidError(BaseError):
    def __init__(self, something, why=None, data=None):
        if why is not None:
            super(InvalidError, self).__init__(
                something=str(something), why=str(why), data=data)
        else:
            super(InvalidError, self).__init__(
                something=str(something), data=data)

    @staticmethod
    def code():
        return 'A05'

    @staticmethod
    def template():
        return "{{something}} is not valid because {{why}}."


class ClassCastError(BaseError):
    def __init__(self, clazz, baseclazz, data=None):
        super(ClassCastError, self).__init__(clazz=clazz,
                                             baseClazz=baseclazz, data=data)

    @staticmethod
    def code():
        return 'A06'

    @staticmethod
    def template():
        return "{{clazz}} is not the sub-class of {{baseClazz}}."


class RequiredError(BaseError):
    def __init__(self, label, data=None):
        super(RequiredError, self).__init__(label=label, data=data)

    @staticmethod
    def code():
        return 'A07'

    @staticmethod
    def template():
        return "{{label}} is required."


class ChoiceError(BaseError):
    def __init__(self, label, choices, data=None):
        super(ChoiceError, self).__init__(label=label,
                                          choices=",".join(map(str, choices)), data=data)

    @staticmethod
    def code():
        return 'A08'

    @staticmethod
    def template():
        return "{{label}}'s value must be one of {{choices}}."


class LengthError(BaseError):
    def __init__(self, label, minlength, maxlength, data=None):
        super(LengthError, self).__init__(label=label, minlength=minlength, maxlength=maxlength, data=data)

    @staticmethod
    def code():
        return 'A09'

    @staticmethod
    def template():
        return "{{label}}'s length must between {{minlength}} and {{maxlength}}."


class RangeError(BaseError):
    def __init__(self, label, mininum, maximum, data=None):
        super(RangeError, self).__init__(
            label=label, mininum=mininum, maximum=maximum, data=data)

    @staticmethod
    def code():
        return 'A10'

    @staticmethod
    def template():
        return "{{label}}'s value 's value {{mininum}} and {{maximum}}."


class CompareError(BaseError):
    def __init__(self, label, operator, limitlabel, limit, data=None):
        super(CompareError, self).__init__(
            label=label, operator=operator, limit=limit, limitlabel=limitlabel,
            data=data)

    @staticmethod
    def code():
        return 'A11'

    @staticmethod
    def template():
        return "{{label}}'s value must {{operator}} {{limitlabel}} {{limit}}."


class TypeInvalidError(BaseError):
    def __init__(self, type_name, label, data=None):
        super(TypeInvalidError, self).__init__(type_name=type_name, label=label, data=data)

    @staticmethod
    def code():
        return 'A12'

    @staticmethod
    def template():
        return "{{label}}'s value must be {{type_name}}."


class FormInvalidError(BaseError):
    def __init__(self, it, data=None):
        super(FormInvalidError, self).__init__(it=it, data=data)

    @staticmethod
    def code():
        return 'A24'

    @staticmethod
    def template():
        return "{{it}} Some field value is invalid."


class AuthenticationError(BaseError):
    def __init__(self, it):
        super(AuthenticationError, self).__init__(it=it)

    @staticmethod
    def code():
        return 'A25'

    @staticmethod
    def template():
        return "Please login to access {{it}}."


class AuthorizationError(BaseError):
    def __init__(self, it):
        super(AuthorizationError, self).__init__(it=it)

    @staticmethod
    def code():
        return 'A26'

    @staticmethod
    def template():
        return "You don't have permission to access {{it}}."


class ExistingError(BaseError):
    def __init__(self, it, data=None):
        super(ExistingError, self).__init__(it=it, data=data)

    @staticmethod
    def code():
        return 'A27'

    @staticmethod
    def template():
        return "{{it}} has existed."


class RpcError(BaseError):
    def __init__(self, app_id, path, message, code=None, alias=None, data=None):
        code = code if code is not None else RpcError.code()
        alias = alias if alias is not None else error_alias(RpcError)
        super(RpcError, self).__init__(app_id=app_id, path=path, message=message, code=code, alias=alias, data=data)

    @staticmethod
    def code():
        return 'A28'

    @staticmethod
    def template():
        return "Failed to call {{app_id}}:{{path}} due to {{code}}-{{alias}}-{{message}}."


class IllegalWordError(BaseError):
    def __init__(self, label, illegal_word):
        super(IllegalWordError, self).__init__(label=label, illegal_word=illegal_word)

    @staticmethod
    def code(self):
        return 'A29'

    @staticmethod
    def template():
        return "{{label}} includes the illegal word {{illegal_word}}"


class UniqueError(BaseError):
    def __init__(self, label, value):
        super(UniqueError, self).__init__(label=label, value=value)

    @property
    def code(self):
        return 'A30'

    @staticmethod
    def template():
        return "The value {{value}} of {{label}} has existed."


class CreationError(BaseError):
    def __init__(self, label):
        super(CreationError, self).__init__(label=label)

    @property
    def code(self):
        return 'A31'

    @staticmethod
    def template():
        return "Failed to create record to {{label}}."


class UpdateError(BaseError):
    def __init__(self, label):
        super(UpdateError, self).__init__(label=label)

    @property
    def code(self):
        return 'A32'

    @staticmethod
    def template():
        return "Failed to update record to {{label}}."


class DeleteError(BaseError):
    def __init__(self, label):
        super(DeleteError, self).__init__(label=label)

    @property
    def code(self):
        return 'A33'

    @staticmethod
    def template():
        return "Failed to delete record to {{label}}."


def format_exc_info(exc_info):
    error_class = exc_info[1]
    tb_message = format_traceback(exc_info[2])
    return "%s\n%s" % (str(error_class), tb_message)


def format_traceback(traceback1=None):
    if traceback1 is not None:
        return "".join(traceback.format_tb(traceback1))
    return traceback.format_exc()


def assert_required(value, label):
    """
        check if value is None or empty str.
    """
    if value is None:
        raise RequiredError(label)
    if type(value) == str and len(value.strip()) == 0:
        raise RequiredError(label)
    if isinstance(value, list) and len(value) == 0:
        raise RequiredError(label)
    if isinstance(value, dict) and len(value) == 0:
        raise RequiredError(label)
    return True


def assert_type(value, expected_type, label):
    """
    @param any value:
    @param int|float|bool|list|dict|str|types.GeneratorType|types.FunctionType expected_type:
    @param str label:
    """
    if value is not None and type(value) != expected_type:
        raise TypeInvalidError(str(expected_type), label)
    return True


def assert_in(value, choices, label):
    if value is not None and value not in choices:
        raise ChoiceError(label, choices)
    return True


def assert_equal(value1, value2, label1, label2):
    if value1 != value2:
        raise CompareError(label1, "=", label2, '')


def assert_not_equal(value1, value2, label1, label2):
    if value1 == value2:
        raise CompareError(label1, "!=", label2, '')


def assert_zero_length(value, label):
    if type(value) == list or type(value) == dict:
        if value is None or len(value) == 0:
            raise LengthError(label, 0, 'infinity')


def assert_range(value, minimum, maximum, label):
    if value < minimum or value > maximum:
        raise RangeError(label, minimum, maximum, data=value)


def assert_page(page, per_page):
    assert_required(page, 'Page')
    assert_required(per_page, 'Per Page')
    assert_type(page, int, 'Page')
    assert_type(per_page, int, 'Per Page')


def assert_http_url(url, label):
    assert_type(url, str, label)
    url = url.lower()
    if not url.startswith('http://') and not url.startswith('https://'):
        raise InvalidError(label, data=url)
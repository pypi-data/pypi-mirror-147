# -*- coding: utf-8 -*-
"""
    :author: Dabai
    :url: samuelbaizg.github.io
    :copyright: © 2018 Dabai <zhgbai@163.com>
    :license: MIT, see LICENSE for more details.
"""
import json
import typing
from functools import wraps
from urllib.parse import urljoin

import flask
from flask import Blueprint, current_app, request

from btoolkit import xtype, error
from btoolkit.web.web_constant import WebConstant
from btoolkit.xtype import Singleton, ValueObj


class BaseBP(Blueprint):

    def __init__(self, *args, **kwargs):
        super(BaseBP, self).__init__(*args, **kwargs)
        self._auth_method = None

    def register_auth(self, auth_method: str) -> typing.NoReturn:
        self._auth_method = auth_method

    def authenticate(self) -> bool:
        if self._auth_method is None:
            raise error.InternalError('auth_method is not registered.')
        return self._auth_method()


class ViewBP(BaseBP):

    def route(self, rule: str, **options) -> typing.Callable:
        """
        the decorator to return view.
        :param str rule: url path rule.
        :return function:
        """

        def decorator(f):
            @wraps(f)
            def wrapper(*args, **kwargs):
                self.authenticate()
                data = f(*args, **kwargs)
                return data

            endpoint = options.pop("endpoint", f.__name__)
            self.add_url_rule(rule, endpoint, wrapper, **options)
            return wrapper

        return decorator


class ApiBP(BaseBP):

    def route(self, rule: str, **options) -> typing.Callable:
        """the decorator to return data with the standard format for rest api.
        :param str rule: url path rule.
        :return function:
        """

        def decorator(f):
            @wraps(f)
            def wrapper(*args, **kwargs):
                self.authenticate()
                code = WebConstant.SUCCESS_CODE
                alias = WebConstant.SUCCESS_ALIAS
                message = WebConstant.SUCCESS_MESSAGE
                data = f(*args, **kwargs)
                return JsonRtn(code, alias, message=message, data=data).make_response()

            endpoint = options.pop("endpoint", f.__name__)
            self.add_url_rule(rule, endpoint, wrapper, **options)
            return wrapper

        return decorator


class JsonRtn(object):

    def __init__(self, code: str, alias: str, message: str = None, data: typing.Any = None):
        self._code = code
        self._alias = alias
        self._message = message
        self._data = data

    @property
    def code(self) -> str:
        return self._code

    @property
    def alias(self) -> str:
        return self._alias

    @property
    def message(self) -> str:
        return self._message

    @property
    def data(self) -> typing.Any:
        return self._data

    @staticmethod
    def construct(e_or_res):
        """Create JsonRtn instance from instance of BaseException or requests.Response."""
        if isinstance(e_or_res, error.BaseError):
            code = e_or_res.code()
            alias = e_or_res.alias
            message = e_or_res.message
            data = e_or_res.data
        elif isinstance(e_or_res, BaseException):
            code = WebConstant.UNKNOWN_ERROR_CODE
            alias = error.error_alias(e_or_res)
            message = str(e_or_res)
            data = None
        else:
            result = json.loads(e_or_res.text)
            code = result.get('code')
            alias = result.get('alias')
            message = result.get('message')
            data = result.get('data')
        return JsonRtn(code, alias, message=message, data=data)

    def make_response(self):
        rtn = {'status': self._code, 'alias': self._alias, 'msg': self._message, 'data': self._data}
        return current_app.response_class(xtype.obj_to_json(rtn),
                                          mimetype=current_app.config["JSONIFY_MIMETYPE"])


class Parameter(object, metaclass=Singleton):
    class Converter(object):
        def get_str(self, key: str, default: str = None) -> str:
            value = self.get_all().get(key)
            value = str(value) if value is not None else None
            return value if value is not None else default

        def get_int(self, key: str, default: int = None) -> int:
            value = self.get_all().get(key)
            return xtype.str_to_int(value, default=default)

        def get_float(self, key: str, default: float = None) -> float:
            value = self.get_all().get(key)
            return xtype.str_to_float(value, default=default)

        def get_bool(self, key: str, default: bool = None) -> bool:
            value = self.get_all().get(key)
            return xtype.str_to_bool(value, default=default)

        def get_date(self, key: str, fmt: str = None, default=None):
            value = self.get_all().get(key)
            return xtype.str_to_date(value, fmt=fmt, default=default)

        def get_datetime(self, key, fmt=None, default=None):
            value = self.get_all().get(key)
            return xtype.str_to_datetime(value, fmt=fmt, default=default)

        def get_json_object(self, key: str, default: typing.Any = None) -> typing.Any:
            value = self.get_all().get(key)
            if value is None:
                return default
            value = xtype.json_to_object(value)
            return value if value is not None else default

        def get_dict(self, key: str, default: typing.Dict = None) -> typing.Dict:
            value = self.get_all().get(key)
            return xtype.str_to_dict(value, default=default)

        def to_value_obj(self) -> ValueObj:
            return ValueObj(**self.get_all())

        def get_all(self) -> typing.Dict:
            raise NotImplementedError('Parameter.get_all is not implemented.')

    class ArgConverter(Converter, metaclass=Singleton):

        def get_all(self) -> typing.Dict:
            return request.args

    class FormConverter(Converter, metaclass=Singleton):

        def get_all(self) -> typing.Dict:
            return request.form

    class JsonConverter(Converter, metaclass=Singleton):

        def get_all(self) -> typing.Dict:
            return request.json

    class DataConverter(Converter, metaclass=Singleton):

        def get_all(self) -> typing.Dict:
            return xtype.json_to_object(request.data)

    def __init__(self):
        self._args = self.ArgConverter()
        self._form = self.FormConverter()
        self._json = self.JsonConverter()
        self._data = self.DataConverter()

    @property
    def args(self):
        return self._args

    @property
    def form(self):
        return self._form

    @property
    def json(self):
        return self._json

    @property
    def data(self):
        return self._data


req_param = Parameter()


def get_request_locale() -> str:
    """Return request locale from request cookies."""
    locale = request.cookies.get('locale')
    if locale is not None:
        return locale
    return request.accept_languages.best_match(['en_US', 'zn_CN'])


def get_request_path(full: bool = False) -> str:
    """Return request full path or path."""
    return request.full_path if full else request.path


def get_request_head(head_name: str) -> str:
    """Return head value from request."""
    return request.headers.get(head_name)


def redirect_view(web_context, url, status=None):
    """redirect to url.
    :param str web_context: Web context.
    :param str url: url without site context prefix.
    :param int status:  http status code.
    :return:
    """

    if status is None:
        status = WebConstant.HTTP_REDIRECT_AJAX if is_ajax_request() else WebConstant.HTTP_REDIRECT
    url = url_join(web_context, url)
    return flask.redirect(url, status)


def is_ajax_request() -> bool:
    header = request.headers.get('X-Requested-With')
    return header == 'XMLHttpRequest'


def url_join(*args, last_slash=False):
    """Join relative url segments"""
    prefix = 'http://abc/'
    url = prefix if not args[0].startswith('http://') and not args[0].startswith('https://') else args[0]
    url += '' if url.endswith('/') else '/'
    for arg in args:
        if arg is None or arg == '' or arg == prefix:
            continue
        arg += '' if arg.endswith('/') else '/'
        arg = arg[1:] if arg.startswith('/') else arg
        url = urljoin(url, arg)
    if url.startswith(prefix):
        url = url[10:]
    if last_slash:
        return url if url.endswith('/') else url + '/'
    else:
        return url[:-1] if url.endswith('/') else url


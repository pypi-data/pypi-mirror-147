# -*- coding: utf-8 -*-
"""
    :author: Dabai
    :url: samuelbaizg.github.io
    :copyright: © 2018 Dabai <zhgbai@163.com>
    :license: MIT, see LICENSE for more details.
"""
import logging
import typing
from urllib.parse import urlencode

import requests

from btoolkit import crypto, web, xtype
from btoolkit.constant import ConstantBase
from btoolkit.error import RpcError, assert_required
from btoolkit.web.web_constant import WebConstant
from btoolkit.web.web_base import JsonRtn
from btoolkit.xtype import ValueObj, Singleton


class AuthConstant(ConstantBase):
    # auth head name
    AUTH_HEAD_NAME = 'Authorization'
    AUTH_APP_ID = 'AppId'
    # unit: second
    AUTH_MAX_AGE = 30
    # unit: second
    RPC_CALL_TIMEOUT = 30


class AuthService(object, metaclass=Singleton):
    logger = logging.getLogger(__name__)

    @staticmethod
    def get_app_id():
        """Return app id from request head."""
        return web.get_request_head(AuthConstant.AUTH_APP_ID)

    @staticmethod
    def get_authorization():
        """Return authorization from request head."""
        return web.get_request_head(AuthConstant.AUTH_HEAD_NAME)

    @staticmethod
    def current_user_token() -> ValueObj:
        """Return user info from request head."""
        return ValueObj(user_id='00000001', preferred_timezone=xtype.tz_china(), preferred_language="zh_CN")

    def current_user_id(self) -> str:
        """Return user id from request head."""
        return self.current_user_token().user_id

    @staticmethod
    def __generate_salt(key):
        """generate salt"""
        value = crypto.str_to_sha1_hex(key)
        value += '@#$6￥%^$2d*x&.;1'
        return crypto.str_to_sha256_hex(value)

    def unpack_authorization(self, secret_key, max_age=AuthConstant.AUTH_MAX_AGE):
        """
        Return authorization from request head.
        :param str secret_key: the secret to un-sign object.
        :param int max_age: the alive period. unit: second.
        """

        authorization = web.get_request_head(AuthConstant.AUTH_HEAD_NAME)
        if authorization is None:
            return None
        try:
            authorization = crypto.unsign_object(secret_key, authorization, max_age=max_age,
                                                 salt=self.__generate_salt(secret_key))
        except BaseException as e:
            self.logger.error('Failed to un-sign object due to %s' % str(e))
            authorization = None
        return authorization

    def generate_authorization(self, secret_key, data):
        """
        Generate authorization.
        :param str secret_key:
        :param object data: the object that can be jsonified.
        """
        return crypto.sign_object(secret_key, data, salt=self.__generate_salt(secret_key))


class AuthRpc(object):
    """Remote proc call using auth head."""

    logger = logging.getLogger(__name__)

    class Method(object):

        def __init__(self, client_app_id: str, client_app_static_token, server_address: str, path: str):
            self._client_app_id = client_app_id
            self._client_app_static_token = client_app_static_token
            self._server_address = server_address
            self._path = path

        def __call__(self, authorization, method: str = WebConstant.HTTP_METHOD_GET,
                     path_data=None, body_data: object = None, header_data=None,
                     timeout=AuthConstant.RPC_CALL_TIMEOUT) -> typing.Any:
            """
            Call restful api.
            :param str authorization: The authorization will be verified by server.
            :param str method: request method of restful api.
            :param dict path_data: the parameters after ? in url.
            :param object body_data: (optional) Dictionary, list of tuples, bytes, or file-like
                                    object to send in the request body.
            :param dict header_data: data in http headers.
            :Return Any object if json response else class<Response> object
            """
            assert_required(authorization, 'authorization')
            url = self.build_url(self._path, path_data)
            headers = self.build_headers(authorization, header_data)

            def is_json(res):
                return True if WebConstant.HTTP_CONTENT_TYPE in res.headers and res.headers[
                    WebConstant.HTTP_CONTENT_TYPE] == WebConstant.HTTP_CONTENT_TYPE_JSON else False

            try:
                response = requests.request(method, url, headers=headers, data=body_data, timeout=timeout)
                if not is_json(response):
                    return response
                rtn = JsonRtn.construct(response)
            except BaseException as e:
                AuthRpc.logger.error('Failed to call %s due to %s' % (url, str(e)))
                raise RpcError(self._app_id, self._path, str(e))
            else:
                if rtn.code != WebConstant.SUCCESS_CODE:
                    raise RpcError(self._app_id, self._path, rtn.message, code=rtn.code, alias=rtn.alias, data=rtn.data)
                return rtn.data

        def build_url(self, path: str, path_data=None) -> str:
            url = web.url_join(self._server_address, path)
            if path_data is not None:
                url = '%s?%s' % (url, urlencode(path_data))
            return url

        @staticmethod
        def build_headers(authorization, **kwargs) -> typing.Dict:
            if kwargs is None:
                return dict()
            headers = dict()
            headers[AuthConstant.AUTH_HEAD_NAME] = authorization
            xtype.dict_merge(headers, kwargs)
            return headers

    def __init__(self, client_app_id, client_app_static_token, server_address):
        """
        :param str client_app_id: the app id to call remote proc.
        :param str client_app_static_token: the app static token to call remote proc.
        """
        self._client_app_id = client_app_id
        self._client_app_static_token = client_app_static_token
        self._server_address = server_address

    def __getitem__(self, path):
        """
        :param str path: the remote rest api path, such as /abc/defG
        """
        return self.Method(self._client_app_id, self._client_app_static_token, self._server_address, path)

    def __getattr__(self, path):
        """
        :param str path: using __bs1__ to define /, such as the real path is abc/defG,
        the argument path should be abc__bs1__defG
        """
        path = path.replace("__bs1__", "/")
        return self.__getitem__(path)


def current_user():
    """Return  current user."""
    AuthService().current_user_token()


def current_user_id():
    """Return  current user id."""
    AuthService().current_user_id()

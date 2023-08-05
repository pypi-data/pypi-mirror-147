# -*- coding: utf-8 -*-
"""
    :author: Dabai
    :url: samuelbaizg.github.io
    :copyright: © 2018 Dabai <zhgbai@163.com>
    :license: MIT, see LICENSE for more details.
"""
from btoolkit.constant import ConstantBase


class WebConstant(ConstantBase):
    """Web Constants."""
    SUCCESS_CODE = 'A00'
    SUCCESS_ALIAS = 'SUCCESS'
    SUCCESS_MESSAGE = 'SUCCESS'
    UNKNOWN_ERROR_CODE = 'Z99'

    HTTP_SUCCESS = 200
    HTTP_SUCCESS_ERROR = 211
    HTTP_SUCCESS_FORM_INVALID = 212

    HTTP_REDIRECT = 301
    HTTP_REDIRECT_AJAX = 311

    HTTP_BAD_REQUEST = 400
    HTTP_NOT_FOUND = 404
    HTTP_NO_AUTHORIZATION = 403
    HTTP_NO_AUTHENTICATION = 401

    HTTP_INTERVAL_ERROR = 500

    HTTP_METHOD_GET = 'GET'
    HTTP_METHOD_POST = 'POST'
    HTTP_METHOD_PUT = 'PUT'
    HTTP_METHOD_DELETE = 'DELETE'

    HTTP_CONTENT_TYPE = 'Content-Type'
    HTTP_CONTENT_TYPE_JSON = 'application/json'

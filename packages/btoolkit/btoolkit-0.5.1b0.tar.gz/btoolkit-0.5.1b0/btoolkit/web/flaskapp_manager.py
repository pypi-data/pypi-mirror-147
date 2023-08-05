# -*- coding: utf-8 -*-
"""
    :author: Dabai
    :url: samuelbaizg.github.io
    :copyright: © 2018 Dabai <zhgbai@163.com>
    :license: MIT, see LICENSE for more details.
"""
import logging
import os
import typing

from flask import current_app, Flask
from flask import request
from flask_sqlalchemy import get_debug_queries

from btoolkit import error
from btoolkit.web.web_base import JsonRtn
from btoolkit.web.web_constant import WebConstant
from btoolkit.xtype import Singleton


class FlaskAppManager(object, metaclass=Singleton):

    logger = logging.getLogger(__name__)

    def create_flask_application(self, app_id, root_path, flask_conf_dict,
                                 error_render=None, extension_register=None,
                                 blueprint_register=None, request_handler_register=None):
        """
        Create flask app
        :param str app_id:
        :param str root_path:
        :param dict flask_conf_dict:
        :param function error_render:
        :param function extension_register:
        :param function blueprint_register:
        :param function request_handler_register:
        Return flask.Application
        """
        static_folder = os.path.join(root_path, 'static')
        template_folder = os.path.join(root_path, 'templates')
        app = Flask(app_id, root_path=root_path, static_folder=static_folder, template_folder=template_folder)
        app.secret_key = flask_conf_dict.get('APP_SECRET_KEY')
        app.config.from_mapping(**flask_conf_dict)
        self.register_error_handler(app, error_render)
        if extension_register:
            extension_register(app)
        if blueprint_register:
            blueprint_register(app)
        if request_handler_register:
            request_handler_register(app)
        if flask_conf_dict.get("DEBUG"):
            def query_profiler(response):
                threshold = flask_conf_dict.get('SLOW_QUERY_THRESHOLD')
                if not threshold:
                    return response
                for q in get_debug_queries():
                    if q.duration >= threshold:
                        self.logger.warning(
                            'Slow query: Duration: %fs\n Context: %s\nQuery: %s\n '
                            % (q.duration, q.context, q.statement)
                        )
                return response

            app.after_request(query_profiler)
        return app

    def render_exception_response(self, status, title, e):
        """render exception response"""
        msg = '[%s] %s' % (request.path, e)
        self.logger.exception(msg)
        rtn = JsonRtn.construct(e)
        return rtn.make_response(), status

    def register_error_handler(self, app: Flask, error_render: typing.Callable, handlers: typing.List = None) -> typing.NoReturn:
        """
        Register error handlers to Flask application.
        :param Flask.Application app:
        :param function(status, message, e) error_render: function with 3 arguments.
            int status: Http status code.
            str message: Http status message.
            Exception e: Exception instance.
        :param [(error code or exception, handler function)] handlers: additional error handlers.
        """
        if error_render is None:
            error_render = self.render_exception_response

        @app.errorhandler(WebConstant.HTTP_BAD_REQUEST)
        def bad_request(e) -> typing.Any:
            return error_render(WebConstant.HTTP_BAD_REQUEST, 'Bad Request', e)

        @app.errorhandler(WebConstant.HTTP_NOT_FOUND)
        def page_not_found(e) -> typing.Any:
            return error_render(WebConstant.HTTP_NOT_FOUND, 'Page Not Found', e)

        @app.errorhandler(WebConstant.HTTP_INTERVAL_ERROR)
        def internal_server_error(e) -> typing.Any:
            return error_render(WebConstant.HTTP_INTERVAL_ERROR, 'Internal Server Error', e)

        @app.errorhandler(error.BaseError)
        def request_error(e):
            return error_render(WebConstant.HTTP_SUCCESS_ERROR, e.alias, e)

        @app.errorhandler(error.FormInvalidError)
        def request_error(e):
            return error_render(WebConstant.HTTP_SUCCESS_FORM_INVALID, e.alias, e)

        @app.errorhandler(error.AuthenticationError)
        def authentication_error(e):
            return error_render(WebConstant.HTTP_NO_AUTHENTICATION, e.alias, e)

        @app.errorhandler(error.AuthorizationError)
        def authorization_error(e):
            return error_render(WebConstant.HTTP_NO_AUTHORIZATION, e.alias, e)

        @app.errorhandler(Exception)
        def unknown_error(e):
            return error_render(WebConstant.HTTP_INTERVAL_ERROR, 'Unknown Server Error', e)

        if handlers is None:
            return

        for (code_ex, handler) in handlers:
            app.register_error_handler(code_ex, handler)

    @staticmethod
    def get_all_routes(app: Flask = None) -> str:
        """Return all routes."""
        app = app if app is not None else current_app
        return app.url_map


app_manager = FlaskAppManager()

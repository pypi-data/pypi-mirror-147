# -*- coding: utf-8 -*-
"""
    :author: Dabai
    :url: samuelbaizg.github.io
    :copyright: © 2018 Dabai <zhgbai@163.com>
    :license: MIT, see LICENSE for more details.
"""
import logging
from logging import config

from flask.cli import ScriptInfo

from btoolkit import xglobal


class ClickContext(ScriptInfo):
    """Command context."""

    def __init__(self, app_info, create_app):
        """
        :param dict app_info:
        :param function create_app(app_id, app_root_path, configuration): the function of creating flask app.
        """
        super(ClickContext, self).__init__(set_debug_flag=False)
        self._app_info = app_info
        self._create_app = create_app
        self._loaded_app = None
        self.load_app()

    def is_debug(self):
        """Return True for debug mode."""
        return self._app_info.get_flask_config("DEBUG")

    def get_app_info(self):
        """Return instance of ConfigHolder."""
        return self._app_info

    def load_app(self):
        """Loaded Flask App"""
        if self._loaded_app is not None:
            return self._loaded_app

        def load_create_app():
            log_dict = self._app_info.get_logging_config()
            config.dictConfig(log_dict)
            xglobal.set_app_info(self._app_info)
            flask_config_dict = self._app_info.get_flask_config()
            application = self._create_app(self._app_info.app_id, self._app_info.app_root_path, flask_config_dict)
            return application

        app = load_create_app()
        self._loaded_app = app
        return app


def make_click_context(app_info, create_app):
    class ClickContextWrapper(ClickContext):

        def __init__(self):
            super(ClickContextWrapper, self).__init__(app_info, create_app)

    return ClickContextWrapper

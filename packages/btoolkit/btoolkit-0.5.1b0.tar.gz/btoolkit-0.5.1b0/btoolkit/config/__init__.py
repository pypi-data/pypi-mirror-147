# -*- coding: utf-8 -*-
"""
    :author: Dabai
    :url: samuelbaizg.github.io
    :copyright: © 2018 Dabai <zhgbai@163.com>
    :license: MIT, see LICENSE for more details.
"""
import logging
import os

from btoolkit import xtype, xfile, error
from btoolkit.config import nacos_client
from btoolkit.constant import CommonConstant
from btoolkit.error import NoFoundError


class AppInfo(object):
    """field values defined in app.yml"""

    def __init__(self, app_root_path, app_yml_abs_path):
        self._app_root_path = app_root_path
        self._app_yml_abs_path = app_yml_abs_path
        self._app_id = None
        self._app_version = None
        self._environment = None
        self._app_static_token = None
        self._config_center_url = None
        self._namespace = None
        self._config_set_ids = list()
        self._config_infos = dict()
        self._parse_app_yaml()

    @property
    def app_id(self):
        return self._app_id

    @property
    def app_version(self):
        return self._app_version

    @property
    def environment(self):
        return self._environment

    @property
    def app_static_token(self):
        return self._app_static_token

    @property
    def config_center_url(self):
        return self._config_center_url

    @property
    def app_root_path(self):
        return self._app_root_path

    @property
    def namespace(self):
        return self._namespace

    def get_config_infos(self):
        return self._config_infos.copy()

    def get_config_info(self, config_set_id) -> object:
        """
        if item_id is None, return all items of config_set_id, or else
        return a specific item value of a config item in config set.
        """
        error.assert_required(config_set_id, "config_set_id")
        if config_set_id not in self._config_infos:
            raise error.NoFoundError("config_set_id", config_set_id)
        return self._config_infos.get(config_set_id)

    def get_flask_config(self, item_id=None):
        """Return flask config item value."""
        config_set_id = "{}-{}".format(self._app_id, CommonConstant.FLASK)
        config_set = self.get_config_info(config_set_id).config_set
        return config_set.get(item_id) if item_id is not None else config_set

    def get_logging_config(self, item_id=None):
        """Return logging config item value."""
        config_set_id = "{}-{}".format(self._app_id, CommonConstant.LOGGING)
        config_set = self.get_config_info(config_set_id).config_set
        return config_set.get(item_id) if item_id is not None else config_set

    def get_gunicorn_config(self, item_id=None):
        """Return gunicorn config item value."""
        config_set_id = "{}-{}".format(self._app_info.app_id, CommonConstant.GUNICORN)
        config_set = self.get_config_info(config_set_id).config_set
        return config_set.get(item_id) if item_id is not None else config_set

    def _parse_app_yaml(self):
        """Read and parse app.yml."""
        app_dict = xfile.read_yaml(self._app_yml_abs_path)
        self._app_id = app_dict['app_id']
        self._app_version = app_dict['app_version']
        self._app_static_token = app_dict['app_static_token']
        self._namespace = app_dict['namespace']
        self._environment = app_dict['environment']
        self._config_center_url = app_dict.get('config_center_url')
        self._config_set_ids = app_dict['config_set_ids']
        for config_set_id in self._config_set_ids:
            config_info = ConfigInfo(self, config_set_id)
            self._config_infos[config_set_id] = config_info

    def _refresh_config_set(self, config_set_id):
        """Refresh config set."""
        config_info = ConfigInfo(self, config_set_id)
        self._config_infos[config_set_id] = config_info


class ConfigInfo(object):
    """Load config items from local or remote config file.
    support file://, ccenter:// protocol to read config items.
    """

    logger = logging.getLogger(__name__)

    def __init__(self, app_info, config_set_id):
        self._app_info = app_info
        self._config_set_id = config_set_id
        self._config_set = self._read_config_set()

    @property
    def config_set(self) -> dict:
        """Return config value."""
        return self._config_set

    def refresh_config_set(self):
        """Refresh config value in this instance."""
        self._config_set = self._read_config_set()

    def _read_config_set(self) -> dict:
        """Read config value from config file or config center."""
        return self._read_config_set_from_center()

    def _read_config_set_from_center(self) -> dict:
        """Read config from config center"""
        if self._app_info.config_center_url is None:
            self.logger.warning("config_center_url is not configured.")
            return None
        data = nacos_client.get_config_set(self._app_info.config_center_url, self._app_info.namespace,
                                           self._app_info.app_id,
                                           self._app_info.environment,
                                           self._config_set_id)
        if xtype.str_is_blank(data):
            self.logger.error("Nothing is returned from config center.")
            raise NoFoundError('config set id', self._config_set_id, 'config center.')
        self._update_config_local_cache(self._app_info.namespace, self._app_info.app_id, self._app_info.environment,
                                        self._config_set_id, data)
        value = self._replace_variables(data)
        items = xtype.yaml_to_object(value)
        return items

    def _replace_variables(self, string):
        string = string.replace('{APP_ROOT_PATH}', self._app_info.app_root_path)
        return string

    def _get_config_local_cache_file_path(self, namespace, app_id, environment, config_set_id):
        """Return config local cache path."""
        path = os.path.join(self._app_info.app_root_path, 'configs',
                            namespace, environment)
        os.makedirs(path, exist_ok=True)
        path = os.path.join(path, '{}.yaml'.format(config_set_id))
        return path

    def _update_config_local_cache(self, namespace, app_id, environment, config_set_id, config_set) -> bool:
        """Refresh local config cache"""
        fp = self._get_config_local_cache_file_path(namespace, app_id, environment, config_set_id)
        xfile.write_file(fp, config_set)


def initialize_config(app_root_path, app_yml_abs_path):
    """Initialize config and return config holder."""
    app_info = AppInfo(app_root_path, app_yml_abs_path)
    return app_info

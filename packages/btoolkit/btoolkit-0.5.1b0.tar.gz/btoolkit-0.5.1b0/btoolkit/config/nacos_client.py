# -*- coding: utf-8 -*-
"""
    :author: Dabai
    :url: samuelbaizg.github.io
    :copyright: © 2018 Dabai <zhgbai@163.com>
    :license: MIT, see LICENSE for more details.
"""
import urllib

import requests


def get_config_set(config_center_url, namespace, app_id, environment, config_set_id):
    """Call nacos open api /nacos/v1/cs/configs"""
    context = "/nacos/v1/cs/configs"
    params = {
        "tenant": namespace,
        "group": environment,
        "dataId": config_set_id
    }
    url = get_absolute_url(config_center_url, context, params)
    response = requests.get(url)
    if response.status_code == 200:
        return response.text
    return None


def get_absolute_url(config_center_url, context, params=None):
    uri = "%s%s" % (config_center_url, context)
    if params is not None:
        return "{}?{}".format(uri, urllib.parse.urlencode(params))
    return uri

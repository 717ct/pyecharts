# coding=utf-8
from __future__ import unicode_literals

import warnings


import pyecharts.constants as constants
from pyecharts.conf import CURRENT_CONFIG


def configure(jshost=None,
              echarts_template_dir=None,
              force_js_embed=None,
              **kwargs):
    """ Config all items for pyecharts when use chart.render()
    or page.render().

    :param jshost:
    :param echarts_template_dir:
    :param force_js_embed:
    :param kwargs:
    """
    if jshost:
        CURRENT_CONFIG.jshost = jshost
    if echarts_template_dir:
        CURRENT_CONFIG.echarts_template_dir = echarts_template_dir
    if force_js_embed is not None:
        CURRENT_CONFIG.force_js_embed = force_js_embed


def online(host=constants.DEFAULT_HOST):
    """ Set the jshost

    :param host:
    """
    warnings.warn(
        "Deprecated since 0.3.0! Please use pyecharts.configure() instead.")
    CURRENT_CONFIG.jshost = host


# TODO Merge the following js functions to pyecharts.utils module or new one.
def produce_require_configuration(dependencies, jshost):
    """

    :param dependencies:
    :param jshost:
    :return:
    """
    _d = ensure_echarts_is_in_the_front(dependencies)
    # if no nick name register, we treat the location as location.js
    require_conf_items = [
        "'%s': '%s/%s'" % (key,
                           jshost,
                           CURRENT_CONFIG.get_js_library(key))
        for key in _d]
    require_libraries = ["'%s'" % key for key in _d]
    return dict(
        config_items=require_conf_items,
        libraries=require_libraries
    )


def produce_html_script_list(dependencies):
    """

    :param dependencies:
    :return:
    """
    _d = ensure_echarts_is_in_the_front(dependencies)
    script_list = [
        '%s' % CURRENT_CONFIG.get_js_library(key)
        for key in _d]
    return script_list


def ensure_echarts_is_in_the_front(dependencies):
    """ make sure echarts is the item in the list
    require(['echarts'....], function(ec) {..}) need it to
    be first but dependencies is a set so has no sequence

    :param dependencies:
    :return:
    """
    if len(dependencies) > 1:
        dependencies.remove('echarts')
        dependencies = ['echarts'] + list(dependencies)
    elif len(dependencies) == 1:
        # make a new list
        dependencies = list(dependencies)
    else:
        raise Exception("No js library found. Nothing works!")
    return dependencies

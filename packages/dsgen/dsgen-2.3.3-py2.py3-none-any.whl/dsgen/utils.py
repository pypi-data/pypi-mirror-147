# -*- python3 -*-
#
# Copyright 2021, 2022 Cecelia Chen
# Copyright 2018, 2019, 2020, 2021 Xingeng Chen
# Copyright 2016, 2017, 2018 Liang Chen
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.'''
#
# dsgen.utils

import json

from .base import DSBase, CeleryHelper
from .message import MSG_FORMAT_ERROR_LOADING_JSON


class DSGenerator(DSBase):
    '''
    instantisilize a sub-class of this, and override module-level reference to instance method
    `__dir__` => `get_config_field_list`
    `__getattr__` => get_config_value`
    '''

    def __init__(self, json_path=None):
        '''
        :param json_path: (string)
        '''
        super(DSGenerator, self).__init__()
        if json_path is not None:
            try:
                with open(json_path, 'r') as json_f:
                    self.site_config = json.load(json_f)
            except Exception as e:
                from django.core.exceptions import ImproperlyConfigured
                msg = MSG_FORMAT_ERROR_LOADING_JSON.format(fp=json_path)
                bad_config = ImproperlyConfigured(msg)
                raise bad_config
        self.collect_apps()

    def get_config_field_list(self):
        return list(self.site_config.keys())

    def get_config_value(self, name):
        '''
        :param name: (string)
        '''
        if name.startswith('_'):
            value = globals().get(name)
        else:
            value = getattr(
                self,
                name,
                self.site_config.get(name)
            )
        return value


class DSetting(object):
    '''
    base-class for Django app setting

    subclass MUST declare the following attributes:
    - `DEFAULT` (dict)
    - `SETTING_NAME` (string)

    subclass MAY declare the following attributes:
    - `PASSTHROUGH_FIELDS` (list/tuple)
    '''

    def __init__(self):
        self._default = self.DEFAULT
        self._cache_key = set()
        from django.conf import settings as _ds_conf
        self._ds_conf = _ds_conf

    @property
    def site_conf(self):
        if not hasattr(self, '_site'):
            _conf = getattr(
                self._ds_conf,
                self.SETTING_NAME,
                dict()
            )
            setattr(
                self,
                '_site',
                _conf
            )
        return self._site

    def __getattr__(self, attr):
        pass_through_list = getattr(
            self,
            'PASSTHROUGH_FIELDS',
            list()
        )
        if attr in pass_through_list:
            return getattr(self._ds_conf, attr)
        if attr not in self._default:
            raise AttributeError("Invalid setting: '%s'" % attr)

        try:
            val = self.site_conf[attr]
        except KeyError:
            val = self._default[attr]

        self._cache_key.add(attr)
        setattr(self, attr, val)
        return val

    def signal_handler_setting_changed(self, *args, **kwargs):
        '''
        stub handler for `django.test.signals.setting_changed`
        '''
        if kwargs['settings'] == self.SETTING_NAME:
            self.reload()
        return None

    def reload(self):
        for item in self._cache_key:
            delattr(self, item)
        self._cache_key.clear()
        if hasattr(self, '_site'):
            delattr(self, '_site')
        return None


#---eof---#

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
# dsgen.base

class DSBase(object):
    '''
    base-class
    '''

    def collect_apps(self, extra=None):
        self.INSTALLED_APPS = list()
        self.INSTALLED_APPS.extend(self.default_app_list)
        return self


class CeleryHelper(object):
    '''
    helper class for Celery task schedule and queue definition
    '''

    def route_for_task(self, task, args=None, kwargs=None):
        '''
        :param task: ()
        '''

    def convert_queue_definition(self, data):
        '''
        construct Celery queue definition

        ```json
        {
            "name": "demo",
            "exchange": "demo",
            "exchange.type": "direct",
            "routing_key": "task"
        }
        ```

        :param data: plain values from JSON (dict)
        :return: conversion result (dict)
        '''
        from kombu import Exchange, Queue
        exch = Exchange(
            data.get('exchange', data['name']),
            type=data.get('exchange.type', 'fanout'),
        )
        queue = Queue(
            data['name'],
            exch,
            routing_key=data['routing_key'],
        )
        return queue

    def create_schedule(self, data):
        '''
        construct Celery schedule objects

        ```json
        {
            "task-description": {
                "task": "app.tasks.a_simple_task",
                "schedule": timedelta(minutes=30)
            },
            "second-task-description": {
                "task": "app.tasks.another_task",
                "schedule": crontab(minute='3', hour='0,1,2,6,7,8,9,10,11')
            }
        }
        ```

        :param data: plain values from JSON (dict)
        :return: conversion result (dict)
        '''
        from celery.schedules import crontab
        from datetime import timedelta

        val = dict()
        val.update(conf)
        for task in val.keys():
            raw_val = val[ task ]['schedule']
            try:
                tokens = raw_val.split('=', 1)
                td_param = {
                    tokens[0]: int(tokens[1]),
                }
                val[ task ]['schedule'] = timedelta(**td_param)
            except AttributeError:
                val[ task ]['schedule'] = crontab(**raw_val)
            except ValueError:
                # currently we just drop the incorrectly defined items;
                pass
            pass  #-end-for-task-in
        return val


#---eof---#

# :coding: utf-8
# :copyright: Copyright (c) 2015 ftrack

import c4d
import c4d.plugins

import time
import uuid
import ctypes

import logging
import threading
import collections

#: ftrack message data plugin id
PLUGIN_ID = 1037466


class ProcessQueue(object):
    def __init__(self):
        self.__jobs = dict()
        self.__results = dict()
        self.__mutex = threading.Lock()

    def add(self, fn, *args, **kwargs):
        uid = int(uuid.uuid1().int>>102)

        with self.__mutex:
            self.__jobs.setdefault(
                uid, {
                    'fn':fn,
                    'args':args,
                    'kwargs':kwargs
                }
            )

        return uid

    def get(self, uid):
        data = None

        with self.__mutex:
            data = self.__jobs.pop(
                uid, None
            )

        return data

    def get_result(self, uid, default=None):
        with self.__mutex:
            return self.__results.pop(
                uid, default
            )

    def task_done(self, uid, result):
        with self.__mutex:
            self.__results.setdefault(
                uid, result
            )


class FtrackMessageData(c4d.plugins.MessageData):
    '''ftrack message data plugin.'''

    __queue = ProcessQueue()

    def __init__(self, *args, **kwargs):
        '''Instantiate ftrack message data.'''
        super(FtrackMessageData, self).__init__(*args, **kwargs)
        self.logger = logging.getLogger(
            __name__ + '.' + self.__class__.__name__
        )

    def CoreMessage(self, id, message):
        '''Handle core *message* with *id* in main thread.

        Will listen for messages directed to *PLUGIN_ID* and call event
        handlers defined in `EVENT_HANDLERS` with decoded data.

        In a separate thread, call an event handler using the logic::

            p1, p2 = save_event_data(topic, data)
            c4d.SpecialEventAdd(PLUGIN_ID, p1, p2)
        '''
        if id == PLUGIN_ID:
            self.logger.debug(
                u'Handling core message {0!r}: {1!r}'.format(id, message)
            )

            uid_id_pointer = message.GetVoid(
                c4d.BFM_CORE_PAR1
            )


            ctypes.pythonapi.PyCapsule_GetPointer.restype = ctypes.c_void_p
            ctypes.pythonapi.PyCapsule_GetPointer.argtypes = [ctypes.py_object]

            uid = ctypes.pythonapi.PyCapsule_GetPointer(uid_id_pointer, None)

            task = self.__queue.get(
                ctypes.pythonapi.PyCapsule_GetPointer(uid_id_pointer, None)
            )

            if task is not None:

                try:
                    result = task.get('fn')(
                        *task.get('args', []), **task.get('kwargs', {})
                    )

                except Exception as e:
                    self.logger.exception(
                        e
                    )

                    result = e

                self.__queue.task_done(
                    uid, result
                )

                self.logger.debug(
                    u'Message handler result: {0!r}'.format(result)
                )

        return True

    @classmethod
    def execute_deferred(cls, fn, *args, **kwargs):
        uid = cls.__queue.add(
            fn, *args, **kwargs
        )

        c4d.SpecialEventAdd(
            PLUGIN_ID, p1=uid
        )

        return uid


    @classmethod
    def execute_in_main_thread(cls, fn, *args, **kwargs):
        uid = cls.execute_deferred(
            fn, *args, **kwargs
        )

        result = None
        while result is None:
            time.sleep(
                0.1
            )

            result = cls.__queue.get_result(
                uid, default=None
            )

        if isinstance(result, Exception):
            raise result

        return result




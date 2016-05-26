# :coding: utf-8
# :copyright: Copyright (c) 2015 ftrack

import c4d
import c4d.plugins

import ctypes
import zlib
import logging
import collections

import ftrack_connect_cinema_4d.core_message_event

# TODO: Replace this ID
PLUGIN_ID = 1230002


class FtrackMessageData(c4d.plugins.MessageData):
    '''ftrack message data plugin.'''

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
            topic_id_pointer = message.GetVoid(c4d.BFM_CORE_PAR1)
            data_id_pointer = message.GetVoid(c4d.BFM_CORE_PAR2)
            ctypes.pythonapi.PyCObject_AsVoidPtr.restype = ctypes.c_void_p
            ctypes.pythonapi.PyCObject_AsVoidPtr.argtypes = [ctypes.py_object]
            topic_id = ctypes.pythonapi.PyCObject_AsVoidPtr(topic_id_pointer)
            data_id = ctypes.pythonapi.PyCObject_AsVoidPtr(data_id_pointer)

            self.logger.debug(
                u'Dereferenced message content: {0!r}'.format((topic_id, data_id))
            )
            result = ftrack_connect_cinema_4d.core_message_event.handle_event(
                topic_id, data_id
            )
            self.logger.debug(u'Message handler result: {0!r}'.format(result))

        return True

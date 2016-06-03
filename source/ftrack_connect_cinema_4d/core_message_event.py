# :coding: utf-8
# :copyright: Copyright (c) 2016 ftrack

import c4d

import logging

import ftrack_connect_cinema_4d.asset
import ftrack_connect_cinema_4d.plugin.ftrack_message_data

logger = logging.getLogger('ftrack_connect_cinema_4d.core_message_event')

#: Event topics: map topic names to integers usable by `SpecialEventAdd`.
EVENT_TOPICS = {
    'IMPORT_OBJECT_FROM_FILE_PATH': 1,
}

#: Map functions to event message topic ids.
EVENT_HANDLERS = {
    EVENT_TOPICS['IMPORT_OBJECT_FROM_FILE_PATH']: (
        lambda data: ftrack_connect_cinema_4d.asset.import_object_from_file_path(**data)
    )
}

#: Event data storage: store data identified by indices usable by `SpecialEventAdd`.
#
# Reserve `None` as the first element since `SpecialEventAdd` expects positive
# integers as arguments.
EVENT_DATA = [None]


def send_event(topic, data=None):
    '''Send `special event` which will be executed in main thread.

    *topic* should be defined in `EVENT_TOPICS` with a handler defined in
    `EVENT_HANDLERS`.

    *data* will be stored and used as argument to the event handler.
    '''
    topic_id = EVENT_TOPICS[topic]
    data_id = len(EVENT_DATA)
    EVENT_DATA.append(data)

    logger.debug(
        u'Saved data at ({0!r}, {1!r}): {2!r}'.format(topic_id, data_id, data)
    )

    c4d.SpecialEventAdd(
        ftrack_connect_cinema_4d.plugin.ftrack_message_data.PLUGIN_ID,
        p1=topic_id,
        p2=data_id
    )
    return True


def handle_event(topic_id, data_id):
    '''Handle core message event for *topic_id*, *data_id*.'''
    data = EVENT_DATA[data_id]
    logger.debug(
        u'Read data at ({0!r}, {1!r}): {2!r}'.format(topic_id, data_id, data)
    )

    handler = EVENT_HANDLERS.get(topic_id, None)
    if handler:
        return handler(data)

    logger.warning(
        'No handler defined for ({0!r}, {1!r})'.format(topic_id, data_id)
    )

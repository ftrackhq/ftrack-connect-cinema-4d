# :coding: utf-8
# :copyright: Copyright (c) 2015 ftrack

import threading
import functools
import logging
import os.path

import c4d.gui

import ftrack_connect_cinema_4d.asset
import ftrack_connect_cinema_4d.publish


from ftrack_connect_cinema_4d.plugin.ftrack_message_data import (
    FtrackMessageData
)

logger = logging.getLogger('ftrack_connect_cinema_4d.event')


def show_debug_message(session, data):
    '''Display message'''
    c4d.gui.MessageDialog(data['message'])
    return {'success': True}


def get_publish_options(session, data):
    '''Get publish options'''
    return dict(
        name=ftrack_connect_cinema_4d.publish.get_document_name()
    )

def publish_media(session, options):
    logger.info(u'publish media')


    result = FtrackMessageData.execute_in_main_thread(
        ftrack_connect_cinema_4d.publish.publish, session, options
    )

    logger.info(u'Published: {0}'.format(result))
    return result


def get_import_components(session, data):
    '''Export media with *options*.'''
    logger.info(u'Getting import components: {0!r}'.format(data))
    result = ftrack_connect_cinema_4d.asset.get_importable_components(
        session, data['versionId']
    )
    logger.info(u'Result: {0!r}'.format(result))
    return result


def import_component(session, data):
    '''Import component in *data*.'''
    logger.info(u'Importing component: {0!r}'.format(data))

    result = FtrackMessageData.execute_in_main_thread(
        ftrack_connect_cinema_4d.asset.import_object_from_file_path, *[], **data
    )
    logger.info(u'Result: {0!r}'.format(result))
    return result


#: Map functions to event names
event_handlers = dict(
    show_debug_message=show_debug_message,
    get_publish_options=get_publish_options,
    publish_media=publish_media,
    get_import_components=get_import_components,
    import_component=import_component,
)


def _get_error_message(error):
    '''Return error message from *error*.'''
    message = None
    if hasattr(error, 'detail'):
        message = str(error.detail)
    elif hasattr(error, 'explanation'):
        message = str(error.explanation)
    else:
        message = str(error)

    return message


def handle_event(event, session=None):
    '''Handle *event* and publish components.'''
    logger.info('Handling event: {0!r}'.format(event))

    topic = event['topic']
    functionName = topic.replace('ftrack.connect-cinema-4d.', '')
    result = None

    try:
        data = event['data']
        output = event_handlers[functionName](session, data)
        result = {
            'success': True,
            'output': output
        }

    except Exception as error:
        logger.exception('Failed to process event')
        result = {
            'success': False,
            'exception': type(error).__name__,
            'content': _get_error_message(error)
        }

    logger.info('Returning event result: {0!r}'.format(result))
    return result


def subscribe(session):
    '''Subscribe to events.'''
    topic = 'ftrack.connect-cinema-4d.*'
    logger.info('Subscribing to event topic: {0!r}'.format(topic))
    return session.event_hub.subscribe(
        u'topic="{0}" and source.user.username="{1}"'.format(
            topic, session.api_user
        ),
        functools.partial(handle_event, session=session)
    )


class EventHubThread(threading.Thread):
    '''Listen for events from ftrack's event hub.'''

    def start(self, session):
        '''Start thread for *session*.'''
        self._session = session
        super(EventHubThread, self).start()

    def run(self):
        '''Listen for events.'''
        self._session.event_hub.wait()

# :coding: utf-8
# :copyright: Copyright (c) 2015 ftrack

import threading
import functools
import logging
import os.path

import c4d.gui

import ftrack_connect_cinema_4d.publish

logger = logging.getLogger('ftrack_connect_cinema_4d.event')


def show_debug_message(data):
    '''Display message'''
    c4d.gui.MessageDialog(data['message'])
    return {'success': True}


def get_publish_options(data):
    '''Get publish options'''
    return dict(
        name=ftrack_connect_cinema_4d.publish.get_document_name()
    )


def export_media(options):
    '''Export media with *options*.'''
    logger.info(u'Exporting files')
    files = []
    if options.get('delivery', False):
        document_path = ftrack_connect_cinema_4d.publish.export_c4d_document()
        filename, file_extension = os.path.splitext(document_path)
        files.append({
            'use': 'delivery',
            'name': 'c4d-document',
            'path': document_path,
            'extension': file_extension,
            'size': os.path.getsize(document_path),
        })

    logger.info(u'Exported files: {0}'.format(files))
    return files


def upload_media(data):
    '''Upload media.'''
    raise NotImplementedError('upload_media is not implemented yet.')


#: Map functions to event names
event_handlers = dict(
    show_debug_message=show_debug_message,
    get_publish_options=get_publish_options,
    export_media=export_media,
    upload_media=upload_media,
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
        output = event_handlers[functionName](data)
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

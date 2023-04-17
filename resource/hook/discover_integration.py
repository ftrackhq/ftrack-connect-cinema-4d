# :coding: utf-8
# :copyright: Copyright (c) 2021 ftrack

import functools
import getpass
import sys
import pprint
import logging
import re
import os

import ftrack_api


def on_discover_cinema_integration(session, event):

    data = {
        'integration': {
            "name": 'ftrack-connect-cinema-4d',
            'version': '0.2.2'
        }
    }
    return data


def register(session):
    '''Subscribe to application launch events on *registry*.'''
    if not isinstance(session, ftrack_api.session.Session):
        return

    handle_event = functools.partial(
        on_discover_cinema_integration,
        session
    )
    session.event_hub.subscribe(
        'topic=ftrack.connect.application.launch'
        ' and data.application.identifier=cinema-4d*'
        ' and data.application.version >= 23',
        handle_event
    )

    session.event_hub.subscribe(
        'topic=ftrack.connect.application.discover'
        ' and data.application.identifier=cinema-4d*'
        ' and data.application.version >= 23',
        handle_event
    )

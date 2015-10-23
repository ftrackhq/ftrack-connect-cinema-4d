# :coding: utf-8
# :copyright: Copyright (c) 2015 ftrack
import tempfile
import os

import c4d
import ftrack_api


def get_temporary_file_path(document_name):
    '''Return file path to *document_name* in temporary directory.'''
    temporary_directory = tempfile.mkdtemp(prefix='ftrack_connect')
    filePath = os.path.join(
        temporary_directory, document_name
    )
    return filePath


def export_c4d_document():
    document = c4d.documents.GetActiveDocument()
    document_name = document.GetDocumentName() or 'Untitled document'

    filePath = get_temporary_file_path(document_name)
    c4d.documents.SaveDocument(
        document,
        filePath,
        c4d.SAVEDOCUMENTFLAGS_AUTOSAVE,
        c4d.FORMAT_C4DEXPORT
    )
    return filePath


def _get_api_session():
    '''Return new ftrack_api session configure without plugins or events.'''
    return ftrack_api.Session(
        auto_connect_event_hub=False
    )


def publish():
    cinema_4d_document = export_c4d_document()

    session = _get_api_session()

    task_id = '9676bf8f-73e3-11e5-a4d9-3c0754289fd3'
    task = session.get('Task', task_id)
    shot = task['parent']

    asset_type = session.query('AssetType where short is "geo"').first()
    asset = session.create('Asset', {
        'parent': shot,
        'name': 'forest',
        'type': asset_type
    })
    status = session.query('Status where name is "Pending"').one()

    version = session.create('AssetVersion', {
        'asset': asset,
        'status': status,
        'comment': 'Added more leaves.',
        'task': task
    })

    component = version.create_component(cinema_4d_document, location='auto')
    session.commit()

# :coding: utf-8
# :copyright: Copyright (c) 2015 ftrack
import tempfile
import os
import uuid

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
    document_name = document.GetDocumentName() or 'untitled_document.c4d'
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
        auto_connect_event_hub=False,
        plugin_paths=[]
    )


def publish():
    cinema_4d_document = export_c4d_document()

    session = _get_api_session()

    task_id = '242e807a-6e7e-11e5-9cd2-3c0754289fd3'
    task = session.get('Task', task_id)
    shot = task['parent']

    asset_type = session.query('AssetType where short is "geo"').first()
    asset = session.create('Asset', {
        'parent': shot,
        'name': 'forest' + uuid.uuid4().hex[6:],
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
    print 'Completed'


if __name__=='__main__':
    publish()

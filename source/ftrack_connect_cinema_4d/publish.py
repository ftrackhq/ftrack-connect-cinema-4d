# :coding: utf-8
# :copyright: Copyright (c) 2015 ftrack

import tempfile
import os
import uuid
import logging

import c4d
import c4d.documents


logger = logging.getLogger('ftrack_connect_cinema_4d.publish')


def get_temporary_file_path(document_name):
    '''Return file path to *document_name* in temporary directory.'''
    temporary_directory = tempfile.mkdtemp(prefix='ftrack_connect')
    filePath = os.path.join(
        temporary_directory, document_name
    )
    return filePath


def get_document_name():
    '''Return document name.'''
    document = c4d.documents.GetActiveDocument()
    document_name = document.GetDocumentName() or 'Untitled document'
    (name, extension) = os.path.splitext(document_name)
    return name


def export_c4d_document():
    '''Export C4D document.'''
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


def publish(session, options):
    '''Publish a version based on *options*.'''
    logger.info(u'Publishing with options: {0}'.format(options))
    document_path = export_c4d_document()
    logger.info(u'Exported C4D document: {0!r}'.format(document_path))

    # Create new or get existing asset.
    asset = session.ensure('Asset', {
        'context_id': options['parent'],
        'type_id': options['type'],
        'name': options['name']
    })

    version = session.create('AssetVersion', {
        'asset': asset,
        'task_id': options.get('task', None),
        'comment': options.get('description', '')
    })

    # Commit before adding components to ensure structures dependent on
    # committed ancestors work as expected.
    session.commit()

    component = version.create_component(
        document_path, location='auto'
    )

    return version['id']

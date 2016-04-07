# :coding: utf-8
# :copyright: Copyright (c) 2015 ftrack
import tempfile
import os
import uuid

import c4d
import c4d.documents

import ftrack_connect_cinema_4d.session


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
    return document.GetDocumentName() or 'Untitled document'


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

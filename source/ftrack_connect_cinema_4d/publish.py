# :coding: utf-8
# :copyright: Copyright (c) 2015 ftrack

import tempfile
import os
import uuid
import logging

import c4d
import c4d.documents


logger = logging.getLogger('ftrack_connect_cinema_4d.publish')


class PublishError(Exception):
    '''Raise when unable to publish.'''
    pass


class SavePreviewImageError(Exception):
    '''Raise when unable to save a preview image.'''
    pass


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


def export_c4d_document(document):
    '''Export C4D document.'''
    document_name = document.GetDocumentName() or 'Untitled document'
    filePath = get_temporary_file_path(document_name)
    c4d.documents.SaveDocument(
        document,
        filePath,
        c4d.SAVEDOCUMENTFLAGS_AUTOSAVE,
        c4d.FORMAT_C4DEXPORT
    )
    return filePath


def render_preview_image(document):
    '''Render *document* as a preview image and return bitmap.

    Note: will not render correctly when called outside of the main thread.
    For example, as the callback in an ftrack event.
    '''
    render_data = document.GetActiveRenderData().GetData()
    render_data[c4d.RDATA_RENDERENGINE] = c4d.RDATA_RENDERENGINE_PREVIEWHARDWARE
    bitmap = c4d.bitmaps.BaseBitmap()
    bitmap.Init(
        x=int(render_data[c4d.RDATA_XRES]),
        y=int(render_data[c4d.RDATA_YRES]),
        depth=24
    )
    render_flags = (c4d.RENDERFLAGS_PREVIEWRENDER | c4d.RENDERFLAGS_DONTANIMATE)
    result = c4d.documents.RenderDocument(
        document,
        render_data,
        bitmap,
        render_flags
    )
    if result != c4d.RENDERRESULT_OK:
        raise SavePreviewImageError('Unable to get document preview bitmap.')

    return bitmap


def save_preview_image(document):
    '''Save preview image from *document* as temporary file and return file path.

    The image will be saved as a JPEG file.

    TODO: Handle situations when there is no document preview and render a 
    preview image using `render_preview_image`.
    '''
    if not document:
        raise SavePreviewImageError('Can not save image without document.')

    bitmap = document.GetDocPreviewBitmap()
    if not bitmap:
        raise SavePreviewImageError('Unable to get document preview bitmap.')

    document_name = get_document_name() + '.jpg'
    file_path = get_temporary_file_path(document_name)
    result = bitmap.Save(file_path, c4d.FILTER_JPG)
    if result != True:
        raise SavePreviewImageError(
            u'Failed to save bitmap (result code: {0!r})'.format(result)
        )
    return file_path


def publish(session, options):
    '''Publish a version based on *options*.'''
    logger.info(u'Publishing with options: {0}'.format(options))

    try:
        active_document = c4d.documents.GetActiveDocument()
        document = active_document
        if options.get('selection_only', False):
            logger.info(u'Isolating selected objects into new document')
            selected_objects = document.GetActiveObjects(
                c4d.GETACTIVEOBJECTFLAGS_0
            )
            if not len(selected_objects):
                raise PublishError('No objects selected')

            document = c4d.documents.IsolateObjects(document, selected_objects)

        document_path = export_c4d_document(document)
        logger.info(u'Exported C4D document: {0!r}'.format(document_path))

        thumbnail_path = None
        try:
            # TODO: Use the new `document` instead of `active_document` when
            # grabbing the preview image so that when publishing only select
            # objects a correct preview is generated.
            # 
            # This requires that publish is executed in the main thread so
            # that render_preview_image renders a non-black image.
            # 
            thumbnail_path = save_preview_image(active_document)
        except Exception:
            logger.exception('Failed to save thumbnail.')

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
        if thumbnail_path:
            version.create_thumbnail(thumbnail_path)

        # Commit before adding components to ensure structures dependent on
        # committed ancestors work as expected.
        session.commit()

        component = version.create_component(
            document_path,
            data=dict(name='cinema-4d-document', file_type='.c4d'),
            location='auto'
        )

    except Exception:
        # On any exception, rollback and re-raise error.
        logger.warning('Failed to publish document, rolling back session')
        session.rollback()
        raise

    return version['id']

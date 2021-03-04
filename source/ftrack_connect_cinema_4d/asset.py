# :coding: utf-8
# :copyright: Copyright (c) 2015 ftrack

import tempfile
import os
import uuid
import logging

import c4d
import c4d.documents

import ftrack_connect_cinema_4d.plugin.component_tag

logger = logging.getLogger('ftrack_connect_cinema_4d.asset')


def encode_unicode(value):
    return value


def get_importable_components(session, version_id):
    '''Return importable components for *version_id*.'''
    logger.info(u'Get importable components for {0!r}'.format(version_id))
    attributes = [
        'id',
        'name',
        'file_type',
        'size',
        'version',
        'version.asset_id',
        'version.link',
        'component_locations.location',
        'component_locations.resource_identifier'
    ]
    components = session.query(
        'select {0} from Component '
        'where version_id is "{1}"'.format(','.join(attributes), version_id)
    )

    result = []
    for component in components:
        caption = u'{0}{1}'.format(component['name'], component['file_type'])
        disabled = False
        file_path = None
        try:
            location = session.pick_location(component)
            assert location is not None
            file_path = location.get_filesystem_path(component)
        except Exception:
            caption += ' (Unavailable)'
            disabled = True
        result.append(
            dict(
                caption=caption,
                disabled=disabled,
                data=dict(
                    file_path=file_path,
                    component_id=component['id'],
                    version_id=component['version']['id'],
                    asset_id=component['version']['asset_id']
                )
            ) 
        )

    logger.info(u'Retrieved result: {0}'.format(result))
    return result


def set_paramaters(scene_object, component_id=None, asset_id=None, version_id=None):
    '''Set parameters on *scene_object*'''
    component_tag = scene_object.GetTag(
        ftrack_connect_cinema_4d.plugin.component_tag.PLUGIN_ID
    )
    if not component_tag:
        logger.info('Creating component tag')
        component_tag = c4d.BaseTag(
            ftrack_connect_cinema_4d.plugin.component_tag.PLUGIN_ID
        )
        scene_object.InsertTag(component_tag)
    else:
        logger.info('Reusing component tag')
    
    logger.info(
        'Setting parameters: {0}, {1}, {2}'.format(
            component_id, version_id, asset_id
        )
    )

    component_tag.SetParameter(
        c4d.FTRACK_COMPONENT_ID,
        encode_unicode(component_id),
        c4d.DESCFLAGS_SET_USERINTERACTION
    )
    component_tag.SetParameter(
        c4d.FTRACK_VERSION_ID,
        encode_unicode(version_id),
        c4d.DESCFLAGS_SET_USERINTERACTION
    )
    component_tag.SetParameter(
        c4d.FTRACK_ASSET_ID,
        encode_unicode(asset_id),
        c4d.DESCFLAGS_SET_USERINTERACTION
    )


def import_object_from_file_path(file_path, component_id=None, asset_id=None, version_id=None):
    logger.info(u'Importing file path: {0}'.format(file_path))
    document = c4d.documents.GetActiveDocument()
    logger.info(u'Active document: {0}'.format(document))
    if not document:
        return False

    xref_object = c4d.BaseObject(c4d.Oxref)
    logger.info(u'Created XRef Object: {0}'.format(xref_object))
    if not xref_object:
        return False

    document.InsertObject(xref_object)
    logger.info(u'Inserted xref object: {0}'.format(xref_object))

    xref_object.SetParameter(
        c4d.ID_CA_XREF_FILE,
        encode_unicode(file_path),
        c4d.DESCFLAGS_SET_USERINTERACTION
    )
    logger.info(
        u'Set xref parameter - {0}: {1}'.format(
            c4d.ID_CA_XREF_FILE, encode_unicode(file_path)
        )
    )

    logger.info(u'Setting asset parameters')
    set_paramaters(xref_object, component_id=component_id, asset_id=asset_id, version_id=version_id)
    c4d.EventAdd()
    return True


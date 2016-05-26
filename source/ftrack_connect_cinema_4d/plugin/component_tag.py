# :coding: utf-8
# :copyright: Copyright (c) 2015 ftrack

import c4d

# TODO: Replace this ID
PLUGIN_ID = 1230001


class ComponentTag(c4d.plugins.TagData):
    '''Tag plugin to mark the object as an ftrack component.'''

    isObjectActive = False

    def Init(self, node):
        node[c4d.FTRACK_COMPONENT_ID] = '2462518f-6e7e-11e5-9f8a-3c0754289fd3'
        return True

    def Execute(self, tag, doc, op, bt, priority, flags):
        print 'Execute', tag[c4d.FTRACK_COMPONENT_ID]
        return True

    def Message(self, node, type, data):
        return True

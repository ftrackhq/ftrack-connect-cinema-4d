# :coding: utf-8
# :copyright: Copyright (c) 2015 ftrack

import c4d

#: ftrack component tag plugin id.
PLUGIN_ID = 1037465


class ComponentTag(c4d.plugins.TagData):
    '''Tag plugin to mark the object as an ftrack component.'''

    def Init(self, node):
        return True

    def Execute(self, tag, doc, op, bt, priority, flags):
        return True

    def Message(self, node, type, data):
        return True

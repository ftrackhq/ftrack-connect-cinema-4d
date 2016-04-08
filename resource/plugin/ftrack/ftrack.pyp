# :coding: utf-8
# :copyright: Copyright (c) 2015 ftrack
import os
import c4d

import sys
sys.path.append(
    os.path.dirname(os.path.realpath(__file__))
)
sys.path.append(
    os.path.join(os.path.dirname(os.path.realpath(__file__)), 'dependencies')
)

import ftrack_connect_cinema_4d.plugin


RESOURCE_DIRECTORY = os.path.join(
    os.path.dirname(os.path.realpath(__file__)), 'res'
)


def create_ftrack_menu():
    '''Create custom ftrack menu.'''
    main_menu = c4d.gui.GetMenuResource('M_EDITOR')
    menu = c4d.BaseContainer()
    menu.InsData(c4d.MENURESOURCE_SUBTITLE, 'ftrack')

    for plugin_id in (
        ftrack_connect_cinema_4d.plugin.spark_command.PLUGIN_ID,
    ):
        pluginCommandString = 'PLUGIN_CMD_'
        pluginIdString = str(plugin_id)
        pluginCommandString = pluginCommandString + pluginIdString
        menu.InsData(c4d.MENURESOURCE_COMMAND, pluginCommandString)

    main_menu.InsData(c4d.MENURESOURCE_SUBMENU, menu)


def PluginMessage(id, data):
    '''Listen for C4DPL_BUILDMENU message and construct custom ftrack menu.'''
    if id == c4d.C4DPL_BUILDMENU:
        create_ftrack_menu()
        return True
    return False


def register_plugins():
    '''Register ftrack plugins.'''
    icon = c4d.bitmaps.BaseBitmap()
    icon.InitWith(os.path.join(
        RESOURCE_DIRECTORY, 'ftrack.tif'
    ))

    c4d.plugins.RegisterCommandPlugin(
        id=ftrack_connect_cinema_4d.plugin.spark_command.PLUGIN_ID,
        str='ftrack',
        info=0,
        help='ftrack',
        icon=icon,
        dat=ftrack_connect_cinema_4d.plugin.SparkCommand()
    )

if __name__ == '__main__':
    register_plugins()

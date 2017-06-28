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

import ftrack_connect_cinema_4d.configure_logging
import ftrack_connect_cinema_4d.plugin
import ftrack_connect_cinema_4d.plugin.component_tag
import ftrack_connect_cinema_4d.plugin.ftrack_message_data


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
    ftrack_connect_cinema_4d.configure_logging.configure_logging(
        'ftrack_connect_cinema_4d'
    )

    icon = c4d.bitmaps.BaseBitmap()
    icon.InitWith(os.path.join(
        RESOURCE_DIRECTORY, 'ftrack.tif'
    ))

    c4d.plugins.RegisterTagPlugin(
        id=ftrack_connect_cinema_4d.plugin.component_tag.PLUGIN_ID,
        str='ftrack Asset',
        info=c4d.TAG_EXPRESSION | c4d.TAG_VISIBLE,
        g=ftrack_connect_cinema_4d.plugin.ComponentTag,
        description='Tftrackasset',
        icon=icon
    )

    c4d.plugins.RegisterCommandPlugin(
        id=ftrack_connect_cinema_4d.plugin.spark_command.PLUGIN_ID,
        str='ftrack',
        info=0,
        help='ftrack',
        icon=icon,
        dat=ftrack_connect_cinema_4d.plugin.SparkCommand()
    )

    c4d.plugins.RegisterMessagePlugin(
        id=ftrack_connect_cinema_4d.plugin.ftrack_message_data.PLUGIN_ID,
        str='ftrack message data',
        info=0,
        dat=ftrack_connect_cinema_4d.plugin.FtrackMessageData()
    )

if __name__ == '__main__':
    register_plugins()

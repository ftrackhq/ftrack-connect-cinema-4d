# :coding: utf-8
# :copyright: Copyright (c) 2015 ftrack
import os

import c4d

import ftrack_connect_cinema_4d.publish

#: TODO: Replace with correct ID.
PLUGIN_ID = 2346589869

RESOURCE_DIRECTORY = os.path.join(
    os.path.dirname(os.path.realpath(__file__)), 'res'
)


class Publisher(c4d.plugins.CommandData):
    def Execute(self, doc):
        print 'Executing publisher'
        ftrack_connect_cinema_4d.publish.publish()


def create_ftrack_menu():
    mainMenu = c4d.gui.GetMenuResource("M_EDITOR")
    menu = c4d.BaseContainer()
    menu.InsData(c4d.MENURESOURCE_SUBTITLE, "ftrack")

    # create command string
    pluginCommandString = "PLUGIN_CMD_"
    pluginIdString = str(PLUGIN_ID)
    pluginCommandString = pluginCommandString + pluginIdString
    menu.InsData(c4d.MENURESOURCE_COMMAND, pluginCommandString)
    mainMenu.InsData(c4d.MENURESOURCE_SUBMENU, menu)


def PluginMessage(id, data):

    # catch C4DPL_BUILDMENU to build custom menus
    if id==c4d.C4DPL_BUILDMENU:
        create_ftrack_menu()
        return True

    return False

def main():
    icon = c4d.bitmaps.BaseBitmap()
    icon.InitWith(os.path.join(
        RESOURCE_DIRECTORY, 'icon.tif'
    ))

    c4d.plugins.RegisterCommandPlugin(
        id=PLUGIN_ID,
        str="ftrack - Publish",
        info=0,
        help='Publish to ftrack',
        icon=icon,
        dat=Publisher()
    )

if __name__ == "__main__":
    main()

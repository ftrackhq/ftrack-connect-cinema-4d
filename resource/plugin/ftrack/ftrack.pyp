# :coding: utf-8
# :copyright: Copyright (c) 2015 ftrack
import os

import c4d
from c4d import bitmaps, plugins, utils, gui

import ftrack_connect_cinema_4d.publish

#: TODO: Replace with correct ID.
PUBLISH_PLUGIN_ID = 23465898
ASSET_PLUGIN_ID = 1028278
INFO_PLUGIN_ID = 234569


RESOURCE_DIRECTORY = os.path.join(
    os.path.dirname(os.path.realpath(__file__)), 'res'
)


class Publisher(c4d.plugins.CommandData):
    def Execute(self, doc):
        print 'Executing publisher'
        ftrack_connect_cinema_4d.publish.publish()


class FtrackAsset(plugins.TagData):
    """Look at Camera"""
    isObjectActive = False
    
    def Init(self, node):
        node[c4d.FTRACK_ASSET_ID] = '2462518f-6e7e-11e5-9f8a-3c0754289fd3'
        return True

    def Execute(self, tag, doc, op, bt, priority, flags):
        print 'Execute', tag[c4d.FTRACK_ASSET_ID]

        isActiveBit = op.GetBit(c4d.BIT_ACTIVE)
        if self.isObjectActive != isActiveBit:
            c4d.SpecialEventAdd(INFO_PLUGIN_ID)

        self.isObjectActive = isActiveBit

        return True

    def Message(self, node, type, data):
        if type == c4d.MSG_DESCRIPTION_COMMAND:
            if data['id'][0].id == c4d.THE_BUTTON:
                print 'Button pressed', c4d.THE_BUTTON
        return True


class InfoDialog(gui.GeDialog):
    url = None
    htmlview = None

    def __init__(self):
        self.url = "https://ftrack-test.ftrackapp.com/widget?view=app_info&itemId=launcher&theme=dark&auth_token=7e1ae10a-7966-11e5-9dcb-42010af0eaa2&entityId=3748c54c-e2ce-11e3-ac7b-040103338201&entityType=task"

    def setEntityUrl(self, entityType, entityId):
        self.setUrl(
            "http://localhost:8090/widget?view=app_info&itemId=launcher&theme=dark&auth_token={0}&entityId={1}&entityType={2}".format(
                '99e7315e-7982-11e5-8ab4-3c0754289fd3',
                entityId,
                entityType
            )
        )

    def setUrl(self, url):
        self.url = url
        if self.htmlview:
            self.htmlview.SetUrl(url, c4d.URL_ENCODING_UTF16)

    def CreateLayout(self):
        self.SetTitle('Info')
        self.GroupBegin(id=0, flags=c4d.BFH_SCALEFIT|c4d.BFV_SCALEFIT, title="", rows=1, cols=1, groupflags=c4d.BORDER_GROUP_IN)
        self.GroupBorderSpace(5, 5, 5, 5)
 
        settings = c4d.BaseContainer()
        self.htmlview = self.AddCustomGui(id=1001, pluginid=c4d.CUSTOMGUI_HTMLVIEWER, name="", flags=c4d.BFH_SCALEFIT|c4d.BFV_SCALEFIT, minw=200, minh=200, customdata=settings)
        self.htmlview.SetUrl(self.url, c4d.URL_ENCODING_UTF16)
        self.GroupEnd()

        return True

    def CoreMessage(self, id, message):
        if id == INFO_PLUGIN_ID:
            print 'Selection changed'

            document = c4d.documents.GetActiveDocument()
            objects = document.GetActiveObjects(c4d.GETACTIVEOBJECTFLAGS_0)
            
            asset_id = None
            for item in objects:
                tag = item.GetTag(ASSET_PLUGIN_ID)
                if tag:
                    asset_id = tag[c4d.FTRACK_ASSET_ID]
                    break
                    #TODO: handle multiple
                    #
            
            if asset_id:
                self.setEntityUrl('task', asset_id)
            else:
                self.setUrl('about:blank')

        return True


class InfoWebView(plugins.CommandData):
    dialog = None

    def Execute(self, doc):
        """Just create the dialog when the user clicked on the entry
        in the plugins menu to open it."""
        if self.dialog is None:
           self.dialog = InfoDialog()

        return self.dialog.Open(dlgtype=c4d.DLG_TYPE_ASYNC, pluginid=INFO_PLUGIN_ID, defaulth=400, defaultw=400)

    def RestoreLayout(self, sec_ref):
        """Same for this method. Just allocate it when the dialog
        is needed"""
        if self.dialog is None:
           self.dialog = InfoDialog()

        return self.dialog.Restore(pluginid=INFO_PLUGIN_ID, secret=sec_ref)



def create_ftrack_menu():
    mainMenu = c4d.gui.GetMenuResource("M_EDITOR")
    menu = c4d.BaseContainer()
    menu.InsData(c4d.MENURESOURCE_SUBTITLE, "ftrack")

    # create command string
    pluginCommandString = "PLUGIN_CMD_"
    pluginIdString = str(PUBLISH_PLUGIN_ID)
    pluginCommandString = pluginCommandString + pluginIdString
    menu.InsData(c4d.MENURESOURCE_COMMAND, pluginCommandString)

    pluginCommandString = "PLUGIN_CMD_"
    pluginIdString = str(INFO_PLUGIN_ID)
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
        id=PUBLISH_PLUGIN_ID,
        str="ftrack Publish",
        info=0,
        help='Publish to ftrack',
        icon=icon,
        dat=Publisher()
    )


    c4d.plugins.RegisterTagPlugin(
        id=ASSET_PLUGIN_ID,
        str="ftrack Asset",
        info=c4d.TAG_EXPRESSION | c4d.TAG_VISIBLE,
        g=FtrackAsset,
        description="Tftrackasset",
        icon=None
    )

    c4d.plugins.RegisterCommandPlugin(
        id=INFO_PLUGIN_ID, str="ftrack Info",
        help="Show ftrack info about the selected object.",
        info=0,
        dat=InfoWebView(),
        icon=None
    )

if __name__ == "__main__":
    main()

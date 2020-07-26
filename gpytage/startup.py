#!/usr/bin/env python
#
# GPytage startup.py module
#
############################################################################
#    Copyright (C) 2008-20010 by Kenneth Prugh                             #
#    ken69267@gmail.com                                                    #
#                                                                          #
#    This program is free software; you can redistribute it and#or modify  #
#    it under the terms of the GNU General Public License as published by  #
#    the Free Software Foundation under version 2 of the license.          #
#                                                                          #
#    This program is distributed in the hope that it will be useful,       #
#    but WITHOUT ANY WARRANTY; without even the implied warranty of        #
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the         #
#    GNU General Public License for more details.                          #
#                                                                          #
#    You should have received a copy of the GNU General Public License     #
#    along with this program; if not, write to the                         #
#    Free Software Foundation, Inc.,                                       #
#    59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.             #
############################################################################

import gi
gi.require_version("Gtk", "3.0") # make sure we have the right version
gi.require_version('GdkPixbuf', '2.0')
from gi.repository import GdkPixbuf
from gi.repository import Gtk

from gpytage.leftpanel import expandRows, collapseRows
from gpytage.leftpanel import scroll as lScroll
from gpytage.rightpanel import scroll as rScroll
from gpytage import config
from gpytage.window import window, unsavedDialog, getTitleState
from gpytage.version import version
from gpytage.datastore import folderModel, config_files, initTreeModel, initData
from gpytage.fileOperations import saveModifiedFile, saveModifiedFiles, revertSelected, revertAllModified
from gpytage.newFile import newFile
from gpytage.deleteFile import deleteFile
from gpytage.rename import renameFile
from .rightpanel import insertRow, deleteRow, commentRow, uncommentRow, toggleComment

#set global defaults
DATA_PATH = "/usr/share/gpytage/"
PIXMAPS = "/usr/share/gpytage/pixmaps/"
GLADE_PATH = "/usr/share/gpytage/glade/"

def local():
    """ set global defaults for running locally """

    global DATA_PATH, PIXMAPS, GLADE_PATH
    DATA_PATH =  os.path.dirname(os.path.abspath(__file__))
    print(DATA_PATH)
    PIXMAPS = os.path.join(DATA_PATH , "pixmaps/")
    GLADE_PATH = os.path.join(DATA_PATH, "glade/")

import os.path
location = os.path.abspath(__file__)
if "site-packages" not in location:
    local()

# Somehow, this line breaks deleteFile.py's shutil.rmtree
#del os.path

class gpytagemain:
    def __init__(self):
        self.window = window

        try: #load icons as pixbufs and set as default icon
            print(" gpytagemain: PIXMAPS =", PIXMAPS)
            self.i16 = GdkPixbuf.Pixbuf.new_from_file(PIXMAPS + "gpytage-16x16.png")
            self.i24 = GdkPixbuf.Pixbuf.new_from_file(PIXMAPS + "gpytage-24x24.png")
            self.i32 = GdkPixbuf.Pixbuf.new_from_file(PIXMAPS + "gpytage-32x32.png")
            self.i48 = GdkPixbuf.Pixbuf.new_from_file(PIXMAPS + "gpytage-48x48.png")
            self.i64 = GdkPixbuf.Pixbuf.new_from_file(PIXMAPS + "gpytage-64x64.png")
            self.i128 = GdkPixbuf.Pixbuf.new_from_file(PIXMAPS + "gpytage-128x128.png")
            Gtk.window_set_default_icon_list(self.i16, self.i24, self.i32, self.i48, self.i64, self.i128)
        except:
            print("GPytage could not find its icons!")

        self.window.set_default_size(800, 500)

        self.datastore = folderModel
        self.files = config_files

        initData()
        initTreeModel()

        self.uimanager = Gtk.UIManager()
        self.accelgroup = self.uimanager.get_accel_group()
        self.actiongroup = Gtk.ActionGroup('GPytage')
        self.ui = '''
        <ui>
            <menubar name="MenuBar">
                <menu action="File">
                    <menuitem action="New"/>
                    <separator/>
                    <menuitem action="Save"/>
                    <menuitem action="Save All"/>
                    <menuitem action="Revert"/>
                    <menuitem action="Revert All"/>
                    <separator/>
                    <menuitem action="Delete File/Folder"/>
                    <menuitem action="Rename"/>
                    <separator/>
                    <menuitem action="Quit"/>
                </menu>
                <menu action="Edit">
                    <menuitem action="Add Package"/>
                    <menuitem action="Remove Package"/>
                    <menuitem action="Toggle Comment"/>
                </menu>
                <menu action="View">
                    <menuitem action="Expand All"/>
                    <menuitem action="Collapse All"/>
                </menu>
                <menu action="Help">
                    <menuitem action="About"/>
                </menu>
            </menubar>
            <toolbar name="ToolBar">
                <toolitem action="New"/>
                <toolitem action="Save"/>
                <toolitem action="Revert"/>
                <toolitem action="Add Package"/>
                <toolitem action="Remove Package"/>
                <toolitem action="Comment"/>
                <toolitem action="Uncomment"/>
            </toolbar>
        </ui>'''

        #This controls the MenuBar and the ToolBar
        self.actiongroup.add_actions([
            ('File', None, '_File'),
            ('New', Gtk.STOCK_NEW, '_New File', '<Control>n', 'New file', newFile),
            ('Save', Gtk.STOCK_SAVE, '_Save', '<Control>s', 'Save changes',
                saveModifiedFile),
            ('Save All', Gtk.STOCK_SAVE_AS, 'Save _All', None, 'Save all changes', saveModifiedFiles),
            ('Revert', Gtk.STOCK_REVERT_TO_SAVED, '_Revert', None, 'Revert changes', revertSelected),
            ('Revert All', Gtk.STOCK_REVERT_TO_SAVED, 'Re_vert All', None, 'Revert all changes', revertAllModified),
            ('Quit', Gtk.STOCK_QUIT, '_Quit', None, 'Quit GPytage', self.destroy),

            ('Edit', None, '_Edit'),
            ('Add Package', Gtk.STOCK_ADD, '_Add Package', '<Control>e', 'Add a package', insertRow),
            ('Remove Package', Gtk.STOCK_REMOVE, '_Remove Package', '<Control>d', "Remove a package", deleteRow),
            ('Delete File/Folder', Gtk.STOCK_DELETE, '_Delete File/Folder', None, 'Delete currently selected file or folder', deleteFile),
            ('Rename', Gtk.STOCK_SAVE_AS, '_Rename', None, 'Rename file', renameFile),
            ('Comment', Gtk.STOCK_INDENT, '_Comment', None, "Comment a package", commentRow),
            ('Uncomment', Gtk.STOCK_UNINDENT, '_Uncomment', None, "Uncomment a package", uncommentRow),
            ('Toggle Comment', Gtk.STOCK_CONVERT, '_Toggle Comment', '<Control><Shift>c', "Toggle comment packages", toggleComment),

            ('View', None, '_View'),
            ('Expand All', None, '_Expand All', '<Control>slash', 'Expand Rows', expandRows),
            ('Collapse All', None, '_Collapse All', '<Control>backslash', 'Collapse Rows', collapseRows),
            ('Help',None,'_Help'),
            ('About', Gtk.STOCK_ABOUT, '_About', None, 'About GPytage', self.about)
        ])

        #Add the UI XML
        self.uimanager.insert_action_group(self.actiongroup, 0)
        self.uimanager.add_ui_from_string(self.ui)

        #Menubar
        self.menubar = self.uimanager.get_widget('/MenuBar')
        self.toolbar = self.uimanager.get_widget('/ToolBar')
        self.vbox = Gtk.VBox() #the master Widget
        self.vbox.pack_start(self.menubar, False, False, 0)
        self.vbox.pack_start(self.toolbar, False, False, 0)

        #allow the program to quit
        self.window.connect("destroy", self.destroy)
        self.window.connect("delete_event", self.delete_event)

        #Show Widgets
        self.pane = Gtk.Paned(orientation=Gtk.Orientation.HORIZONTAL)
        self.pane.pack1(lScroll, True, True)
        self.pane.pack2(rScroll, True, True)
        self.pane.set_position(200)
        self.vbox.pack_start(self.pane, True, True, 0)
        self.window.add_accel_group(self.accelgroup)
        self.window.add(self.vbox)
        self.window.show_all()

    def destroy(self, widget, data=None):
        state = getTitleState()
        print("STATE IS: ")
        print(state)
        if state is True: #There are edited files
            status, uD = unsavedDialog()
            if status == -8:   #YES
                Gtk.main_quit()
            else:              #NO and other unhandled signals
                uD.hide()
        else:
            Gtk.main_quit()

    def delete_event(self, widget, event, data=None):
        self.destroy(widget)
        return True

    #Menu Functions
    def about(self, *args):
        aboutw = Gtk.AboutDialog()
        aboutw.set_name('GPytage')
        aboutw.set_copyright('Copyright 2008-2009, GPL2')
        aboutw.set_authors(["Kenneth 'ken69267' Prugh",
            "\nWith patches contributed by Brian Dolbec <dol-sen>\nand Josh 'nightmorph' Saddler. \n" +
            "\nWith special thanks to the Gentoo \ndevelopers and community. \n\n" +
            "Licensed under the GPL-2"]) #Fix wording? :)
        f=open(config.PORTDIR + '/licenses/GPL-2')
        gpl2 = f.read()
        f.close
        aboutw.set_license(gpl2)
        aboutw.set_wrap_license(True)
        aboutw.set_version(version)
        aboutw.set_website('https://gna.org/projects/gpytage/')
        try:
            aboutw.set_logo(self.i128)
        except:
            print("ABOUT(): Logo could not be set")
        aboutw.run()
        aboutw.hide()

    def TODO(self):
        pass

    def main(self):
        Gtk.main()

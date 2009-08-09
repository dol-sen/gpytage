#!/usr/bin/env python
#
# GPytage startup.py module
#
############################################################################
#    Copyright (C) 2008-2009 by Kenneth Prugh                              #
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

import pygtk; pygtk.require("2.0")
import gtk

from gpytage import leftpanel, rightpanel
from gpytage import config
from gpytage.window import window, unsavedDialog, setTitleEdited, getTitleState
from gpytage.version import version
from gpytage.datastore import folderModel, config_files, initTreeModel, initData, reload
from rightpanel import insertRow, deleteRow

#set global defaults
DATA_PATH = "/usr/share/gpytage/"
PIXMAPS = "/usr/share/gpytage/pixmaps/"
GLADE_PATH = "/usr/share/gpytage/glade/"

def local():
    """ set global defaults for running locally """
    from os import getcwd
    global DATA_PATH, PIXMAPS, GLADE_PATH
    DATA_PATH = getcwd() + "/../"
    print DATA_PATH
    PIXMAPS = DATA_PATH + "gpytage/pixmaps/"
    GLADE_PATH = DATA_PATH + "gpytage/glade/"
    

class gpytagemain:
    def __init__(self):
        self.window = window
        
        try: #load icons as pixbufs and set as default icon
            print PIXMAPS
            self.i16 = gtk.gdk.pixbuf_new_from_file(PIXMAPS + "gpytage-16x16.png")
            self.i24 = gtk.gdk.pixbuf_new_from_file(PIXMAPS + "gpytage-24x24.png")
            self.i32 = gtk.gdk.pixbuf_new_from_file(PIXMAPS + "gpytage-32x32.png")
            self.i48 = gtk.gdk.pixbuf_new_from_file(PIXMAPS + "gpytage-48x48.png")
            self.i64 = gtk.gdk.pixbuf_new_from_file(PIXMAPS + "gpytage-64x64.png")
            self.i128 = gtk.gdk.pixbuf_new_from_file(PIXMAPS + "gpytage-128x128.png")
            gtk.window_set_default_icon_list(self.i16, self.i24, self.i32, self.i48, self.i64, self.i128)
        except:
            print "GPytage could not find its icons!"
        
        self.window.set_default_size(800, 500)
        
        self.datastore = folderModel
        self.files = config_files
        
        initData()
        initTreeModel()

        self.uimanager = gtk.UIManager()
        self.accelgroup = self.uimanager.get_accel_group()
        self.actiongroup = gtk.ActionGroup('GPytage')
        self.ui = '''
        <ui>
            <menubar name="MenuBar">
                <menu action="File">
                    <menuitem action="New"/>
                    <separator/>
                    <menuitem action="Save"/>
                    <menuitem action="Revert"/>
                    <separator/>
                    <menuitem action="Quit"/>
                </menu>
                <menu action="Edit">
                    <menuitem action="Add Package"/>
                    <menuitem action="Remove Package"/>
                    <separator/>
                    <menuitem action="Delete"/>
                    <menuitem action="Split"/>
                    <menuitem action="Rename"/>
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
            ('New', gtk.STOCK_NEW, '_New Subfile', '<Control>n', 'New file', self.TODO),
            ('Save', gtk.STOCK_SAVE, '_Save', '<Control>s', 'Save changes', self.TODO),
            ('Revert', gtk.STOCK_REVERT_TO_SAVED, '_Revert', None, 'Revert changes', self.reload),
            ('Quit', gtk.STOCK_QUIT, '_Quit', None, 'Quit GPytage', self.destroy),
            
            ('Edit', None, '_Edit'),
            ('Add Package', gtk.STOCK_ADD, '_Add Package', '<Control>Plus', 'Add a package', insertRow),
            ('Remove Package', gtk.STOCK_REMOVE, '_Remove Package',    '<Control>-', "Remove a package", deleteRow),
            ('Delete', gtk.STOCK_DELETE, '_Delete subfile', None, 'Delete file', self.TODO),
            ('Split', gtk.STOCK_CONVERT, '_Convert file->subfile', None, 'Convert file', self.TODO),
            ('Rename', gtk.STOCK_SAVE_AS, '_Rename subfile', None, 'Rename file', self.TODO),
            ('Comment', gtk.STOCK_INDENT, '_Comment', '<Control>period', "Comment a package", self.TODO),
            ('Uncomment', gtk.STOCK_UNINDENT, '_Uncomment', '<Control>comma', "Uncomment a package", self.TODO),
             
            ('View', None, '_View'),
            ('Expand All', None, '_Expand All', '<Control>slash', 'Expand Rows', self.TODO),
            ('Collapse All', None, '_Collapse All', '<Control>backslash', 'Collapse Rows', self.TODO), 
            ('Help',None,'_Help'),
            ('About', gtk.STOCK_ABOUT, '_About', None, 'About GPytage', self.about)
        ])

        #Add the UI XML
        self.uimanager.insert_action_group(self.actiongroup, 0)
        self.uimanager.add_ui_from_string(self.ui)

        #Menubar
        self.menubar = self.uimanager.get_widget('/MenuBar')
        self.toolbar = self.uimanager.get_widget('/ToolBar')
        self.vbox = gtk.VBox() #the master Widget
        self.vbox.pack_start(self.menubar, False)
        self.vbox.pack_start(self.toolbar, False)
        
        #allow the program to quit
        self.window.connect("destroy", self.destroy)
        self.window.connect("delete_event", self.delete_event)

        #Show Widgets
        self.pane = gtk.HPaned()
        self.pane.pack1(leftpanel.scroll, True, True)
        self.pane.pack2(rightpanel.scroll, True, True)
        self.pane.set_position(200)
        self.vbox.pack_start(self.pane)
        self.window.add_accel_group(self.accelgroup)
        self.window.add(self.vbox)
        self.window.show_all()

    def destroy(self, widget, data=None):
        if getTitleState is False:
            status, uD = unsavedDialog()
            if status == -8:   #YES
                gtk.main_quit()
            elif status == 1:  #SAVE
                self.save()
                gtk.main_quit()
            else:              #NO and other unhandled signals
                uD.hide()
        else:
            gtk.main_quit()

    def delete_event(self, widget, event, data=None):
        self.destroy(widget)
        return True

    #Menu Functions
    def about(self, *args):
        aboutw = gtk.AboutDialog()
        aboutw.set_name('GPytage')
        aboutw.set_copyright('Copyright 2008-2009, GPL2')
        aboutw.set_authors(["Kenneth 'ken69267' Prugh", "\nWith patches contributed by Brian Dolbec <dol-sen>\nand Josh 'nightmorph' Saddler. \n\nWith special thanks to the Gentoo \ndevelopers and community. \n\nLicensed under the GPL-2"]) #Fix wording? :)
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
            print "ABOUT(): Logo could not be set"
        aboutw.run()
        aboutw.hide()
    
    def reload(self, *args):
        """ Call datastore.reload() """
        reload()

#===============================================================================
#    def expand(self, *args):
#        leftpanel.leftview.expand_all()
# 
#    def collapse(self, *args):
#        leftpanel.leftview.collapse_all()
#            
# #===============================================================================
# #    def save(self, *args):
# #        save.SaveFile().saveModified()
# #===============================================================================
# 
#    def new(self, *args):
#        new(self.window, GLADE_PATH)
# 
#    def convert(self, *args):
#        convert(self.window, GLADE_PATH)
# 
#    def rename(self, *args):
#        rename().renameDialog(self.window, GLADE_PATH)
# 
#    def deleteFile(self, *args):
#        delete(self.window, GLADE_PATH)
# 
#    def comment(self, *args):
#        rightpanel.commentRow(self.window)
# 
#    def uncomment(self, *args):
#        rightpanel.uncommentRow(self.window)
#===============================================================================

    def TODO(self):
        pass

    def main(self):
        gtk.main()

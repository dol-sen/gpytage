#!/usr/bin/env python
#
############################################################################
#    Copyright (C) 2011 by Kenneth Prugh                                   #
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

import gtk

class UIbar(object):
    def __init__(self):
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
            ('New', gtk.STOCK_NEW, '_New File', '<Control>n', 'New file', todo),
            ('Save', gtk.STOCK_SAVE, '_Save', '<Control>s', 'Save changes',
                todo),
            ('Save All', gtk.STOCK_SAVE_AS, 'Save _All', None, 'Save all changes', todo),
            ('Revert', gtk.STOCK_REVERT_TO_SAVED, '_Revert', None, 'Revert changes', todo),
            ('Revert All', gtk.STOCK_REVERT_TO_SAVED, 'Re_vert All', None,
                'Revert all changes', todo),
            ('Quit', gtk.STOCK_QUIT, '_Quit', None, 'Quit GPytage', todo),
            
            ('Edit', None, '_Edit'),
            ('Add Package', gtk.STOCK_ADD, '_Add Package', '<Control>e', 'Add a package', todo),
            ('Remove Package', gtk.STOCK_REMOVE, '_Remove Package',
                '<Control>d', "Remove a package", todo),
            ('Delete File/Folder', gtk.STOCK_DELETE, '_Delete File/Folder',
                None, 'Delete currently selected file or folder', todo),
            ('Rename', gtk.STOCK_SAVE_AS, '_Rename', None, 'Rename file', todo),
            ('Comment', gtk.STOCK_INDENT, '_Comment', None, "Comment a package",
                todo),
            ('Uncomment', gtk.STOCK_UNINDENT, '_Uncomment', None, "Uncomment a package", todo),
            ('Toggle Comment', gtk.STOCK_CONVERT, '_Toggle Comment',
                '<Control><Shift>c', "Toggle comment packages", todo),

            ('View', None, '_View'),
            ('Expand All', None, '_Expand All', '<Control>slash', 'Expand Rows',
                todo),
            ('Collapse All', None, '_Collapse All', '<Control>backslash',
                'Collapse Rows', todo), 
            ('Help',None,'_Help'),
            ('About', gtk.STOCK_ABOUT, '_About', None, 'About GPytage', todo)
        ])

        #Add the UI XML
        self.uimanager.insert_action_group(self.actiongroup, 0)
        self.uimanager.add_ui_from_string(self.ui)

        #Menubar
        self.menubar = self.uimanager.get_widget('/MenuBar')
        self.toolbar = self.uimanager.get_widget('/ToolBar')

    def getMenuBar(self):
        return self.menubar

    def getToolBar(self):
        return self.toolbar

def todo(*args):
    pass

#!/usr/bin/env python
#
# GPytage leftpanel.py module
#
############################################################################
#    Copyright (C) 2008-2011 by Kenneth Prugh                              #
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

class FileTree(object):
    def __init__(self, gp):
        self.gp = gp

        self.treeContainer = gtk.ScrolledWindow()
        self.fileTree = gtk.TreeView(gp.backend.dataModel)

        self.__initSettings()

        self.treeContainer.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        self.treeContainer.add_with_viewport(self.fileTree)

        #The last file in the tree selected
        self.last = None

    def __initSettings(self):
        self.fileTree.set_search_column(0)

        name = gtk.TreeViewColumn("Package File")
        self.fileTree.append_column(name)

        cname = gtk.CellRendererText()
        cbuf = gtk.CellRendererPixbuf()

        name.pack_start(cbuf, False)
        name.pack_start(cname, True)

        name.add_attribute(cname, "markup", 0)
        name.add_attribute(cbuf, "pixbuf", 1)

        name.set_sizing(gtk.TREE_VIEW_COLUMN_AUTOSIZE)

        self.fileTree.connect("cursor-changed", self.__clicked)

    def __clicked(self, treev, *args):
        """ Change the editor to focus on the file selected """
        selectedkfile = self.getSelectedFile()
        if not selectedkfile:
            return
        if selectedkfile == self.last:
            return
        else:
            self.last = selectedkfile
            self.gp.loadBuffer(selectedkfile)

    def getSelectedFile(self):
        model, iter = self.fileTree.get_selection().get_selected()
        if iter: # None if no row is selected 
            kfile = model.get_value(iter, self.gp.backend.B_KFILE)
            return kfile
        else:
            return None

    #kfile has been edited by one of the editors, we need to reflect this
    #change in the filetree
    def setEdited(self, kfile):
        if (kfile.bEdited):
            return
        kfile.bEdited = True
        model, iter = self.fileTree.get_selection().get_selected()
        editedName = model.get_value(iter, self.gp.backend.B_NAME) + "*"
        model.set_value(iter, self.gp.backend.B_NAME, editedName)

#def expandRows(*args):
#    """ Expand all columns in the left panel """
#    leftview.expand_all()
#    
#def collapseRows(*args):
#    """ Collapse all columns in the left panel """
#    leftview.collapse_all()
#    
#
## Allows us to check if the user simply clicked on the same file or on another one
#__lastSelected = None
#
#def __clicked(treeview, *args):
#    """ Handle TreeView clicks """
#    global __lastSelected
#    model, iter = treeview.get_selection().get_selected()
#    if iter: # None if no row is selected 
#        target = model.get_value(iter, F_REF)
#        targetName = target.path
#    else: 
#        targetName = __lastSelected
#    # Has the selection changed
#    if targetName != __lastSelected:
#        print("LEFTPANEL: parent change detected")
#        if isinstance(target, PackageFileObj.PackageFileObj): # A file
#            print "attempting to change to:", target.path
#            setListModel(target.data)
#        elif isinstance(target, FolderObj.FolderObj): # A folder
#            setListModel(None)
#    # save current selection as last selected
#    __lastSelected = targetName
#
#def __rightClicked(view, event):
#    """ Right click menu for file options """
#    if event.button == 3:
#        menu = gtk.Menu()
#        new = gtk.MenuItem("New File")
#        new.connect("activate", newFile)
#        menu.append(new)
#        rename = gtk.MenuItem("Rename File")
#        rename.connect("activate", renameFile)
#        menu.append(rename)
#        delete = gtk.MenuItem("Delete File")
#        delete.connect("activate", deleteFile)
#        menu.append(delete)
#        menu.show_all()
#        menu.popup(None, None, None, event.button, event.time)
#
## Signals
#leftview.connect("cursor-changed", __clicked)
#leftview.connect("button_press_event", __rightClicked)

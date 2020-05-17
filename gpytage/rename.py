#!/usr/bin/env python
#
#   rename.py GPytage module
#
############################################################################
#    Copyright (C) 2009-2010 by Kenneth Prugh                              #
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
from gi.repository import Gtk

from .config import get_config_path
from datastore import reinitializeDatabase
from PackageFileObj import PackageFileObj
from FolderObj import FolderObj
from sys import stderr
from os import rename
from .errorDialog import errorDialog
from .fileOperations import ensureNotModified

msg = "A file cannot be renamed with unsaved changes. Please save your changes."

def renameFile(*args):
    """ Renames the currently selected file """
    from leftpanel import leftview
    model, iter = leftview.get_selection().get_selected()
    from datastore import F_REF
    try:
        object = model.get_value(iter, F_REF)
        if isinstance(object, PackageFileObj): # A file
            type = "File"
            if object.parent == None:
                setFolder = get_config_path()
            else:
                setFolder = object.parent.path
        elif isinstance(object, FolderObj): # A folder
            type = "Directory"
            setFolder = object.parent.path
        if ensureNotModified(msg):
            __createRenameDialog(object, type, setFolder)
    except TypeError as e:
        print("__renameFile:",e, file=stderr)

def __createRenameDialog(object, type, setFolder):
    """ Spawms the Rename Dialog where a user can choose what the file should
    be renamed to """
    fc = Gtk.FileChooserDialog("Rename file...", None,
            Gtk.FILE_CHOOSER_ACTION_SAVE, (Gtk.STOCK_CANCEL,
                Gtk.RESPONSE_CANCEL, Gtk.STOCK_OK, Gtk.RESPONSE_ACCEPT))
    fc.set_do_overwrite_confirmation(True)
    fc.set_filename(object.path) #Set the fc to the object to be renamed
    fc.set_extra_widget(Gtk.Label("Renaming " + object.path))
    response = fc.run()
    if response == Gtk.RESPONSE_ACCEPT:
        if fc.get_filename() != None:
            __writeRenamedFile(object.path, fc.get_filename())
            reinitializeDatabase()
            __reselectAfterRename(fc.get_filename(), type)
        else:
            print("Invalid rename request", file=stderr)
    fc.destroy()

def __writeRenamedFile(oldFile, newFile):
    """ Performs the actual renaming of the file """
    try:
        rename(oldFile, newFile)
        print(oldFile + " renamed to " + newFile)
    except OSError as e:
        print("Rename: ",e, file=stderr)
        d = errorDialog("Error Renaming...", str(e))
        d.spawn()

def __reselectAfterRename(filePath, type):
    """ Reselects the parent folder of the deleted object """
    from leftpanel import leftview
    model = leftview.get_model()
    model.foreach(getMatch, [filePath, leftview, type])

def getMatch(model, path, iter, data):
    """ Obtain the match and perform the selection """
    testObject = model.get_value(iter, 1) #col 1 stores the reference
    # clarify values passed in from data list
    filePath = data[0]
    leftview = data[1]
    #type = data[2]
    if testObject.path == filePath:
        # We found the file object we just renamed, lets select it
        leftview.expand_to_path(path)
        leftview.set_cursor(path, None, False)
        return True
    else:
        return False

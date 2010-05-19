#!/usr/bin/env python
#
#   deleteFile.py GPytage module
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

import pygtk; pygtk.require("2.0")
import gtk

from sys import stderr
from shutil import rmtree
from os import remove
from fileOperations import hasModified
from PackageFileObj import PackageFileObj
from FolderObj import FolderObj
from datastore import reinitializeDatabase 
from errorDialog import errorDialog

def deleteFile(*args):
    """ Deletes the currently selected file """
    if __ensureNotModified():

        # What exactly is currently selected?
        from leftpanel import leftview
        model, iter = leftview.get_selection().get_selected()
        from datastore import F_REF
        try:
            object = model.get_value(iter, F_REF)
            if isinstance(object, PackageFileObj): # A file
                file = object
                dialog = gtk.MessageDialog(None, gtk.DIALOG_MODAL, gtk.MESSAGE_WARNING, gtk.BUTTONS_YES_NO,\
                        "This operation is irreversible, are you sure you want to delete " + str(file) + "?")
                dialog.set_default_response(gtk.RESPONSE_NO)
                dialog.set_title("File removal...")
                response = dialog.run()
                if response == gtk.RESPONSE_YES:
                    print "Test delete file: " + file.getPath()
                    __removeFile(file.getPath())
                    dialog.destroy()
                    reinitializeDatabase()
                    if file.getParentFolder() != None:
                        __reselectAfterDelete(file.getParentFolder().getPath())
                else:
                    dialog.destroy()
            elif isinstance(object, FolderObj): # A folder 
                folder = object
                dialog = gtk.MessageDialog(None, gtk.DIALOG_MODAL, gtk.MESSAGE_WARNING, gtk.BUTTONS_YES_NO,\
                        "This operation is irreversible, are you sure you want to delete directory " + \
                                str(folder) + " and its contents?")
                dialog.set_default_response(gtk.RESPONSE_NO)
                dialog.set_title("Directory removal...")
                response = dialog.run()
                if response == gtk.RESPONSE_YES:
                    print "Test delete dir: " + folder.getPath()
                    __removeDirectory(folder.getPath())
                    dialog.destroy()
                    reinitializeDatabase()
                    if folder.getParentState():
                        __reselectAfterDelete(folder.getParentFolder().getPath())
                else:
                    dialog.destroy()
        except TypeError,e:
            print >>stderr, "deleteFile: ",e


def __removeFile(path):
    try:
        remove(path)
    except OSError,e:
        print >>stderr,e
        d = errorDialog("Error Deleting File...", str(e))
        d.spawn()

def __removeDirectory(path):
    try:
        rmtree(path)
    except OSError, e:
        print >>stderr, e
        d = errorDialog("Error Deleting Directory...", str(e))
        d.spawn()

def __ensureNotModified():
    if hasModified():
        #inform user to save
        msg = "A file cannot be deleted with unsaved changes. Please save your changes."
        d = errorDialog("Unsaved Files Found...", msg)
        d.spawn()
        return False
    else:
        return True

def __reselectAfterDelete(folderPath):
    """ Reselects the parent folder of the deleted object """
    from leftpanel import leftview
    model = leftview.get_model()
    model.foreach(getMatch, [folderPath, leftview])

def getMatch(model, path, iter, data):
    """ Obtain the match and perform the selection """
    testObject = model.get_value(iter, 1) #col 1 stores the reference
    # clarify values passed in from data list
    folderPath = data[0]
    leftview = data[1]
    if testObject.getPath() == folderPath:
        # since we delete the object, we need to just expand to the folder we
        # were in
        leftview.expand_to_path(path)
        leftview.set_cursor(path, None, False)
        return True
    else:
        return False


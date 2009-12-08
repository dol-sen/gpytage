#!/usr/bin/env python

# GPL2 by Kenneth Prugh <ken69267@gmail.com>

import pygtk; pygtk.require("2.0")
import gtk

from sys import stderr
from shutil import rmtree
from os import remove
from window import createMessageDialog
from fileOperations import hasModified
from PackageFileObj import PackageFileObj
from FolderObj import FolderObj
from datastore import reinitializeDatabase 

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
                        "This operation is irreversible, are you sure you want to delete " + file.getName() + "?")
                dialog.set_default_response(gtk.RESPONSE_NO)
                dialog.set_title("File removal...")
                response = dialog.run()
                if response == gtk.RESPONSE_YES:
                    print "Test delete file: " + file.getPath()
                    __removeFile(file.getPath())
                    dialog.destroy()
                    reinitializeDatabase()
                else:
                    dialog.destroy()
            elif isinstance(object, FolderObj): # A folder 
                folder = object
                dialog = gtk.MessageDialog(None, gtk.DIALOG_MODAL, gtk.MESSAGE_WARNING, gtk.BUTTONS_YES_NO,\
                        "This operation is irreversible, are you sure you want to delete directory " + \
                                folder.getName() + " and its contents?")
                dialog.set_default_response(gtk.RESPONSE_NO)
                dialog.set_title("Directory removal...")
                response = dialog.run()
                if response == gtk.RESPONSE_YES:
                    print "Test delete dir: " + folder.getPath()
                    __removeDirectory(folder.getPath())
                    dialog.destroy()
                    reinitializeDatabase()
                else:
                    dialog.destroy()
        except TypeError,e:
            print >>stderr, "deleteFile: ",e


def __removeFile(path):
    try:
        remove(path)
    except OSError,e:
        print >>stderr,e

def __removeDirectory(path):
    try:
        rmtree(path)
    except IOError, e:
        print >>stderr, e

def __ensureNotModified():
    if hasModified():
        #inform user to save
        createMessageDialog(None, gtk.DIALOG_DESTROY_WITH_PARENT,
                gtk.MESSAGE_ERROR, gtk.BUTTONS_OK, "Unsaved Files Found...",
                "A new file cannot be created with unsaved changes. Please save your changes.")
        return False
    else:
        return True

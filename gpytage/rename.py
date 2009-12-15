#!/usr/bin/env python

# GPL2 by Kenneth Prugh <ken69267@gmail.com>

import pygtk; pygtk.require("2.0")
import gtk

from config import get_config_path
from fileOperations import hasModified
from window import createMessageDialog
from datastore import reinitializeDatabase 
from PackageFileObj import PackageFileObj
from FolderObj import FolderObj
from sys import stderr

def renameFile(*args):
    """ Renames the currently selected file """
    from leftpanel import leftview
    model, iter = leftview.get_selection().get_selected()
    from datastore import F_REF
    try:
        object = model.get_value(iter, F_REF)
        if isinstance(object, PackageFileObj): # A file
            type = "File"
            if object.getParentFolder() == None:
                setFolder = get_config_path()
            else:
                setFolder = object.getParentFolder().getPath()
        elif isinstance(object, FolderObj): # A folder 
            type = "Directory"
            setFolder = object.getParentFolder().getPath()
        __createRenameDialog(object, type, setFolder)
    except TypeError,e:
        print >>stderr, "__renameFile:",e

def __createRenameDialog(object, type, setFolder):
    fc = gtk.FileChooserDialog("Rename file...", None,
            gtk.FILE_CHOOSER_ACTION_SAVE, (gtk.STOCK_CANCEL,
                gtk.RESPONSE_CANCEL, gtk.STOCK_OK, gtk.RESPONSE_ACCEPT))
    fc.set_do_overwrite_confirmation(True)
    fc.set_filename(object.getPath()) #Set the fc to the object to be renamed
    fc.set_extra_widget(gtk.Label("Renaming " + object.getPath()))
    response = fc.run()
    # todo return the value to renameFile and handle accordingly
    if response == gtk.RESPONSE_ACCEPT:
        if fc.get_filename() != None:
            print object.getPath() + " renamed to " + fc.get_filename()
        else:
            print >>stderr, "Invalid rename request"
    fc.destroy()

def __ensureNotModified():
    if hasModified():
        #inform user to save
        createMessageDialog(None, gtk.DIALOG_DESTROY_WITH_PARENT,
                gtk.MESSAGE_ERROR, gtk.BUTTONS_OK, "Unsaved Files Found...",
                "A new file cannot be created with unsaved changes. Please save your changes.")
        return False
    else:
        return True

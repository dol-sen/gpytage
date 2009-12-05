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

def newFile(*args):
    """ Create a new file """
    if __ensureNotModified():
        nFile = __getNewFileChoice()
        if nFile is not None:
            __saveToDisk(nFile)
            reinitializeDatabase()

def __saveToDisk(nFile):
    print "Saving new file: " + nFile
    try:
        f=open(nFile, 'w')
        f.write("# " + nFile + "\n")
        f.write("# Created by GPytage\n")
        f.close
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

def __getNewFileChoice():
    dialog = gtk.FileChooserDialog("New file...", None,
            gtk.FILE_CHOOSER_ACTION_SAVE, (gtk.STOCK_CANCEL,
                gtk.RESPONSE_CANCEL, gtk.STOCK_OPEN, gtk.RESPONSE_OK))
    filter = gtk.FileFilter()
    filter.set_name("All files")
    filter.add_pattern("*")
    dialog.add_filter(filter)
    # Does the user have a folder selected that we should instead load on
    # newFile?
    from leftpanel import leftview
    model, iter = leftview.get_selection().get_selected()
    from datastore import F_REF
    try:
        object = model.get_value(iter, F_REF)
        if isinstance(object, PackageFileObj): # A file
            folder = object.getParentFolder()
        elif isinstance(object, FolderObj): # A folder 
            folder = object
        if folder == None:
            folderPath = get_config_path()
        else:
            folderPath = folder.getPath() # Get the path to the folder object
    except TypeError,e:
        print >>stderr, "__getNewFileChoice:",e
        #Nothing selected, select default
        folderPath = get_config_path()

    dialog.set_current_folder(folderPath)
    ## end logic
    
    dialog.set_do_overwrite_confirmation(True)

    response = dialog.run()
    name = None
    if response == gtk.RESPONSE_OK:
        name = dialog.get_filename()
    dialog.destroy()
    return name


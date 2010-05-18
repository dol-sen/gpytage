#!/usr/bin/env python
#
#   newFile.py GPytage module
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

from config import get_config_path
from fileOperations import hasModified
from datastore import reinitializeDatabase 
from PackageFileObj import PackageFileObj
from FolderObj import FolderObj
from sys import stderr
from errorDialog import errorDialog

def newFile(*args):
    """ Create a new file """
    if __ensureNotModified():
        nFile = __getNewFileChoice()
        if nFile is not None:
            __saveToDisk(nFile)
            reinitializeDatabase()
            __reselectAfterNew(nFile)

def __saveToDisk(nFile):
    print "Saving new file: " + nFile
    try:
        f=open(nFile, 'w')
        f.write("# " + nFile + "\n")
        f.write("# Created by GPytage\n")
        f.close
    except IOError, e:
        print >>stderr, e
        d = errorDialog("Error Creating File...", str(e))
        d.spawn()

def __ensureNotModified():
    if hasModified():
        #inform user to save
        msg = "A new file cannot be created with unsaved changes. Please save your changes."
        d = errorDialog("Unsaved Files Found...", msg)
        d.spawn()
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

def __reselectAfterNew(filePath):
    """ Reselects the parent folder of the deleted object """
    from leftpanel import leftview
    model = leftview.get_model()
    model.foreach(getMatch, [filePath, leftview])

def getMatch(model, path, iter, data):
    """ Obtain the match and perform the selection """
    testObject = model.get_value(iter, 1) #col 1 stores the reference
    # clarify values passed in from data list
    filePath = data[0]
    leftview = data[1]
    if testObject.getPath() == filePath:
        # We found the file object we just added, lets select it
        leftview.expand_to_path(path)
        leftview.set_cursor(path, None, False)
        #from rightpanel import setListModel
        #setListModel(testObject.getData())
        return True
    else:
        return False

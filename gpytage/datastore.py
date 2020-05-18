#!/usr/bin/env python
#
# GPytage datastore.py module
#
############################################################################
#    Copyright (C) 2008-2010 by Kenneth Prugh                              #
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

import os

from . import FolderObj, PackageFileObj

from .config import config_files, get_config_path

# declare some constants for clarity of code
F_NAME = 0
F_REF = 1

folderModel = Gtk.TreeStore(
                            str,        # 0 entry name
                            object,     # 1 entry reference
)                                       # Folders

TLFolders = [] # Holds *ALL* folders, check for children
TLFiles = []

def initData():
    """ Constructs Folder and PackageFile objects """
    path = get_config_path()
    #print "USING PATH: " + path
    for rootDir, folders, files in os.walk(path, topdown=True):
        # Begin the construction
        if rootDir is get_config_path(): # we are top level, no children
            # Filter unrelated files TOPLEVEL ONLY
            # Folders sanity
            for folder in folders[:]:
                if folder not in config_files:
                    folders.remove(folder) #ignore unrelated folders
            # Files sanity
            for pfile in files[:]:
                if pfile not in config_files:
                    files.remove(pfile) #ignore unrelated files
            #construct
            for folder in folders:
                foldobj = FolderObj.FolderObj(folder, rootDir + "/" + folder)
                TLFolders.append(foldobj)
            for pfile in files:
                fileobj = PackageFileObj.PackageFileObj(pfile, rootDir + "/" + pfile, None)
                TLFiles.append(fileobj)
        else: # No longer top level, we are inside a folder
            tlname = rootDir.split("/")[-1] # /etc/portage/sets => sets
            #construct
            for folder in folders: # recursive folder
                parent = __getParent(tlname, "folder") # FolderObj
                foldobj = FolderObj.FolderObj(folder, rootDir + "/" + folder)
                foldobj.parentState = True
                foldobj.parent = parent
                parent.addFolder(foldobj)
                parent.childState = True
                TLFolders.append(foldobj)
            for pfile in files:
                parent = __getParent(tlname, "file") #PackageFileObj
                fileobj = PackageFileObj.PackageFileObj(pfile, rootDir + "/" + pfile, parent)
                parent.addPackage(fileobj)
                #TLFiles.append(fileobj)

def __getParent(tlname, type):
    """ Finds the associated parent named tlname from the specified list type """
    if type == "folder":
        for f in TLFolders:
            if str(f) == tlname:
                return f
    if type == "file":
        for f in TLFolders:
            if str(f) == tlname:
                return f

def initTreeModel():
    """ Populate the TreeModel with data """
    for folder in TLFolders: #Contains *all* folders
        # Handle Top level Folders with no folder children first
        if (folder.childState == False and folder.parentState == False):
            row = [folder, folder]
            parentIter = folderModel.append(None, row)
            path = folderModel.get_path(parentIter)
            treeRowRef = Gtk.TreeRowReference(folderModel, path)
            folder.treeRowRef = treeRowRef
            children = folder.getPackages()
            for child in children: #Add children files to treeview
                row = [child, child]
                childIter = folderModel.append(parentIter, row)
                path = folderModel.get_path(childIter)
                treeRowRef = Gtk.TreeRowReference(folderModel, path)
                child.treeRowRef = treeRowRef
        else: # Folders have folder children (an unknown amount unfortunately) (Recursive)
            #Add the parent folder to the treeview
            row = [folder, folder]
            if folder.parentState == False: #Top level
                parentIter = folderModel.append(None, row)
                path = folderModel.get_path(parentIter)
                treeRowRef = Gtk.TreeRowReference(folderModel, path)
                folder.treeRowRef = treeRowRef # We will need this later to pack the children
                                                 # in the treeview
            else: #child folder
                # We gotta find the stupid things parent row
                parent = folder.parent
                path = parent.treeRowRef.get_path()
                grandIter = folderModel.get_iter(path)
                parentIter = folderModel.append(grandIter, row)
                path = folderModel.get_path(parentIter)
                treeRowRef = Gtk.TreeRowReference(folderModel, path)
                folder.treeRowRef = treeRowRef

            for subfile in folder.getPackages():
                row = [subfile, subfile]
                FileIter = folderModel.append(parentIter, row)
                path = folderModel.get_path(FileIter)
                treeRowRef = Gtk.TreeRowReference(folderModel, path)
                subfile.treeRowRef = treeRowRef
    # Top Level Files only
    for pfile in TLFiles:
        row = [pfile, pfile]
        parentIter = folderModel.append(None, row)
        path = folderModel.get_path(parentIter)
        treeRowRef = Gtk.TreeRowReference(folderModel, path)
        pfile.treeRowRef = treeRowRef

def __clearData():
    """ Clears the TreeModel and the TLFolder,TLFiles list """
    folderModel.clear()
    del TLFolders[:]
    del TLFiles[:]

def reinitializeDatabase():
    """ Clears the backend and rebuilds the database from disk """
    __clearData()
    initData()
    initTreeModel()

    from .rightpanel import setListModel
    setListModel(None)

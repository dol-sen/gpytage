#!/usr/bin/env python
#
# GPytage FolderObj.py module
#
############################################################################
#    Copyright (C) 2009 by Kenneth Prugh                                   #
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

class FolderObj:
    """ FolderObj represent Folders """
    
    def __init__(self, name, filePath):
        self.Name = name
        self.filePath = filePath
        self.packageFileChildren = [] # List for PackageFile children
        self.folderChildren = [] # List for FolderObj children
        self.hasChildren = False # By default we have no folder children
        self.hasParent = False # Top level default
        self.parentFolder = None # Parent FolderObj
        self.treeRowRef = None
    
    def addPackage(self, Package):
        """ Add the specified PackageFile """
        self.packageFileChildren.append(Package)
        
    def removePackage(self, Package):
        """ Removes the specified PackageFile """
        self.packageFileChildren.remove(Package)
        
    def addFolder(self, folder):
        """ Add child FolderObj """
        self.folderChildren.append(folder)
        
    def removeFolder(self, folder):
        """ Remove child FolderObj """
        self.folderChildren.remove(folder)
        
    def setChildren(self, boolean):
        """ Sets the state of hasChildren with the passed boolean """
        self.hasChildren = boolean
        
    def getChildrenState(self):
        """ Returns whether the Folder has child Folder objects """
        return self.hasChildren
        
    def getName(self):
        """ Return FolderObj Name """
        return self.Name
    
    def getPackages(self):
        """ Return list of children PackageFileObj's """
        return self.packageFileChildren
    
    def getFolders(self):
        """ Return list of children FolderObj's """
        return self.folderChildren
    
    def setHasParent(self, boolean):
        """ Set whether the object has a parent or not """
        self.hasParent = True
        
    def getParentState(self):
        """ Return True if object has a parent """
        return self.hasParent

    def getParentFolder(self):
        """ Retrieve parent FolderObj """
        return self.parentFolder

    def setParentFolder(self, parentFolder):
        """ Sets the parent FolderObj """
        self.parentFolder = parentFolder

    def getTreeRowRef(self):
        """ Returns a gtk.TreeRowReference pointing to this FolderObj """
        return self.treeRowRef

    def setTreeRowRef(self, value):
        """ Set the gtk.TreeRowReference for this FolderObj """
        self.treeRowRef = value

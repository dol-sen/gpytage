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

class FolderObj(object):
    """ FolderObj represent Folders """
    def __repr__(self):
        return self._name
    
    def __init__(self, name, filepath):
        self._name = name
        self._path = filepath
        self._packageFileChildren = [] # List for PackageFile children
        self._folderChildren = [] # List for FolderObj children
        self._childState = False # By default we have no folder children
        self._parentState = False # Top level default
        self._parentFolder = None # Parent FolderObj
        self._treeRowRef = None
    
    @property
    def path(self):
        """ The ondisk path representation for the Folder """
        return self._path

    def addPackage(self, Package):
        """ Add the specified PackageFile """
        self._packageFileChildren.append(Package)

    def getPackages(self):
        """ Return list of children PackageFileObj's """
        return self.packageFileChildren
        
    def removePackage(self, Package):
        """ Removes the specified PackageFile """
        self._packageFileChildren.remove(Package)
        
    def addFolder(self, folder):
        """ Add child FolderObj """
        self._folderChildren.append(folder)
        
    def getFolders(self):
        """ Return list of children FolderObj's """
        return self._folderChildren
    
    def removeFolder(self, folder):
        """ Remove child FolderObj """
        self._folderChildren.remove(folder)
        
    @property
    def childState(self):
        """ True if folder has children """
        return self._childState

    @childState.setter
    def childState(self, boolean):
        self._childState = boolean
        
    @property
    def parentState(self):
        """ True if folder has a parent """
        return self._parentState

    @parentState.setter
    def parentState(self, boolean):
        self._parentState = boolean
        
    @property
    def parent(self):
        """ Parent folder """
        return self._parentFolder

    @parent.setter
    def parent(self, parentFolder):
        self._parentFolder = parentFolder

    @property
    def treeRowRef(self):
        """ gtk.TreeRowReference pointing to this Folder """
        return self._treeRowRef

    @treeRowRef.setter
    def treeRowRef(self, value):
        self._treeRowRef = value
        

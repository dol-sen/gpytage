#!/usr/bin/env python
#
# GPytage PackageFileObj.py module
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

import gtk

L_NAME = 0
L_FLAGS = 1
L_REF = 2

class PackageFileObj:
    """ PackageFile objects represent Files and their contents """
    
    def __init__(self, name, path, parent): # FilePath, FolderObj
        self.name = name
        self.path = path
        self.parentObj = parent
        self.data = gtk.ListStore(str, str, object)
        self.initData()
        self.edited = False
        self.treeRowRef = None
        
    def initData(self):
        """ Read contents of File into ListStore """
        self.data.clear()
        rawData = self.__scanFileContents(self.path)
        for line in rawData:
            try:
                c1 = line[L_NAME].rstrip()
            except:
                c1 = None
            try:
                c2 = line[L_FLAGS].rstrip()
            except:
                c2 = None
            row = [c1, c2, self]
            self.data.append(row)

    def getData(self):
        """ Return the internal gtk.ListStore """
        return self.data
    
    def getName(self):
        """ Return Name """
        return self.name

    def getEditedState(self):
        """ Returns whether the PackageFileObj has been modified or not """
        return self.edited

    def setEditedState(self, boolean):
        """ Sets the PackageFileObj edited state """
        self.edited = boolean
        
    def getTreeRowRef(self):
        """ Returns a gtk.TreeRowReference pointing to this PackageFileObj """
        return self.treeRowRef

    def setTreeRowRef(self, value):
        """ Set the gtk.TreeRowReference for this PackageFileObj """
        self.treeRowRef = value
        
    def getPath(self):
        """ Returns the filepath for this PackageFileObj """
        return self.path
        
    def __scanFileContents(self, filepath):
        """ Return data in specified file in a list of a list [[col1, col2]]"""
        try:
            f=open(filepath, 'r')
            contents = f.readlines()
            f.close()
        except IOError: #needed or everything breaks
            contents = None
            print 'HELPER: scan_contents(); Warning: Critical file %s not found' % (filepath)
    
        data = [] #list of list: eg [['python','x86']]
        for i in contents:
            if i.startswith('#'): #don't split if its a comment
                new = [i, None]
            else:
                new = i.split(None,1)
            # NoneType's are annoying...lets replace them with an empty string
            # Occurs when no flags present
            if len(new) == 1:
                new.append("")
            # Blank line
            if len(new) == 0:
                new = ["", ""]
            data.append(new)
        return data #return the master list of lists

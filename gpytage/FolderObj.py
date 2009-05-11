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
    
    def addPackage(self, Package):
        """ Add the specified PackageFile """
        self.packageChildren.append(Package)
        
    def removePackage(self, Package):
        """ Removes the specified PackageFile """
        self.packageChildren.remove(Package)
        
    def getName(self):
        return self.Name
    
    def getPackages(self):
        return self.packageFileChildren

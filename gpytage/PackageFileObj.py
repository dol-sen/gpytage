#!/usr/bin/env python
#
# GPytage PackageFileObj.py module
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

import gi
gi.require_version("Gtk", "3.0") # make sure we have the right version
from gi.repository import Gtk

from sys import stderr

L_NAME = 0
L_FLAGS = 1
L_REF = 2

class PackageFileObj(object):
    """ PackageFile objects represent Files and their contents """
    def __repr__(self):
        return self._name

    def __init__(self, name, path, parent): # FilePath, FolderObj
        self._name = name
        self._path = path
        self._parent = parent
        self._data = Gtk.ListStore(str, str, object)
        self._edited = False
        self._treeRowRef = None
        self.initData()

    def initData(self):
        """ Read contents of File into ListStore """
        self.data.clear()
        rawData = self.__scanFileContents(self.path)
        for line in rawData:
            try:
                c1 = line[L_NAME].rstrip()
            except:
                c1 = ""
            try:
                c2 = line[L_FLAGS].rstrip()
            except:
                c2 = ""
            row = [c1, c2, self]
            self.data.append(row)

    @property
    def path(self):
        """ filepath for this PackageFileObj """
        return self._path

    @property
    def parent(self):
        """ The parent folder """
        return self._parent

    @property
    def data(self):
        """ internal Gtk.ListStore """
        return self._data

    @property
    def edited(self):
        """ The state of the file being edited """
        return self._edited

    @edited.setter
    def edited(self, boolean):
        """ Sets the PackageFileObj edited state """
        self._edited = boolean

    @property
    def treeRowRef(self):
        """ Gtk.TreeRowReference pointing to this PackageFileObj """
        return self._treeRowRef

    @treeRowRef.setter
    def treeRowRef(self, boolean):
        """ Set the Gtk.TreeRowReference for this PackageFileObj """
        self._treeRowRef = boolean

    def __scanFileContents(self, filepath):
        """ Return data in specified file in a list of a list [[col1, col2]]"""
        data = [] #list of list: eg [['python','x86']]
        try:
            f = open(filepath, 'r')
            contents = f.readlines()
            f.close()
        except IOError as e: #needed or everything breaks
            contents = None
            print(e, file=stderr)
            from .errorDialog import errorDialog
            d = errorDialog("Error Reading File...", str(e))
            d.spawn()
            return data

        for i in contents:
            if i.startswith('#'): #don't split if its a comment
                new = [i, None]
            else:
                new = i.split(None, 1)
            # NoneType's are annoying...lets replace them with an empty string
            # Occurs when no flags present
            if len(new) == 1:
                new.append("")
            # Blank line
            if len(new) == 0:
                new = ["", ""]
            data.append(new)
        return data #return the master list of lists


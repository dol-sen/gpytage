#!/usr/bin/env python
#
############################################################################
#    Copyright (C) 2011-2012 by Kenneth Prugh                              #
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

class kfile(object):
    T_EDIT = 0
    T_COL = 1

    def __init__(self, name, path):
        self._data = None

        self.bEdited = False
        self.name = name
        self.path = path

        #Files which need the 2col layout have package in their names
        if "package" in name+path: 
            self.ftype = kfile.T_COL 
        else: 
            self.ftype = kfile.T_EDIT 

        # Depending on the file type, we will either need to set the data as a
        # textbuffer for an editor view, or as a 2 col liststore for the other
        # view
        #
        # Move this to getData() domain for a type of lazy loading. 
        #self.loadData()

    def getData(self):
        if self._data != None:
            return self._data
        else:
            if (self.ftype == kfile.T_EDIT):
                self._data = gtk.TextBuffer()
                self.__loadData()
            else:
                self._data = gtk.ListStore(str, str, object)
                self.__loadColData()
            return self._data

    def __loadData(self):
        """ Read contents of File into self.data Buffer """
        rawData = self.__scanFileContents(self.path)
        for line in rawData:
            iter = self._data.get_end_iter()
            self._data.insert(iter, line)

    def __loadColData(self):
        rawData = self.__scanFileContents(self.path)
        for line in rawData:
            if (line.startswith("#")):
                name = line
                flags = ""
            else:
                try:
                    name = line.split(" ", 1)[0]
                except:
                    name = ""

                try:
                    flags = line.split(" ",1)[1]
                except:
                    flags = ""
            
            self._data.append([name, flags, self])

    #throws ioerror
    def savedata(self):
        """ Private method to write file to desk """
        # Save the file
        print "Attempting to save " + self.path
        #sync buffer to disk
        return
        try:
            f = open(self.path, 'w')
            for row in self._data:
                pass
        finally:
            f.close()


    #throws ioerror
    def __scanFileContents(self, filepath):
        """ Return data in specified file in a list """
        data = []
        try:
            f = open(filepath, 'r')
            data = f.readlines()
        finally:
            f.close()
        return data


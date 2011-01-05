#!/usr/bin/env python
#
############################################################################
#    Copyright (C) 2011 by Kenneth Prugh                                   #
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
    def __init__(self, name, path):
        self.data = gtk.ListStore(
                str,    # Name
                str,    # Use flags
                object) # Reference to kfile

        self.bEdited = False
        self.name = name
        self.path = path

    def loadData(self):
        """ Read contents of File into ListStore """
        self.data.clear()
        rawData = self.__scanFileContents(self.path)
        for line in rawData:
            c1 = line[L_NAME].rstrip()
            c2 = line[L_FLAGS].rstrip()
            row = [c1, c2, self]
            self.data.append(row)

    #throws ioerror
    def savedata(self):
        """ Private method to write file to desk """
        # Save the file
        print "Attempting to save " + self.path
        try:
            f = open(self.path, 'w')
            for row in self.data:
                if row[0] is not None:
                    c1 = row[0]
                else:
                    c1 = ""
                if row[1] is not None:
                    c2 = row[1]
                else:
                    c2 = ""
                if row[0].strip().startswith("#"):
                    f.write(c1 + c2 + "\n")
                else:
                    f.write(c1 + " " + c2 + "\n")
        finally:
            f.close()


    #throws ioerror
    def __scanFileContents(self, filepath):
        """ Return data in specified file in a list of a list [[col1, col2]]"""
        data = [] #list of list: eg [['python','x86']]
        try:
            f = open(filepath, 'r')
            contents = f.readlines()
        finally:
            f.close()
    
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
        return data


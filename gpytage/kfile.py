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
        self.data = gtk.TextBuffer()

        self.bEdited = False
        self.name = name
        self.path = path

        self.loadData()

    def loadData(self):
        """ Read contents of File into self.data Buffer """
        rawData = self.__scanFileContents(self.path)
        for line in rawData:
            iter = self.data.get_end_iter()
            self.data.insert(iter, line)

    #throws ioerror
    def savedata(self):
        """ Private method to write file to desk """
        # Save the file
        print "Attempting to save " + self.path
        #sync buffer to disk
        return
        try:
            f = open(self.path, 'w')
            for row in self.data:
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


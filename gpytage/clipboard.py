#!/usr/bin/env python
#
#   clipboard.py GPytage module
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

from .helper import getMultiSelection, getCurrentFile
from .PackageFileObj import L_NAME, L_FLAGS, L_REF

class clipboard():
    def __init__(self):
        self.clipboard = Gtk.Clipboard()

    def copyToClipboard(self, rightview):
        """ Copies selected rows into the clipboard """
        selectedRefs = getMultiSelection(rightview)
        if len(selectedRefs) == 0:
            return
        model = rightview.get_model()

        clipText = ""

        for ref in selectedRefs:
            iter = model.get_iter(ref.get_path())
            c1 = model.get_value(iter, L_NAME)
            c2 = model.get_value(iter, L_FLAGS)
            clipText += c1 + ' ' + c2 + '\n'

        self.clipboard.set_text(clipText, -1)

    def cutToClipboard(self, rightview):
        """ Copies selected rows into the clipboard and then deletes them """
        self.copyToClipboard(rightview)
        from .rightpanel import deleteRow
        deleteRow(rightview)

    def pasteClipboard(self, rightview):
        """ Pastes the clipboard below the current selection """
        rowReferences = getMultiSelection(rightview)
        model = rightview.get_model()

        # Grab the actual clipboard text
        clipText = self.clipboard.wait_for_text()

        # Get a list to store into the PackageFile
        newData = self.__formatPaste(clipText)

        try:
            # A row has been selected and we should paste below it
            lastRowSelectedPath = rowReferences[-1].get_path()

            lastRowIter = model.get_iter(lastRowSelectedPath)
            # We need to link this new row with its PackageFile Object
            PackageFile = model.get_value(lastRowIter, L_REF)

            for row in newData:
                #insert the new row
                newRow = model.insert_after(lastRowIter, [row[0], row[1], PackageFile])
                newPath = model.get_path(newRow)
                lastRowIter = model.get_iter(newPath)

        except IndexError:
            # No row selected
            PackageFile, lModel = getCurrentFile()

            for row in newData:
                #insert the new row
                newRow = model.append([row[0], row[1], PackageFile])

            # Fire off the edited methods
            from .fileOperations import fileEdited
            fileEdited(PackageFile)

    def __formatPaste(self, text):
        """ Formats the clipboard text into a form acceptible for storing into
        the Package File """
        rawData = []

        tmpdata = text.split('\n')

        for line in tmpdata:
            if len(line.strip()) > 0:
                cols = line.split(None, 1)
                # If after splitting we only have 1 element in our column
                # list we need to append a blank so that GPytage may store it
                # in its PackageFile object
                if len(cols) == 1:
                    cols.append("")

                rawData.append(cols)
        return rawData

#!/usr/bin/env python

# GPL2 by Kenneth Prugh <ken69267@gmail.com>

import pygtk; pygtk.require("2.0")
import gtk

from helper import getMultiSelection, getCurrentFile
from PackageFileObj import L_NAME, L_FLAGS, L_REF

class clipboard():
    def __init__(self):
        self.clipboard = gtk.Clipboard() 

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
        from rightpanel import deleteRow
        deleteRow(rightview)

    def pasteClipboard(self, rightview):
        """ Pastes the clipboard below the current selection """
        selectedRegs = getMultiSelection(rightview)
        
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
            from fileOperations import fileEdited
            fileEdited(PackageFile)

    def __formatPaste(self, text):
        rawData = []

        tmpdata = text.split('\n')

        for line in tmpdata:
            if len(line) > 0:
                rawData.append(line.split(None, 1))

        return rawData

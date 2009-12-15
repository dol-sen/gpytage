#!/usr/bin/env python

# GPL2 by Kenneth Prugh <ken69267@gmail.com>

import pygtk; pygtk.require("2.0")
import gtk

from helper import getMultiSelection, getCurrentFile
from PackageFileObj import L_NAME, L_FLAGS

class clipboard():
    def __init__(self):
        self.clipboard = gtk.Clipboard() 

    def copyToClipboard(self, rightview):
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

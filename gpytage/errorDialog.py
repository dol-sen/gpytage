#!/usr/bin/env python
#
# GPytage errorDialog.py module
#
############################################################################
#    Copyright (C) 2010 by Kenneth Prugh                                   #
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

class errorDialog(Gtk.MessageDialog):
    """ Spawn an error dialog with the given title and text. """
    def __init__(self, title, text):
        Gtk.MessageDialog.__init__(self, None, Gtk.DIALOG_DESTROY_WITH_PARENT, Gtk.MESSAGE_ERROR, Gtk.BUTTONS_OK, text)
        self.set_title(title)

    def spawn(self):
        self.run()
        self.destroy()

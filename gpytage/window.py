#!/usr/bin/env python
#
# GPytage window.py module
#
############################################################################
#    Copyright (C) 2008-2009 by Kenneth Prugh                              #
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

window = Gtk.Window(Gtk.WINDOW_TOPLEVEL)
window.set_title("GPytage")
__editedState = False

from .clipboard import clipboard
clipboard = clipboard()

def setTitleEdited(bool):
    """
    Changes the state of the title. Edited state causes the title to change to *GPytage.

    True: Sets as edited

    """
    global __editedState
    if bool is True:
        window.set_title("*GPytage")
        __editedState = True
    else:
        window.set_title("GPytage")
        __editedState = False

def getTitleState():
    """ Returns if the title is in the edited state """
    return __editedState

def unsavedDialog():
    """
    Spawn Generic Yes/No/Save Dialog when unsaved changes are present.

    YES returns -8. NO returns -9. Save returns 1.

    """
    uD = Gtk.MessageDialog(parent=None, flags=Gtk.DIALOG_MODAL, type=Gtk.MESSAGE_WARNING, buttons=Gtk.BUTTONS_YES_NO, message_format="You have unsaved changes, if you proceed these changes will be lost.\n\n Do you wish to Quit?")
    uD.set_title("You have unsaved changes")
    uD.set_default_response(Gtk.RESPONSE_NO)
    status = uD.run()
    return status, uD


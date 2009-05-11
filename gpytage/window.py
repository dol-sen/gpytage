#!/usr/bin/env python
#
# GPytage window.py module
#
############################################################################
#    Copyright (C) 2008 by Kenneth Prugh                                   #
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

import pygtk; pygtk.require("2.0")
import gtk
from sys import stderr

window = gtk.Window(gtk.WINDOW_TOPLEVEL)
window.set_title("GPytage")
__editedState = False

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

def createMessageDialog(parent, flags, type, buttons, mtitle, message_format):
	md = gtk.MessageDialog(None, flags, type, buttons, message_format)
	md.set_title(mtitle)
	md.run()
	md.destroy()

def unsavedDialog():
	"""
	Spawn Generic Yes/No/Save Dialog when unsaved changes are present.

	YES returns -8. NO returns -9. Save returns 1.
	
	"""
	uD = gtk.MessageDialog(parent=None, flags=gtk.DIALOG_MODAL, type=gtk.MESSAGE_WARNING, buttons=gtk.BUTTONS_YES_NO, message_format="You have unsaved changes, if you proceed these changes will be lost.\n\n Do you wish to continue?")
	uD.set_title("You have unsaved changes")
	uD.set_default_response(gtk.RESPONSE_NO)
	RESPONSE_SAVE = 1
	uD.add_button("_Save and Continue", 1)
	status = uD.run()
	return status, uD

def error_dialog(errors):
	"""generic dialog to report file operation errors"""
	err = ',\n'.join(errors)
	message = "Please correct the problem(s) and try again.  It may include running gpytage as the root user\n\n" + err
	createMessageDialog(None, gtk.DIALOG_DESTROY_WITH_PARENT, 
		gtk.MESSAGE_ERROR, gtk.BUTTONS_OK, "Error Saving Files...", message)

#!/usr/bin/env python
#
# GPytage helper.py module
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

import gtk
from PackageFileObj import L_NAME, L_FLAGS, L_REF

def getMultiSelection(treeview):
    """ Return a list of the currently selected rows in the form of TreeRowReferences """
    selection = treeview.get_selection()
    model, paths = selection.get_selected_rows()
    rowReferences = []
    for path in paths:
        rowRef = gtk.TreeRowReference(model, path)
        rowReferences.append(rowRef)
    return rowReferences

def getCurrentFile():
	""" Return  [PackageFileObj, model] when it cannot be retrieved by others means """
	from leftpanel import leftview
	model, iter = leftview.get_selection().get_selected()
	from datastore import F_REF
	try:
		PackageFile = model.get_value(iter, F_REF)
	except: #Nothing selected
		PackageFile = None
	return [PackageFile, model]
	

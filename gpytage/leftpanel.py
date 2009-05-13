#!/usr/bin/env python
#
# GPytage leftpanel.py module
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
import datastore
from datastore import F_NAME, F_REF
#===============================================================================
# import rightpanel
# from panelfunctions import switchListView
#===============================================================================

leftview = gtk.TreeView(datastore.folderModel) #create the container

leftview.set_search_column(F_NAME)

# TreeViewColumns
namecol = gtk.TreeViewColumn('Package File')

# add TreeViewColumn to TreeView
leftview.append_column(namecol)

cell = gtk.CellRendererText()

# add CellRenderer to TreeViewColumn
namecol.pack_start(cell, True)
namecol.add_attribute(cell, 'text', F_NAME)
namecol.set_sizing(gtk.TREE_VIEW_COLUMN_AUTOSIZE)

#===============================================================================
# Scroll Window
#===============================================================================
scroll = gtk.ScrolledWindow()
scroll.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
scroll.add_with_viewport(leftview)

# Allows us to check if the user simply clicked on the same file or on another one
__lastSelected = None

def __clicked(treeview, *args):
	""" Handle TreeView clicks """
	global __lastSelected
	model, iter = treeview.get_selection().get_selected()
	if iter: # None if no row is selected 
		parent = model.get_value(iter, F_REF).getName()
	else: 
		parent = lastSelected
	# has the selection really changed?
	if parent != last_parent:
		print("LEFTPANEL: parent change detected")
		list = model.get_value(iter, F_NAME).strip('*')
		print list
		print parent
		if parent.strip('*') == 'package.' + list:
			rightpanel.setListModel(parent.strip('*'))
		else:
			rightpanel.setListModel(list.strip('*'))
	else: #fixes bug: if two subfiles are selected after each other with same parent
		list = model.get_value(iter, E_NAME).strip('*')
		rightpanel.setListModel(list)
	# save current selection as last selected
	lastSelected = parent

# Signals
leftview.connect("cursor-changed", __clicked)

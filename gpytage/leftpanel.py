#!/usr/bin/env python
#
# GPytage leftpanel.py module
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

import pygtk; pygtk.require("2.0")
import gtk

from datastore import F_NAME, F_REF, folderModel
from rightpanel import setListModel
import PackageFileObj, FolderObj

leftview = gtk.TreeView(folderModel) #create the container

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
		target = model.get_value(iter, F_REF)
		targetName = target.getName()
	else: 
		targetName = __lastSelected
	# Has the selection changed
	if targetName != __lastSelected:
		print("LEFTPANEL: parent change detected")
		if isinstance(target, PackageFileObj.PackageFileObj): # A file
			print "attempting to change to:", target.getName()
			setListModel(target.getData())
		elif isinstance(target, FolderObj.FolderObj): # A folder
			pass
	# save current selection as last selected
	__lastSelected = targetName

# Signals
leftview.connect("cursor-changed", __clicked)

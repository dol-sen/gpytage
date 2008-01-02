#!/usr/bin/env python
#
# GPytage leftpanel.py module
#
############################################################################
#    Copyright (C) 2007 by Kenneth Prugh                                   #
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
import rightpanel


leftview = gtk.TreeView(datastore.datastore) #create the container

leftview.set_search_column(0) #search broken atm #child?
leftview.set_reorderable(True) # allow inline drag and drop
#columns
namecol = gtk.TreeViewColumn('Package File')
testcol = gtk.TreeViewColumn('Flags')
boolcol = gtk.TreeViewColumn() #editable col
filecol = gtk.TreeViewColumn()
#add to tree
leftview.append_column(namecol)
leftview.append_column(testcol)
leftview.append_column(boolcol)
leftview.append_column(filecol)

#render cell
cell = gtk.CellRendererText()
cell1 = gtk.CellRendererText()

#add cols to cell
namecol.pack_start(cell, True)
namecol.set_attributes(cell, text=0)
namecol.add_attribute(cell, "editable", 2)#set row editable
namecol.set_sizing(gtk.TREE_VIEW_COLUMN_AUTOSIZE)

boolcol.set_visible(False)
filecol.set_visible(False)

testcol.pack_start(cell1, True)
testcol.set_attributes(cell1, text=1)
testcol.add_attribute(cell1, "editable", 2)#set row editable
testcol.set_expand(True)
testcol.set_sizing(gtk.TREE_VIEW_COLUMN_AUTOSIZE)
testcol.set_visible(False)

###########Scroll Window#########################
scroll = gtk.ScrolledWindow()
scroll.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
scroll.add_with_viewport(leftview)

############Drag and Drop####################
leftview.enable_model_drag_source(gtk.gdk.BUTTON1_MASK, [('text/plain', 0, 0)], gtk.gdk.ACTION_DEFAULT | gtk.gdk.ACTION_MOVE)
leftview.enable_model_drag_dest([('text/plain', 0, 0)], gtk.gdk.ACTION_DEFAULT)
import panelfunctions
leftview.connect("drag_data_get", panelfunctions.get_dragdata)
leftview.connect("drag_data_received", panelfunctions.get_dragdestdata)

###########some variables####################
last_parent = None

#Callbacks
#def dclicked(view, path, column,): #obsolete by Brian's _clicked
	##import rightpanel
	#iter, value = panelfunctions.selected(view)
	#model = view.get_model()
	#list = model.get_value(iter, 0)
	#parent = model.get_value(iter, 3)
	##print list
	##print parent
	#if parent == 'package.' + list:
		#rightpanel.setListModel(parent)
	#else:
		#rightpanel.setListModel(list)

def _clicked(treeview, *args):
	""" Handle treeview clicks """
	global last_parent
	model, iter = treeview.get_selection().get_selected()
	if iter: parent = model.get_value(iter, 3)
	else: parent = last_parent
	# has the selection really changed?
	if parent != last_parent:
		print("LEFTPANEL: parent change detected")
		list = model.get_value(iter, 0)
		#print list
		#print parent
		if parent == 'package.' + list:
			rightpanel.setListModel(parent)
		else:
			rightpanel.setListModel(list)
	else: #fixes bug: if two subfiles are selected after each other with same parent
		list = model.get_value(iter, 0)
		rightpanel.setListModel(list)
	# save current selection as last selected
	last_parent = parent

#can't really edit files names for now...
#def edited_cb(self, cell, path, new_text, user_data, col):
	#self.datastore[path][col] = new_text
	#title("* GPytage")
	#return

#Signals
#leftpanel.cell.connect("edited", self.edited_cb, datastore.datastore, 0)
#leftview.connect("button_press_event", dclicked)
#leftview.connect("row-activated", dclicked)
leftview.connect("cursor-changed", _clicked)

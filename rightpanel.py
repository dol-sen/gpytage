#!/usr/bin/env python
#
# GPytage rightpanel.py module
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
from window import title
from panelfunctions import selected, fileEdited

#rightview = gtk.TreeView(datastore.lists['package.use']) #create the container
rightview = gtk.TreeView()

def setListModel(list): #we need to switch the model on click
	try:
		rightview.set_model()
		rightview.set_model(datastore.lists[list]) #example
		namecol.queue_resize()
		testcol.queue_resize()
		filecol.queue_resize()
	except:
		print 'RIGHTPANEL: setListModel(); failed'
		return

rightview.set_search_column(0) #search broken atm #child?
rightview.set_reorderable(True) # allow inline drag and drop
#columns
namecol = gtk.TreeViewColumn('Value')
testcol = gtk.TreeViewColumn('Flags')
boolcol = gtk.TreeViewColumn() #editable col
filecol = gtk.TreeViewColumn()
#add to tree
rightview.append_column(namecol)
rightview.append_column(testcol)
rightview.append_column(boolcol)
rightview.append_column(filecol)
#render cell
cell = gtk.CellRendererText()
cell1 = gtk.CellRendererText()

#add cols to cell
namecol.pack_start(cell, True)
namecol.set_attributes(cell, text=0)
namecol.add_attribute(cell, "editable", 2)#set row editable
namecol.set_sizing(gtk.TREE_VIEW_COLUMN_AUTOSIZE)

testcol.pack_start(cell1, True)
testcol.set_attributes(cell1, text=1)
testcol.add_attribute(cell1, "editable", 2)#set row editable
testcol.set_expand(True)
testcol.set_sizing(gtk.TREE_VIEW_COLUMN_AUTOSIZE)

boolcol.set_visible(False)
filecol.set_visible(False)

#filecol.pack_start(cell1, True)
#filecol.set_attributes(cell1, text=3)
#filecol.add_attribute(cell1, "editable", 2)#set row editable
#filecol.set_expand(True)
#filecol.set_sizing(gtk.TREE_VIEW_COLUMN_AUTOSIZE)

###########Scroll Window#########################
scroll = gtk.ScrolledWindow()
scroll.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
scroll.add_with_viewport(rightview)

############Drag and Drop####################
rightview.enable_model_drag_source(gtk.gdk.BUTTON1_MASK, [('text/plain', 0, 0)], gtk.gdk.ACTION_DEFAULT | gtk.gdk.ACTION_MOVE)
rightview.enable_model_drag_dest([('text/plain', 0, 0)], gtk.gdk.ACTION_DEFAULT)
import panelfunctions
rightview.connect("drag_data_get", panelfunctions.get_dragdata)
rightview.connect("drag_data_received", panelfunctions.get_dragdestdata)

#Callbacks
def edited_cb(cell, path, new_text, col):
	model = rightview.get_model()
	model[path][col] = new_text
	#Indicate file status
	fileEdited() #edit rightpanel to show status
	title("* GPytage")
	return

def insertrow(arg):
	treeview = rightview
	iter, value = selected(treeview)
	model = treeview.get_model()
	if value == True:
		parent = model.get_value(iter, 3)
		new = model.insert_after(iter, [None, None, True, parent])
		path = model.get_path(new)
		treeview.set_cursor_on_cell(path, namecol, cell, True)
		title("* GPytage")

def deleterow(arg):
	treeview = rightview
	iter, value = selected(treeview)
	model = treeview.get_model()
	if value == True:
		model.remove(iter)
		title("* GPytage")
	
def clicked(view, event):#needs updating from dual panels
	if event.button == 3:
		menu = gtk.Menu()
		irow = gtk.MenuItem("Insert Package")
		irow.connect("activate", insertrow)
		drow = gtk.MenuItem("Delete Package")
		drow.connect("activate", deleterow)
		menu.append(irow)
		menu.append(drow)
		menu.show_all()
		menu.popup(None, None, None, event.button, event.time)

#Signals
cell.connect("edited", edited_cb, 0)
cell1.connect("edited", edited_cb, 1)
rightview.connect("button_press_event", clicked)

#!/usr/bin/env python
#
# GPytage rightpanel.py module
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

from window import setTitleEdited
from PackageFileObj import L_NAME, L_FLAGS, L_REF
#===============================================================================
# from panelfunctions import mselected, fileEdited
#===============================================================================

rightview = gtk.TreeView()
rightselection = rightview.get_selection()

#set MULTIPLE selection mode
rightselection.set_mode(gtk.SELECTION_MULTIPLE)

def setListModel(ListStore): #we need to switch the model on click
	try:
		rightview.set_model() # Clear from view first
		rightview.set_model(ListStore) #example
		namecol.queue_resize()
	except:
		print 'RIGHTPANEL: setListModel(); failed'

rightview.set_search_column(L_NAME)

# TreeViewColumns
namecol = gtk.TreeViewColumn('Value')
useFlagCol = gtk.TreeViewColumn('Flags')

# Add TreeViewColumns to TreeView
rightview.append_column(namecol)
rightview.append_column(useFlagCol)

#render cell
nameCell = gtk.CellRendererText()
nameCell.set_property('editable', True)
flagCell = gtk.CellRendererText()
flagCell.set_property('editable', True)

#add cols to cell
namecol.pack_start(nameCell, True)
namecol.add_attribute(nameCell, 'text', L_NAME)
namecol.set_sizing(gtk.TREE_VIEW_COLUMN_AUTOSIZE)

useFlagCol.pack_start(flagCell, True)
useFlagCol.add_attribute(flagCell, 'text', L_FLAGS)
useFlagCol.set_expand(True)
useFlagCol.set_sizing(gtk.TREE_VIEW_COLUMN_AUTOSIZE)

# ScrolledWindow
scroll = gtk.ScrolledWindow()
scroll.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
scroll.add_with_viewport(rightview)

###########Drag and Drop####################
#===============================================================================
# rightview.set_reorderable(True) # allow inline drag and drop
# rightview.enable_model_drag_source(gtk.gdk.BUTTON1_MASK, [('text/plain', 0, 0)], gtk.gdk.ACTION_DEFAULT | gtk.gdk.ACTION_MOVE)
# rightview.enable_model_drag_dest([('text/plain', 0, 0)], gtk.gdk.ACTION_DEFAULT)
# import panelfunctions
# rightview.connect("drag_begin", panelfunctions.drag_begin_signal)
# rightview.connect("drag_data_delete", panelfunctions.drag_data_delete_signal)
# rightview.connect("drag_data_received", panelfunctions.get_dragdestdata)
#===============================================================================

#Callbacks
def edited_cb(cell, path, new_text, col):
	""" Indicate file has been edited """
	model = rightview.get_model()
	model[path][col] = new_text
	model[path][E_MODIFIED] = True
	#Indicate file status
	fileEdited() #edit rightpanel to show status
	title("* GPytage")
	return

def insertrow(arg):
	""" Insert row below selected row(s) """
	treeview = rightview
	model, iterdict = mselected(treeview)
	for iter,value in iterdict.iteritems(): #Should only have 1 via right click.. funky results with accelerator.
		if value == True:
			parent = model.get_value(iter, E_PARENT)
			new = model.insert_after(iter, new_entry(parent=parent))
			path = model.get_path(new)
			treeview.set_cursor_on_cell(path, namecol, cell, True)
			title("* GPytage")

def deleterow(arg):
	""" Delete selected row(s) """
	treeview = rightview
	model, iterdict = mselected(treeview)
	for iter,value in iterdict.iteritems():
		if value == True:
			model.remove(iter)
			fileEdited()
			title("* GPytage")

def commentRow(window):
	""" Comment selected row(s) """
	treeview = rightview
	model, iterdict = mselected(treeview)
	for iter,value in iterdict.iteritems():
		if value == True:
			old = model.get_value(iter, E_NAME)
			if old.startswith("#") is False:
				model.set_value(iter, E_NAME, "#"+old)
				fileEdited()
				title("* GPytage")

def uncommentRow(window):
	""" Uncomment selected row(s) """
	treeview = rightview
	model, iterdict = mselected(treeview)
	for iter,value in iterdict.iteritems():
		if value == True:
			old = model.get_value(iter, E_NAME)
			if old.startswith("#"):
				model.set_value(iter, E_NAME, old[1:])
				fileEdited()
				title("* GPytage")

def clicked(view, event):#needs updating from dual panels
	""" Right click menu for rightview """
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
nameCell.connect("edited", edited_cb, L_NAME)
flagCell.connect("edited", edited_cb, L_FLAGS)
rightview.connect("button_press_event", clicked)

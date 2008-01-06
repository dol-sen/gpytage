#!/usr/bin/env python
#
# GPytage panelfunctions.py module
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
import pdb
import datastore

def get_dragdata(treeview, context, selection, target_id, etime):
	iter, value = selected(treeview)
	model = treeview.get_model()
	print treeview
	if value == True:
		global data
		data = []
		data.append(model.get_value(iter, 0))
		data.append(model.get_value(iter, 1))
		data.append(model.get_value(iter, 2))
		data.append(model.get_value(iter, 3))
		selection.set(selection.target, 0, str(data[0]))
		selection.set(selection.target, 1, str(data[1]))
		selection.set(selection.target, 2, str(data[2]))
		selection.set(selection.target, 2, str(data[3]))

def get_dragdestdata(treeview, context, x, y, selection, info, etime):
	iter, value = selected(treeview)
	model = treeview.get_model()
	#print treeview
	if value == True:
		ldata = data
		drop_info = treeview.get_dest_row_at_pos(x,y)
		if drop_info:
			path, position = drop_info
			iteri = model.get_iter(path)
			if model.get_value(iteri, 2):
				if (position == gtk.TREE_VIEW_DROP_BEFORE or position == gtk.TREE_VIEW_DROP_INTO_OR_BEFORE):
					model.insert_before(iteri, ldata)
					#print 'before'
				else:
					model.insert_after(iteri, ldata)
					#print 'after'
			else:
				return
		else:
			model.append([data])
			#print 'else'
		from window import title
		title("* GPytage")
		if context.action == gtk.gdk.ACTION_MOVE:
			context.finish(True, True, etime)
		return

def selected(treeview): #helper function
	selection = treeview.get_selection()
	model, iter = selection.get_selected()
	try:
		value = model.get_value(iter, 2)
	except:
		value = False
	return iter, value

def fileEdited(): #leftpanel
	from leftpanel import leftview
	model = leftview.get_model()
	iter, value = selected(leftview)
	oldName = model.get_value(iter, 0).strip('*')
	newName = "*%s" % oldName
	model.set_value(iter, 0, newName)

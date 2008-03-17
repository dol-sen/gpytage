#!/usr/bin/env python
#
# GPytage panelfunctions.py module
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
import pdb
import datastore

#def get_dragdata(treeview, context, selection, target_id, etime): #not used anymore
#	model, iterdict = mselected(treeview)
#	print "fmodel",model
#	print "GET_DRAGDATA"
#	for iter,value in iterdict.iteritems():
#		print iter,value,"ITERLOOP"
#		if value == True:
#			global data
#			data = []
#			data.append(model.get_value(iter, 0))
#			data.append(model.get_value(iter, 1))
#			data.append(model.get_value(iter, 2))
#			data.append(model.get_value(iter, 3))
#			selection.set(selection.target, 0, str(data[0]))
#			selection.set(selection.target, 1, str(data[1]))
#			selection.set(selection.target, 2, str(data[2]))
#			selection.set(selection.target, 2, str(data[3]))
#			print data,"DATA FROM DRAGDATA"

def get_dragdestdata(treeview, context, x, y, selection, info, etime):
	iter, value = cselected(treeview,x,y)
	model = treeview.get_model()
	print "model",model
	if value == True:
		ldata = data
		print data,"global data"
		print selection.data,"selection data"
		drop_info = treeview.get_dest_row_at_pos(x,y)
		print "eep"
		if drop_info:
			path, position = drop_info
			iteri = model.get_iter(path)
			if model.get_value(iteri, 2):
				if (position == gtk.TREE_VIEW_DROP_BEFORE or position == gtk.TREE_VIEW_DROP_INTO_OR_BEFORE):
					model.insert_before(iteri, ldata)
				else:
					model.insert_after(iteri, ldata)
			else:
				return
		else:
			model.append([data])
			print 'else'
		from window import title
		title("* GPytage")
		fileEdited()
		if context.action == gtk.gdk.ACTION_MOVE:
			context.finish(True, True, etime)
		return
	else:
		# rightpanel -> leftpanel logic goes here.
		parent = model.get_value(iter, 3).strip('*')
		oldName = model.get_value(iter, 0).strip('*')
		print parent
		if model.iter_children(iter):#has children [subfiles]
			print "has children"
		else: #doesn't have children
			newName = "*%s" % oldName
			model.set_value(iter, 0, newName)
			# append the data
			print data,"DATA TO APPEND"
			datastore.lists[oldName].append(data)
			print "appended"
			#nuke what we moved
			from leftpanel import leftview
			bmodel.remove(biter)
			lmodel = leftview.get_model()
			lselection.select_path(lmodel.get_path(lselected[1]))
			fileEdited()


def drag_begin_signal(treeview, dragcontext, *args):
	""" Grab model and data begin dragged """
	model, iterdict = mselected(treeview)
	global bmodel
	global data
	global biter
	global lselection
	global lselected
	from leftpanel import leftview
	lselection = leftview.get_selection()
	lselected = lselection.get_selected()
	bmodel = model
	data = []
	for iter,value in iterdict.iteritems():
		data.append(model.get_value(iter, 0))
		data.append(model.get_value(iter, 1))
		data.append(model.get_value(iter, 2))
		data.append(model.get_value(iter, 3))
		biter = iter
	print model,"BEGIN MODEL",data,"BEGIN DATA"

def drag_data_delete_signal(*args):
	""" Delete begin signals data """
	bmodel.remove(biter)
	

def cselected(treeview, x, y):
	""" Return iter:value from current coordinates """
	selection = treeview.get_dest_row_at_pos(x,y) #tuple path,dropposition
	model = treeview.get_model()
	iter = model.get_iter(selection[0])
	try:
		value = model.get_value(iter,2)
	except:
		value = False
	print model.get_value(iter,0)
	return iter,value


def selected(treeview): #helper function
	""" Return iter of currently selected row """
	selection = treeview.get_selection()
	model, iter = selection.get_selected()
	try:
		value = model.get_value(iter, 2)
	except:
		value = False
	return iter, value

def mselected(treeview):
	""" Return model and dictionary of iters:values from currently selected rows """
	selection = treeview.get_selection()
	model, iters = selection.get_selected_rows() #iters == paths
	iterdict = {}
	for i in iters:
		iref = gtk.TreeRowReference(model, i)
		iter = model.get_iter(i)
		try:
			iterdict[iter] = model.get_value(iter, 2)
		except:
			iterdict[iter] = False
	return model, iterdict

def fileEdited(): #leftpanel
	""" Mark a file as edited """
	from leftpanel import leftview
	model = leftview.get_model()
	iter, value = selected(leftview)
	oldName = model.get_value(iter, 0).strip('*')
	newName = "*%s" % oldName
	model.set_value(iter, 0, newName)

def switchListView(widget, drag_context, x, y, timestamp, *args):
	""" Hilights leftview drop target during drag operation """
	from leftpanel import leftview
	import rightpanel
	model = leftview.get_model()
	path = leftview.get_dest_row_at_pos(x, y)
	leftview.expand_row(path[0], True)
	#iter = model.get_iter(path[0])
	treeselection = leftview.get_selection()
	treeselection.select_path(path[0])


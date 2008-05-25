#!/usr/bin/env python
#
# GPytage subfile module
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
from window import title, unsavedDialog, window
from save import SaveFile
from helper import folder_scan, folder_walk
from config import get_config_path, config_files

def new(window):
	""" Spawn the new subfile dialog """
	newd = gtk.Dialog('Create new Subfile', window, gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT, None)
	dirs,files = folder_scan()
	cb = gtk.combo_box_new_text()
	for i in dirs:
		cb.append_text(i)
		
	cb.set_active(0)
	sbox = gtk.HBox()
	sbox.pack_start(gtk.Label("Parent directory:"))
	sbox.pack_start(cb)
	newd.vbox.pack_start(sbox)
	ftextbox = gtk.HBox()
	flabel = gtk.Label("New subfile name:")
	ftext = gtk.Entry()
	ftextbox.pack_start(flabel)
	ftextbox.pack_start(ftext)

	newd.vbox.pack_start(ftextbox)
	addb = gtk.Button("Add", gtk.STOCK_ADD)
	closeb = gtk.Button("Close",gtk.STOCK_CLOSE)
	addb.connect("clicked", add_subfile, cb, ftext, newd, window)
	closeb.connect("clicked", close_subfile, newd)
	newd.action_area.pack_start(closeb)
	newd.action_area.pack_start(addb)
	
	if dirs == []:
		from window import statusbar
		sbar, smsg = statusbar()
		sbar.pop(smsg)
		sbar.push(smsg, "Warning: No parent directories detected")
		sbar.show()
		newd.vbox.pack_start(sbar)
	
	newd.show_all()
	newd.run()

def close_subfile(arg, newd):
	""" Close subfile dialog """
	newd.hide()

def add_subfile(arg, cb, ftext, newd, window):
	model = cb.get_model()
	index = cb.get_active()
	if index >= 0: # prevent index errors
		# next line gets an index error when trying to add a subfile to a non existent sets dir. (Or if selection is blank)
		cbselection =  model[index][0] #current selection
		ftextselection = ftext.get_text()
		Success = False
		if len(ftextselection):
			addToMemory(cbselection, ftextselection)
			newd.hide()

def addToMemory(parent, filename):
	""" Adds new subfile to memory """
	datastore.datastore.foreach(findMatch, [parent, filename])
	msg= '#This file was created by GPytage'
	datastore.lists[filename] = gtk.ListStore(str, str, bool, str)
	datastore.lists[filename].append([msg, None, True, parent]) #rightpanel stuff
	title("* GPytage")

def findMatch(model, path, iter, user_data):
	print user_data[0], user_data[1]
	print model.get_value(iter, 0).strip('*')
	if model.get_value(iter, 0).strip('*') == user_data[0]:
		edited_file = "*%s" % user_data[1]
		model.append(iter, [edited_file, None, False, user_data[0]])

def convert(window):
	""" Spawn the convert file dialog """
	convertd = gtk.Dialog('Convert file to subfile', window, gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT, None)
	convertd.vbox.pack_start(gtk.Label("This will convert a normal file to a subfile under a directory named after the original file. \nWarning: This operation cannot be undone\n"))

	dirs,files = folder_scan()
	cb = gtk.combo_box_new_text() #combobox with files that are NOT subfiles
	for i in files:
		cb.append_text(i)
	cb.set_active(0)
	
	tbox = gtk.HBox()
	tbox.pack_start(gtk.Label("File to be converted:"))
	tbox.pack_start(cb)

	newfile = gtk.Label("Please rename old file:")
	ftext = gtk.Entry()

	#main box to hold stuff
	cbox = gtk.HBox()
	cbox.pack_start(newfile)
	cbox.pack_start(ftext)
	convertd.vbox.pack_start(tbox)
	convertd.vbox.pack_start(cbox)
	#pack action area with buttons
	convertb = gtk.Button("Convert", gtk.STOCK_CONVERT)
	closeb = gtk.Button("Close",gtk.STOCK_CLOSE)
	convertb.connect("clicked", convertFile, cb, ftext, convertd, window)
	closeb.connect("clicked", close_subfile, convertd)

	if files == []:
		from window import statusbar
		sbar, smsg = statusbar()
		sbar.pop(smsg)
		sbar.push(smsg, "Warning: No files detected")
		sbar.show()
		convertd.vbox.pack_start(sbar)

	convertd.action_area.pack_start(closeb)
	convertd.action_area.pack_start(convertb)

	convertd.show_all()
	convertd.run()

def convertFile(arg, cb, ftext, convertd, window):
	""" Convert Top level file to directory with subfile """
	#Currently I don't see how to do such a change "in memory", so the change must be done live and probably call the evil reload() nuke
	model = cb.get_model()
	index = cb.get_active()
	if index >= 0: # prevent index errors
		cbselection =  model[index][0] #current selected item
		ftextselection = ftext.get_text()
		if window.get_title() != "GPytage":
			status, uD = unsavedDialog()
			if status == -8:
				uD.hide()
			elif status == 1:
				SaveFile().save()
				uD.hide()
			else:
				uD.hide()
				return
		if len(ftextselection):
			#create an old file
			nfile = ftextselection
			from shutil import move
			from os import mkdir
			from config import get_config_path
			from helper import reload
			pconfig = get_config_path()
			move(pconfig+cbselection, pconfig+nfile) #rename the file
			mkdir(pconfig+cbselection) #create the parent directory
			move(pconfig+nfile, "%s/%s" %(pconfig+cbselection,nfile))
			reload() #sigh
			convertd.hide()

def delete(window):
	""" Spawn the delete subfile dialog """
	deld = gtk.Dialog('Delete Subfile', window, gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT, None)
	dirs,files = folder_scan()
	cb = gtk.combo_box_new_text()

	subfiles = []
	for i in dirs:
		data = folder_walk(i)
		for i in data:
			subfiles.append(i)
	cb = gtk.combo_box_new_text()
	for i in subfiles:
		cb.append_text(i)
	cb.set_active(0)

	sbox = gtk.HBox()
	sbox.pack_start(gtk.Label("File to delete:"))
	sbox.pack_start(cb)
	deld.vbox.pack_start(sbox)

	if subfiles == []:
		from window import statusbar
		sbar, smsg = statusbar()
		sbar.pop(smsg)
		sbar.push(smsg, "Warning: No files detected")
		sbar.show()
		deld.vbox.pack_start(sbar)

	remb = gtk.Button("Add", gtk.STOCK_DELETE)
	closeb = gtk.Button("Close",gtk.STOCK_CLOSE)
	remb.connect("clicked", deleteFile, cb, deld, window)
	closeb.connect("clicked", close_subfile, deld)
	deld.action_area.pack_start(closeb)
	deld.action_area.pack_start(remb)
	deld.show_all()
	deld.run()

def deleteFile(arg, cb, deld, window):
	""" Delete subfile """
	model = cb.get_model()
	index = cb.get_active()
	if index >= 0: # prevent index errors
		if window.get_title() != "GPytage":
			status, uD = unsavedDialog()
			if status == -8:
				uD.hide()
			elif status == 1:
				SaveFile().save()
				uD.hide()
			else:
				uD.hide()
				return
	from os import remove
	from config import get_config_path
	from helper import reload
	pconfig = get_config_path() # /
	
	global ddata
	ddata = None
	def findMatch(model, path, iter, user_data):
		""" Get path, iter for the file to be deleted """
		if model.get_value(iter, 0).strip('*') == user_data[0]:
			global ddata
			ddata = [model, path, iter]
			return True
	datastore.datastore.foreach(findMatch, [model[index][0]])
	if ddata:
		model = ddata[0]
		path = ddata[1]
		iter = ddata[2]
		filePath = pconfig+model.get_value(iter, 3)+'/'+model.get_value(iter, 0).strip('*')
		remove(filePath)
		print "deleteFILE: %s DELETED" % filePath
		reload()
		deld.hide()


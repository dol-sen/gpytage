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
import gtk.glade
import datastore
from datastore import E_NAME, E_DATA, E_EDITABLE, E_PARENT, E_MODIFIED
from window import title, unsavedDialog, window
from save import SaveFile
from helper import folder_scan, folder_walk
from config import get_config_path, config_files

def new(window, GLADE_PATH):
	""" Spawn the new subfile dialog """
	gladefile = GLADE_PATH + "newsubfile.glade"  
	wTree = gtk.glade.XML(gladefile) 
	newd = wTree.get_widget("newfile")
	dirs,files = folder_scan()
	cb = wTree.get_widget("ncb")
		
	model = gtk.ListStore(str)
	cb.set_model(model)
	cell = gtk.CellRendererText()
	cb.pack_start(cell)
	cb.add_attribute(cell, 'text', 0)
	
	for i in dirs:
		cb.append_text(i)
		
	cb.set_active(0)

	ftext = wTree.get_widget("aentry")

	addb = wTree.get_widget("addb")
	closeb = wTree.get_widget("closeb")
	
	addb.connect("clicked", add_subfile, cb, ftext, newd, window)
	closeb.connect("clicked", close_subfile, newd)
	
	if dirs == []:
		sbar = wTree.get_widget("sbar")
		smsg = sbar.get_context_id("standard message")
		sbar.pop(smsg)
		sbar.push(smsg, "Error: No parent directories found")
		sbar.show()
	
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
		cbselection =  model[index][E_NAME] #current selection
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
	print user_data[E_NAME], user_data[E_DATA]
	print model.get_value(iter, E_NAME).strip('*')
	if model.get_value(iter, E_NAME).strip('*') == user_data[E_NAME]:
		edited_file = "*%s" % user_data[E_DATA]
		model.append(iter, [edited_file, None, False, user_data[E_NAME], True])

def convert(window, GLADE_PATH):
	""" Spawn the convert file dialog """
	gladefile = GLADE_PATH + "convertfile.glade"  
	wTree = gtk.glade.XML(gladefile) 
	convertd = wTree.get_widget("convertd")

	dirs,files = folder_scan()
	cb = wTree.get_widget("ncb")
	
	model = gtk.ListStore(str)
	cb.set_model(model)
	cell = gtk.CellRendererText()
	cb.pack_start(cell)
	cb.add_attribute(cell, 'text', E_NAME)
	
	for i in files:
		cb.append_text(i)
	cb.set_active(0)
	
	ftext = wTree.get_widget("aentry")

	convertb = wTree.get_widget("convertb")
	closeb = wTree.get_widget("closeb")
	
	convertb.connect("clicked", convertFile, cb, ftext, convertd, window)
	closeb.connect("clicked", close_subfile, convertd)

	if files == []:
		sbar = wTree.get_widget("sbar")
		smsg = sbar.get_context_id("standard message")
		sbar.pop(smsg)
		sbar.push(smsg, "Error: No files detected")
		sbar.show()

	convertd.show_all()
	convertd.run()

def convertFile(arg, cb, ftext, convertd, window):
	""" Convert Top level file to directory with subfile """
	#Currently I don't see how to do such a change "in memory", so the change must be done live and probably call the evil reload() nuke
	model = cb.get_model()
	index = cb.get_active()
	if index >= 0: # prevent index errors
		cbselection =  model[index][E_NAME] #current selected item
		ftextselection = ftext.get_text()
		if window.get_title() != "GPytage":
			status, uD = unsavedDialog()
			if status == -8:
				uD.hide()
			elif status == 1:
				SaveFile().saveModified()
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

def delete(window, GLADE_PATH):
	""" Spawn the delete subfile dialog """
	gladefile = GLADE_PATH + "deletefile.glade"  
	wTree = gtk.glade.XML(gladefile) 
	deld = wTree.get_widget("deld")
	
	dirs,files = folder_scan()

	cb = wTree.get_widget("ncb")
	
	model = gtk.ListStore(str)
	cb.set_model(model)
	cell = gtk.CellRendererText()
	cb.pack_start(cell)
	cb.add_attribute(cell, 'text', E_NAME)

	subfiles = []
	for i in dirs:
		data = folder_walk(i)
		for i in data:
			subfiles.append(i)
				
	for i in subfiles:
		cb.append_text(i)
	cb.set_active(0)

	if subfiles == []:
		sbar = wTree.get_widget("sbar")
		smsg = sbar.get_context_id("standard message")
		sbar.pop(smsg)
		sbar.push(smsg, "Error: No files detected")
		sbar.show()

	remb = wTree.get_widget("delb")
	closeb = wTree.get_widget("closeb")
	
	remb.connect("clicked", deleteFile, cb, deld, window)
	closeb.connect("clicked", close_subfile, deld)
	
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
				SaveFile().saveModified()
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
		if model.get_value(iter, E_NAME).strip('*') == user_data[E_NAME]:
			global ddata
			ddata = [model, path, iter]
			return True
	datastore.datastore.foreach(findMatch, [model[index][E_NAME]])
	if ddata:
		model = ddata[E_NAME]
		path = ddata[E_DATA]
		iter = ddata[E_EDITABLE]
		filePath = pconfig+model.get_value(iter, E_PARENT)+'/'+model.get_value(iter, E_NAME).strip('*')
		remove(filePath)
		print "deleteFILE: %s DELETED" % filePath
		reload()
		deld.hide()


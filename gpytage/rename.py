#!/usr/bin/env python
#
# GPytage rename.py module
#
############################################################################
#    Copyright (C) 2008 by Kenneth Prugh, Brian Dolbec                     #
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
from datastore import E_NAME, E_DATA, E_EDITABLE, E_PARENT, E_MODIFIED
from helper import folder_scan, folder_walk
from config import get_config_path, config_files
from save import SaveFile
from window import title, unsavedDialog, window, error_dialog

class rename: #this is mostly just a test... this may be removed entirely
	#Ideally we should be able to rename a file with rightclick/current selected
	def renameDialog(self, window, GLADE_PATH):
		gladefile = GLADE_PATH + "renamefile.glade"  
		wTree = gtk.glade.XML(gladefile) 
		rDialog = wTree.get_widget("renamed")
		
		cb = wTree.get_widget("ncb")
		
		model = gtk.ListStore(str)
		cb.set_model(model)
		cell = gtk.CellRendererText()
		cb.pack_start(cell)
		cb.add_attribute(cell, 'text', 0)
		
		dirs,files = folder_scan()

		subfiles = []
		
		for i in dirs:
			data = folder_walk(i)
			for i in data:
				subfiles.append(i)
		
		for i in subfiles:
			cb.append_text(i)
		cb.set_active(0)

		ftext = wTree.get_widget("aentry")

		addb = wTree.get_widget("renameb")
		closeb = wTree.get_widget("closeb")
		
		addb.connect("clicked", self.renameFile, cb, ftext, rDialog, window)
		closeb.connect("clicked", self.close_renameD, rDialog)

		sbar = wTree.get_widget("sbar")
		#sbar.hide()
		if subfiles == []:
			smsg = sbar.get_context_id("standard message")
			sbar.pop(smsg)
			sbar.push(smsg, "Error: No subfiles detected")
			sbar.show()

		rDialog.show_all()
		rDialog.run()

	def close_renameD(self, arg, rDialog):
			rDialog.hide()

	def renameFile(self, arg, cb, ftext, rDialog, window):
		model = cb.get_model()
		index = cb.get_active()
		if index >= 0: # prevent index errors
			oldName =  model[index][E_NAME]
			newName = ftext.get_text()
			#model[index][E_MODIFIED] = True
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
			if len(newName):
				#inline function to get our values
				def findMatch(model, path, iter, user_data):
					if model.get_value(iter, E_NAME).strip('*') == user_data[E_NAME]:
						self.data = [model, path, iter]
						return True
					return False
				datastore.datastore.foreach(findMatch, [oldName, newName])
				if self.data:
					model = self.data[0]
					path = self.data[1]
					iter = self.data[2]
					from shutil import move
					from config import get_config_path
					from helper import reload
					pconfig = get_config_path() # /
					if model.get_value(iter, E_NAME) == model.get_value(iter, E_PARENT):
						#technically this wont ever execute the way I have it now
						print "RENAME: FILE MATCH"
						filePath = pconfig+model.get_value(iter, E_NAME)
						try:
							errors = []
							move(filePath, pconfig+newName)
						except IOError, e:
							errors.append(str(e))
							error_dialog(errors)
					else:
						print "RENAME: FILE NOMATCH"
						filePath = pconfig+model.get_value(iter, E_PARENT)+'/'+model.get_value(iter, E_NAME)
						try:
							errors = []
							move(filePath, pconfig+model.get_value(iter, E_PARENT)+'/'+newName)
							reload() #will nuke unsaved changes, implement a unsaved changes dialog?
						except IOError, e:
							errors.append(str(e))
							error_dialog(errors)
					rDialog.hide()


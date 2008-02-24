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
from helper import folder_scan, folder_walk
from config import get_config_path, config_files
from save import SaveFile
from window import title, unsavedDialog, window

class rename: #this is mostly just a test... this may be removed entirely
	#Ideally we should be able to rename a file with rightclick/current selected
	def renameDialog(self, window):
		rDialog = gtk.Dialog('Rename File', window, gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT, None)
		dirs,files = folder_scan()
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
		sbox.pack_start(gtk.Label("File to rename"))
		sbox.pack_start(cb)
		rDialog.vbox.pack_start(sbox)
		ftextbox = gtk.HBox()
		flabel = gtk.Label("New name:")
		ftext = gtk.Entry()
		ftextbox.pack_start(flabel)
		ftextbox.pack_start(ftext)

		rDialog.vbox.pack_start(ftextbox)
		addb = gtk.Button("Rename", "_Rename")
		closeb = gtk.Button("Cancel",gtk.STOCK_CLOSE)
		addb.connect("clicked", self.renameFile, cb, ftext, rDialog, window)
		closeb.connect("clicked", self.close_renameD, rDialog)
		rDialog.action_area.pack_start(closeb)
		rDialog.action_area.pack_start(addb)
		rDialog.show_all()
		rDialog.run()

	def close_renameD(self, arg, rDialog):
			rDialog.hide()

	def renameFile(self, arg, cb, ftext, rDialog, window):
		model = cb.get_model()
		index = cb.get_active()
		if index >= 0: # prevent index errors
			oldName =  model[index][0]
			newName = ftext.get_text()
			if window.get_title() =! "GPytage":
				status, uD = unsavedDialog()
				if status == -8:
					uD.hide()
				elif status == 1:
					SaveFile().save()
					uD.hide()
				else:
					uD.hide()
					return
			if len(newName):
				#inline function to get our values
				def findMatch(model, path, iter, user_data):
					if model.get_value(iter, 0).strip('*') == user_data[0]:
						self.data = [model, path, iter]
						return True
				datastore.datastore.foreach(findMatch, [oldName, newName])
				if self.data:
					model = self.data[0]
					path = self.data[1]
					iter = self.data[2]
					from shutil import move
					from config import get_config_path
					from helper import reload
					pconfig = get_config_path() # /
					if model.get_value(iter, 0) == model.get_value(iter, 3):
						#technically this wont ever execute the way I have it now
						print "RENAME: FILE MATCH"
						filePath = pconfig+model.get_value(iter, 0)
						move(filePath, pconfig+newName)
					else:
						print "RENAME: FILE NOMATCH"
						filePath = pconfig+model.get_value(iter, 3)+'/'+model.get_value(iter, 0)
						move(filePath, pconfig+model.get_value(iter, 3)+'/'+newName)
					reload() #will nuke unsaved changes, implement a unsaved changes dialog?
					rDialog.hide()


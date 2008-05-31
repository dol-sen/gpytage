#!/usr/bin/env python
#
# GPytage save.py module
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

import os.path
import sys

from helper import reload
from config import get_config_path
from window import title, window, createMessageDialog
import gtk
from leftpanel import leftview


class SaveFile:
	def __init__(self):
		self.errors = []
		
	def save(self):
		import datastore
		lists = datastore.lists
		for name,store in lists.iteritems():
			try:
				if name == store[0][3]:#I'm a main file
					file = name
					data = []
					parent = None
					for row in store:
						datarow = self.assemblerow(row)
						data.append(datarow)
					self.savefile(parent, file, data)
					model = leftview.get_model()
					model.foreach(self.findMatch, name)
				else: #we have a subfile
					parent = store[0][3] #main dir
					file = name #sub file
					data = []
					for row in store:
						datarow = self.assemblerow(row)
						data.append(datarow)
					self.savefile(parent, file, data)
					model = leftview.get_model()
					model.foreach(self.findMatch, name)
			except IndexError:
				#when a file is "blank" and a save is attempted it fails here. This should be the only case...
				print name,store
				model = leftview.get_model()
				model.foreach(self.findMatch, name)
				piter = model.iter_parent(self.fiter)
				if piter:
					#has parent
					parent = model.get_value(piter, 0)
				else:
					#no parent
					parent = None	
				data = "\n"
				self.savefile(parent, name, data)

		title("GPytage")
		if self.errors != []:
			#spawn dialog
			err = ',\n'.join(self.errors)
			message = "The following files failed to save:\n\n%s. \n\nPossible causes may include insufficient privileges to write to these files." %err
			createMessageDialog(None, gtk.DIALOG_DESTROY_WITH_PARENT, gtk.MESSAGE_ERROR, gtk.BUTTONS_OK, "Error Saving...", message)

	def assemblerow(self, child):
		""" Assemble data columns for saving """
		try:
			len(child[0])
			text1 = child[0]
		except:
			text1 = ""
		try:
			len(child[1])
			text2 = child[1]
		except:
			text2 = ""
		datarow = text1 + " " + text2 + '\n'
		return datarow

	def savefile(self, parent, file, data):
		""" Write data to file """
		config_path = get_config_path()
		if parent is None: #main file
			try:
				f=open(config_path + file, 'w')
				for row in data:
					f.write(row)
				f.close
			except IOError:
				self.errors.append("%s%s" % (config_path, file))
				return
		else: #subfile
			try:
				f=open(config_path + parent + '/' + file, 'w')
				for row in data:
					f.write(row)
				f.close
			except IOError:
				self.errors.append("%s%s/%s" %(config_path, parent, file))
				return

	def findMatch(self, model, path, iter, user_data):
		if model.get_value(iter, 0).strip('*') == user_data:
			model.set_value(iter, 0, user_data)
			self.fiter = iter


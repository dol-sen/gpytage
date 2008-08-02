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
from sys import stderr

from helper import reload
from config import get_config_path
from window import title, window, createMessageDialog, error_dialog
import gtk
from leftpanel import leftview
import datastore
from datastore import E_NAME, E_DATA, E_EDITABLE, E_PARENT, E_MODIFIED

class SaveFile:
	def __init__(self):
		self.errors = []
		
	def save(self, name):
		lists = datastore.lists
		try:
			store = lists[name]
		except: # key error
			print >>stderr, name, " was not found in lists... returning"
			return False
		try:
			if name == store[0][E_PARENT]:#I'm a main file
				file = name
				data = []
				parent = None
				for row in store:
					datarow = self.assemblerow(row)
					data.append(datarow)
					row[E_MODIFIED] = False
				success = self.savefile(parent, file, data)
			else: #we have a subfile
				parent = store[0][E_PARENT] #main dir
				file = name #sub file
				data = []
				for row in store:
					datarow = self.assemblerow(row)
					data.append(datarow)
					row[E_MODIFIED] = False
				success = self.savefile(parent, file, data)
		except IndexError:
			#when a file is "blank" and a save is attempted it fails here. This should be the only case...
			print name,store
			model = leftview.get_model()
			piter = model.iter_parent(self.fiter)
			if piter:
				#has parent
				parent = model.get_value(piter, E_NAME)
			else:
				#no parent
				parent = None	
			data = "\n"
			success = self.savefile(parent, name, data)
		return success

	def assemblerow(self, child):
		""" Assemble data columns for saving """
		try:
			len(child[E_NAME])
			text1 = child[E_NAME]
		except:
			text1 = ""
		try:
			len(child[E_DATA])
			text2 = child[E_DATA]
		except:
			text2 = ""
		datarow = text1 + " " + text2 + '\n'
		return datarow

	def savefile(self, parent, file, data):
		""" Write data to file """
		print "savefile(), parent=", parent, " file=", file
		config_path = get_config_path()
		if parent is None: #main file
			file_path = config_path + file
		else: #subfile
			file_path = config_path + parent + '/'  + file
		try:
			f=open(file_path, 'w')
			for row in data:
				f.write(row)
			f.close
		except IOError, e:
			print >>stderr, "savefile(), got an error: ", e
			#self.errors.append("%s%s/%s, error = %s" %(config_path, parent, file, e))
			self.errors.append(str(e))
			return False
		return True

	def saveModified(self):
		model = leftview.get_model()
		model.foreach(self.checkModified)
		print >>stderr, "made it thru model.foreach().  checking for errors: ", self.errors
		if self.errors != []:
			#spawn dialog
			error_dialog(self.errors)
		else:
			title("GPytage")

	def checkModified(self, model, path, iter, *user_data):
		print >>stderr, model.get_value(iter, E_NAME), ' ', model.get_value(iter, E_MODIFIED)
		if model.get_value(iter, E_MODIFIED):
			name = model.get_value(iter, E_NAME).strip('*')
			print >>stderr, "found a modified file... saving: ", name
			self.fiter = iter
			suceeded = self.save(name)
			if suceeded:
				model.set_value(iter, E_NAME, name)
				model.set_value(iter, E_MODIFIED, False)
		return


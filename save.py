#!/usr/bin/env python
#
# GPytage save.py module
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

import os.path
import sys
import pdb

from helper import portage_path, reload
from window import title, window, createMessageDialog
import gtk

class SaveFile():
	def __init__(self):
		self.errors = []
		
	def save(self): #the important one...
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
				else: #we have a subfile
					parent = store[0][3] #main dir
					file = name #sub file
					data = []
					for row in store:
						datarow = self.assemblerow(row)
						data.append(datarow)
					self.savefile(parent, file, data)
			except IndexError:
				print 'Failed to save the file %s for write access' % name
		reload()
		if self.errors != []:
			#spawn dialog
			err = ',\n'.join(self.errors)
			message = "The following files failed to save:\n\n%s. \n\nPossible causes may include insufficient privileges to write to these files." %err
			createMessageDialog(None, gtk.DIALOG_DESTROY_WITH_PARENT, gtk.MESSAGE_ERROR, gtk.BUTTONS_OK, "Erroring Saving...", message)
	#insight: datastore can be thought of a giant list, where row[0] references the first item in a multi list list. eg: foo = [['blah'],['blah1']]

	def assemblerow(self, child):
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
		if parent is None: #main file
			try:
				f=open(portage_path + file, 'w')
				for row in data:
					f.write(row)
				f.close
			except IOError:
				self.errors.append("%s%s" % (portage_path, file))
				return
		else: #subfile
			try:
				f=open(portage_path + parent + '/' + file, 'w')
				for row in data:
					f.write(row)
				f.close
			except IOError:
				self.errors.append("%s%s/%s" %(portage_path, parent, file))
				return

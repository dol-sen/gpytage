#!/usr/bin/env python
#
# GPytage helper.py module
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

import os
import pygtk; pygtk.require("2.0")
import gtk
from config import get_config_path, config_files
import config
import os

def folder_scan():#returns what files are files/dirs wrt portage
	config_path = get_config_path()
	dirs = []
	file = []
	for i in config_files:
		result = os.path.isdir(config_path+i)
		if(result):
			dirs.append(i)
		elif(os.access(config_path+i, os.F_OK)):
			file.append(i)
		else:
			print "%s DOES NOT EXIST" % i
			continue
	return dirs, file

def folder_walk(dir):#returns list of files within dirs
	config_path = get_config_path()
	dir_files = []
	for i in os.listdir(config_path+dir):
		dir_files.append(i)
	return dir_files

def reload():
	import datastore
	datastore.datastore.clear()
	for name, store in datastore.lists.iteritems():
		store.clear()
	datastore.create_treeiter()
	datastore.create_lists()
	from window import title
	title("GPytage")

def scan_contents(arg):#returns data in specified file
	config_path = get_config_path()
	fmessage = ""
	writemessage = ""
	try:
		f=open(config_path+arg, 'r')
		contents = f.readlines()
		f.close()
	except IOError: #needed or everything breaks
		from window import createMessageDialog
		if arg != 'sets': # 'sets' is not critical
			print 'HELPER: scan_contents(); Warning: Critical file %s%s not found' % (config_path, arg)
			writemessage = '''# This file was created by GPytage as it is required for proper operation.'''
		try:
			if arg != "sets":
				f=open(config_path + arg, 'w')
				f.write(writemessage)
				f.close
				fail = 1
			else:
				print "HELPER: scan_contents(); the sets directory is not being created automatically in " + config_path
				#os.mkdir('%s/sets' % config_path)
				data = [["does not exist"]]
				fail = 0 # do not create message dialog
		except:
			fail = 2
			data = []
			
		if fail == 1:
			fmessage = "Warning: Critical file/dir\n\n %s%s\n\n not found, it has been created for you." % (config_path, arg)
		elif fail == 2:
			fmessage = "Warning: Critical file/dir\n\n %s%s\n\n not found. An attempt to automatically create this file/dir has been made, but has failed. It is recommended that you create this file/dir yourself." % (config_path, arg)
		if fail > 0:  # make it doable for any valid fail message
			createMessageDialog(None, gtk.DIALOG_DESTROY_WITH_PARENT, gtk.MESSAGE_WARNING, gtk.BUTTONS_OK, "Error reading critical file", fmessage)
		return data

	data = [] #list of list: eg [['python','x86']]
	for i in contents:
		if i.startswith('#'): #don't split if its a comment
			new = [i, None]
		else:
			new = i.split(None,1)
		data.append(new)
	return data #return the master list of lists


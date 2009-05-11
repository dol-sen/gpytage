#!/usr/bin/env python
#
# GPytage helper.py module
#
############################################################################
#    Copyright (C) 2008-2009 by Kenneth Prugh                              #
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
import os
from config import get_config_path, config_files

def folder_scan():
	""" Return files and directories in the portage config path """
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

def folder_walk(dir):
	""" Return list of files in specified directory """
	config_path = get_config_path()
	dir_files = []
	for i in os.listdir(config_path+dir):
		dir_files.append(i)
	return dir_files

def reload():
	""" Revert all saved changes and reinitialize data from the filesystem """
	from datastore import clearData, initData, initTreeModel
	clearData()
	initData()
	initTreeModel()
	
	from window import setTitleEdited
	setTitleEdited(False)

def scan_contents(filepath):
	""" Return data in specified file """
	config_path = get_config_path()

	try:
		f=open(config_path+filepath, 'r')
		contents = f.readlines()
		f.close()
	except IOError: #needed or everything breaks
		print 'HELPER: scan_contents(); Warning: Critical file %s%s not found' % (config_path, arg)

	data = [] #list of list: eg [['python','x86']]
	for i in contents:
		if i.startswith('#'): #don't split if its a comment
			new = [i, None]
		else:
			new = i.split(None,1)
		data.append(new)
	return data #return the master list of lists

#!/usr/bin/env python
#
# GPytage datastore.py module
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

import pygtk; pygtk.require("2.0")
import gtk
from helper import folder_scan, folder_walk, scan_contents

config_files = ['package.keywords', 'package.unmask', 'package.mask', 'package.use']

datastore = gtk.TreeStore(str, str, bool, str) #stores the main files

#19:33 < Zalamander> Ken69267 use a dictionary to map the names to created 
                    #lists. "d = {}; for name in list: d[name] = [1,2,3,4,5]" values will be in the dict.
					
def create_lists():
	parent_folder, simple_files = folder_scan()
	global lists
	lists = {}
	for i in simple_files:
		lists[i] = gtk.ListStore(str, str, bool, str)
		data = scan_contents(i)
		for row in data:
			try:
				col1 = row[0].rstrip() #strips \n
			except:
				col1 = None
			try:
				col2 = row[1].rstrip() # not all files have 2 cols
			except:
				col2 = None
			lists[i].append([col1, col2, True, i])
			
	for i in parent_folder:
		parent = i
		sub_folders = folder_walk(i)
		for i in sub_folders:
			lists[i] = gtk.ListStore(str, str, bool, str)
			sub_file_path = parent + '/' + i
			data = scan_contents(sub_file_path)
			for row in data:
				try:
					col1 = row[0].rstrip() #strips \n
				except:
					col1 = None
				try:
					col2 = row[1].rstrip() # not all files have 2 cols
				except:
					col2 = None
				lists[i].append([col1, col2, True, parent])
	#for i in lists:
		#print lists[i]
	return lists
	
def create_treeiter():#create the parent/main files
		parent_folder, simple_files = folder_scan()
		#parent_files = self.folder_walk(parent_folder)
		for i in simple_files: #needs no sub main rows just data
			siter = datastore.append(None, [i, None, False, i])
		for i in parent_folder: #parent_folders is list of folders such as package.keywords
			#i is a dir such as package.keywords
			pfolder = i
			piter = datastore.append(None, [i, None, False, i])
			complex_files = folder_walk(i) #this needs to return list files in dir
			for i in complex_files: #"simple files"
				name = i #folder name being iterated
				citer = datastore.append(piter, [i, None, False, pfolder])

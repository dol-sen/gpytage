#!/usr/bin/env python
#
# GPytage v0.1_Alpha released under the GPLv2 License
# GPytage is a utility that helps manage portage's package.* files
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

datastore = gtk.TreeStore(str, str, bool)

def create_treeiter():#create the parent/main rows
		parent_folder, simple_files = folder_scan()
		#parent_files = self.folder_walk(parent_folder)
		for i in simple_files: #needs no sub main rows just data
			name = i.partition('.')[2]
			siter = name+"_iter"
			siter = datastore.append(None, [name, None, False])
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
				datastore.append(siter, [col1, col2, True])
		for i in parent_folder: #parent_folders is list of folders such as package.keywords
			#i is a dir such as package.keywords
			pfolder = i
			name = i.partition('.')[2]
			giter = name+"_iter"
			giter = datastore.append(None, [name, None, False])
			complex_files = folder_walk(i) #this needs to return list files in dir
			for i in complex_files: #"simple files"
				name = i #folder name being iterated
				gciter = name+"_iter"
				gciter = datastore.append(giter, [name, None, False])
				dir_file_path = pfolder+'/'+i
				data = scan_contents(dir_file_path)
				for row in data:
					col1 = row[0].rstrip()
					try:
						col2 = row[1].rstrip()
					except:
						col2 = None
					datastore.append(gciter, [col1,col2, True])
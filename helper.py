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

portage_path = '/etc/testportage/'
config_files = ['package.keywords', 'package.unmask', 'package.mask', 'package.use']

def folder_scan():#returns what files are files/dirs wrt portage
	dirs = []
	file = []
	for i in config_files:
		result = os.path.isdir(portage_path+i)
		if(result):
			dirs.append(i)
		else:
			file.append(i)
	return dirs, file

def folder_walk(dir):#returns list of files within dirs
	dir_files = []
	for i in os.listdir(portage_path+dir+'/'):
		dir_files.append(i)
	return dir_files

#FIX ME FOR DUAL PANEL
def reload(window): #reloads all rows in treeview
	import datastore
	datastore.datastore.clear()
	datastore.create_treeiter()
	window.set_title("GPytage")

def scan_contents(arg):#returns data in specified file
	try:
		f=open(portage_path+arg, 'r')
		contents = f.readlines()
		f.close()
	except IOError: #needed or everything breaks
		print 'Warning: Critical file /etc/%s not found, creating...' % arg
		writemessage = '''# This file was created by GPytage as it is required for proper operation.'''
		f=open(portage_path+arg, 'w')
		f.write(writemessage)
		f.close

	data = [] #list of list: eg [['python','x86']]
	for i in contents:
		if i.startswith('#'): #don't split if its a comment
			new = [i, None]
		else:
			new = i.split(None,1)
		data.append(new)
	return data #return the master list of lists
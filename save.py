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

import os.path
import sys
import pdb

def save(arg, datastore): #the important one...
	for row in datastore: #iters through parents
		file = 'package.'+row[0] #eg: package.keywords
		simlist = [] #uh, write this to file i guess
		for child in row.iterchildren(): #child of parents
			if child[2] == False: #if its false it has subfiles
				subdlist = []
				for cell in child.iterchildren(): #child.iter is subfile
					datarow = assemblerow(cell)
					subdlist.append(datarow)
				status = savefile(file, child[0], subdlist)
			else:
				#print child #list
				datarow = assemblerow(child)
				simlist.append(datarow)
		if simlist != []:
			status = savefile(file, None, simlist)
	#window.set_title("GPytage")
	if status:
		return True
#insight: datastore can be thought of a giant list, where row[0] references the first item in a multi list list. eg: foo = [['blah'],['blah1']]

def assemblerow(child):
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

def savefile(package, subfile, rowlist):
	if subfile is None:
		try:
			f=open('/etc/portage/'+package, 'w')
		except IOError:
			print 'Failed to open /etc/portage/' + package + ' for write access'
			return False
		for row in rowlist:
			f.write(row)
		f.close
		return True
	else:
		try:
			f=open('/etc/portage/'+package+'/'+subfile, 'w')
		except IOError:
			print 'failed to open /etc/portage/'+package+'/'+subfile + ' for write access'
			return False
		for row in rowlist:
			f.write(row)
		f.close
		return True

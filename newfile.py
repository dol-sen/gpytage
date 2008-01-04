#!/usr/bin/env python
#
# GPytage newfile.py subfile module
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
import datastore
from window import title

from config import get_config_path, config_files

def new(window):#create a new subfile
	newd = gtk.Dialog('Create new Subfile', window, gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT, None)
	dirs,files = folder_scan()
	#eventually you will be able to create a new subfile from a files
	#selection rather than just dirs
	cb = gtk.combo_box_new_text()
	for i in dirs:
		cb.append_text(i)
	cb.set_active(0)
	sbox = gtk.HBox()
	sbox.pack_start(gtk.Label("Parent directory:"))
	sbox.pack_start(cb)
	newd.vbox.pack_start(sbox)
	ftextbox = gtk.HBox()
	flabel = gtk.Label("New subfile name:")
	ftext = gtk.Entry()
	ftextbox.pack_start(flabel)
	ftextbox.pack_start(ftext)

	newd.vbox.pack_start(ftextbox)
	addb = gtk.Button("Add", gtk.STOCK_ADD)
	closeb = gtk.Button("Close",gtk.STOCK_CLOSE)
	addb.connect("clicked", add_subfile, cb, ftext, newd, window)
	closeb.connect("clicked", close_subfile, newd)
	newd.action_area.pack_start(closeb)
	newd.action_area.pack_start(addb)
	newd.show_all()
	newd.run()

def close_subfile(arg, newd):
	newd.hide()

def add_subfile(arg, cb, ftext, newd, window):
	model = cb.get_model()
	index = cb.get_active()
	#print "NEWFILE: add_subfile(); index = " + str(index)
	if index >= 0: # prevent index errors
		# next line gets an index error when trying to add a subfile to a non existent sets dir. (Or if selection is blank)
		cbselection =  model[index][0] #current text
		ftextselection = ftext.get_text()
		Success = False
		if len(ftextselection):
			#Success = True
			#create_subfile(cbselection, ftextselection)
		#if Success:
			addToMemory(cbselection, ftextselection)
			#arg = "subfile" #no idea...reload needs something passed
			#from helper import reload
			#reload() #no, we want local changes to be kept in memory.
			newd.hide() #hide/destroy the dialog

matched = False

def addToMemory(parent, filename):
	datastore.datastore.foreach(findMatch, [parent, filename])
	msg= '#This file was created by GPytage'
	datastore.lists[filename] = gtk.ListStore(str, str, bool, str)
	datastore.lists[filename].append([msg, None, True, parent]) #rightpanel stuff
	title("* GPytage")

#ugly hack really..but it works
def findMatch(model, path, iter, user_data): #This can't return a value... stupid callback
	print user_data[0], user_data[1]
	print model.get_value(iter, 0).strip('*')
	if model.get_value(iter, 0).strip('*') == user_data[0]:
		edited_file = "*%s" % user_data[1]
		model.append(iter, [edited_file, None, False, user_data[0]])

#def create_subfile(cbselection, ftextselection): #lets make it so save has to handle this
	#config_path = get_config_path()
	#try:
		#path = "%s/%s/%s" %(config_path,cbselection, ftextselection)
		##print path
		#msg= '''# This file was created by GPytage.'''
		#f=open(path, 'w')
		#f.write(msg)
		#f.close
	#except IOError:
		#print 'Failed to create %s%s/%s' %(config_path,cbselection,ftext)

#to be moved to a helper file
def folder_scan():#returns what files are files/dirs wrt portage
	config_path = get_config_path()
	dirs = []
	file = []
	import os.path
	for i in config_files:
		result = os.path.isdir(config_path+i)
		if(result):
			dirs.append(i)
		else:
			file.append(i)
	return dirs, file

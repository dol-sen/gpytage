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

from helper import portage_path

config_files = datastore.config_files

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
	cbselection =  model[index][0] #current text
	ftextselection = ftext.get_text()
	Success = False
	if len(ftextselection):
		Success = True
		create_subfile(cbselection, ftextselection)
	if Success:
		arg = "subfile" #no idea...reload needs something passed
		from helper import reload
		reload(window)
		newd.hide() #destroy better?

def create_subfile(cbselection, ftextselection):
	try:
		path = "%s/%s/%s" %(portage_path,cbselection, ftextselection)
		#print path
		msg= '''# This file was created by GPytage.'''
		f=open(path, 'w')
		f.write(msg)
		f.close
	except IOError:
		print 'Failed to create %s%s/%s' %(portage_path,cbselection,ftext)

#to be moved to a helper file
def folder_scan():#returns what files are files/dirs wrt portage
	dirs = []
	file = []
	import os.path
	for i in config_files:
		result = os.path.isdir(portage_path+i)
		if(result):
			dirs.append(i)
		else:
			file.append(i)
	return dirs, file
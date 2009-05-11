#!/usr/bin/env python
#
# GPytage datastore.py module
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

import FolderObj, PackageFileObj

from helper import folder_scan, folder_walk
from config import config_files

# declare some constants for clarity of code
F_NAME = 0
F_REF = 1

folderModel = gtk.TreeStore(
						    str,        # 0 entry name
						    object,		# 1 entry reference
)						                # Folders

TLFolders = []
TLFiles = []

def initData():
	""" Constructs Folder and PackageFile objects """
	
	Folders, Files = folder_scan() # Top level folders and files in config path
	
	# Handle Folders first
	for folder in Folders:
		fobj = FolderObj.FolderObj(folder, folder)
		TLFolders.append(fobj)
		subFiles = folder_walk(folder)
		
		# These folders contain files
		for subFile in subFiles:
			fileobj = PackageFileObj.PackageFileObj(subFile, folder+"/"+subFile, fobj)
	
	# Handle Top-level Files
	for file in Files:
		fileobj = PackageFileObj.PackageFileObj(file, file, None)
		TLFiles.append(fileobj)
		
def initTreeModel():
	""" Populate the TreeModel with data """
	for folder in TLFolders:
		row = [folder.getName(), folder]
		parentIter = folderModel.append(None, row)
		children = folder.getPackages
		for child in children:
			row = [child.getName(), child]
			folderModel.append(parentIter, row)
	for file in TLFiles:
		row = [file.getName(), file]
		folderModel.append(None, row)
		
def clearData():
	""" Clears the TreeModel and the TLFolder,TLFiles list """
	folderModel.clear()
	del TLFolders[:]
	del TLFiles[:]

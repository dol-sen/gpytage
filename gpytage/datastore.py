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

import os

import FolderObj, PackageFileObj

from config import config_files, get_config_path

# declare some constants for clarity of code
F_NAME = 0
F_REF = 1

folderModel = gtk.TreeStore(
						    str,        # 0 entry name
						    object,		# 1 entry reference
)						                # Folders

TLFolders = [] # Holds *ALL* folders, check for children
TLFiles = []

def initData():
	""" Constructs Folder and PackageFile objects """
	path = get_config_path()
	#print "USING PATH: " + path
	for rootDir, folders, files in os.walk(path, topdown=True):
		# Begin the construction
		if rootDir is get_config_path(): # we are top level, no children
			# Filter unrelated files TOPLEVEL ONLY
			# Folders sanity
			for folder in folders[:]:
				if folder not in config_files:
					folders.remove(folder) #ignore unrelated folders
			# Files sanity
			for file in files[:]:
				if file not in config_files:
					files.remove(file) #ignore unrelated files
			#construct
			for folder in folders:
				foldobj = FolderObj.FolderObj(folder, rootDir + "/" + folder)
				TLFolders.append(foldobj)
			for file in files:
				fileobj = PackageFileObj.PackageFileObj(file, rootDir + "/" + file, None)
				TLFiles.append(fileobj)
		else: # No longer top level, we are inside a folder
			tlname = rootDir.split("/")[-1] # /etc/portage/sets => sets
			#construct
			for folder in folders: # recursive folder
				parent = __getParent(tlname, "folder") # FolderObj
				foldobj = FolderObj.FolderObj(folder, rootDir + "/" + folder)
				foldobj.setHasParent(True)
				foldobj.setParentFolder(parent)
				parent.addFolder(foldobj)
				parent.setChildren(True)
				TLFolders.append(foldobj)
			for file in files:
				parent = __getParent(tlname, "file") #PackageFileObj
				fileobj = PackageFileObj.PackageFileObj(file, rootDir + "/" + file, parent)
				parent.addPackage(fileobj)
				#TLFiles.append(fileobj)
			
def __getParent(tlname, type):
	""" Finds the associated parent named tlname from the specified list type """
	if type is "folder":
		for folder in TLFolders:
			if folder.getName() == tlname:
				return folder
	if type is "file":
		for folder in TLFolders:
			if folder.getName() == tlname:
				return folder
		
def initTreeModel():
	""" Populate the TreeModel with data """
	for folder in TLFolders: #Contains *all* folders
		# Handle Top level Folders with no folder children first
		if (folder.getChildrenState() == False and folder.getParentState() == False):
			row = [folder.getName(), folder]
			parentIter = folderModel.append(None, row)
			path = folderModel.get_path(parentIter)
			treeRowRef = gtk.TreeRowReference(folderModel, path)
			folder.setTreeRowRef(treeRowRef)
			children = folder.getPackages()
			for child in children: #Add children files to treeview
				row = [child.getName(), child]
				childIter = folderModel.append(parentIter, row)
				path = folderModel.get_path(childIter)
				treeRowRef = gtk.TreeRowReference(folderModel, path)
				child.setTreeRowRef(treeRowRef)
		else: # Folders have folder children (an unknown amount unfortunately) (Recursive)
			#Add the parent folder to the treeview
			row = [folder.getName(), folder]
			if folder.getParentState() == False: #Top level
				parentIter = folderModel.append(None, row)
				path = folderModel.get_path(parentIter)
				treeRowRef = gtk.TreeRowReference(folderModel, path)
				folder.setTreeRowRef(treeRowRef) # We will need this later to pack the children
				                                 # in the treeview
			else: #child folder
				# We gotta find the stupid things parent row
				parent = folder.getParentFolder()
				path = parent.getTreeRowRef().get_path()
				grandIter = folderModel.get_iter(path)
				parentIter = folderModel.append(grandIter, row)
				path = folderModel.get_path(parentIter)
				treeRowRef = gtk.TreeRowReference(folderModel, path)
				folder.setTreeRowRef(treeRowRef)
				
	 		for subfile in folder.getPackages():
	 			row = [subfile.getName(), subfile]
	 			FileIter = folderModel.append(parentIter, row)
	 			path = folderModel.get_path(FileIter)
				treeRowRef = gtk.TreeRowReference(folderModel, path)
				subfile.setTreeRowRef(treeRowRef)
	# Top Level Files only
	for file in TLFiles:
		row = [file.getName(), file]
		parentIter = folderModel.append(None, row)
		path = folderModel.get_path(parentIter)
		treeRowRef = gtk.TreeRowReference(folderModel, path)
		file.setTreeRowRef(treeRowRef)
		
def __clearData():
	""" Clears the TreeModel and the TLFolder,TLFiles list """
	folderModel.clear()
	del TLFolders[:]
	del TLFiles[:]
	
def reinitializeDatabase():
	""" Clears the backend and rebuilds the database from disk """
	__clearData()
	initData()
	initTreeModel()

	from rightpanel import setListModel
	setListModel(None)

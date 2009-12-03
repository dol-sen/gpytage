#!/usr/bin/env python

# GPL2 by Kenneth Prugh <ken69267@gmail.com>

from window import setTitleEdited
from PackageFileObj import L_NAME, L_FLAGS, L_REF

# List of files that have been edited and need saving or reverting
modifiedFiles = []

def __appendModifiedFile(file):
	if file not in modifiedFiles:
		modifiedFiles.append(file)

def fileEdited(file):
	""" Set the passed PackageFileObj as edited """
	file.setEditedState(True)
	lpath = file.getTreeRowRef().get_path()
	lmodel = file.getTreeRowRef().get_model()
	treename = lmodel[lpath][L_NAME]
	if treename == file.getName():
		# mark as edited
		lmodel[lpath][L_NAME] = "*" + treename
	# Reflect in title
	setTitleEdited(True)
	# Add to the modifiedFiles
	__appendModifiedFile(file)

def saveModifiedFiles(*args):
	for file in modifiedFiles:
		print file.getName()

#!/usr/bin/env python
#
#   fileOperations.py GPytage module
#
############################################################################
#    Copyright (C) 2009-2010 by Kenneth Prugh                              #
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

from window import setTitleEdited
from PackageFileObj import L_NAME
from sys import stderr

# List of files that have been edited and need saving or reverting
modifiedFiles = []

def __appendModifiedFile(file):
    if file not in modifiedFiles:
        modifiedFiles.append(file)

def __removeModifiedFile(file):
    if file in modifiedFiles:
        modifiedFiles.remove(file)

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

#TODO: Test if files are writable os.access before proceeding further in the
#       save routine?
def saveModifiedFiles(*args):
    """ Saves all modified files """
    for file in modifiedFiles[:]:
        __saveFile(file)

def saveModifiedFile(*args):
    """ Saves the file currently selected """
    # Discover file currently selected
    from helper import getCurrentFile
    file, model = getCurrentFile()
    # save it
    if file in modifiedFiles:
        __saveFile(file)

def __saveFile(file):
    """ Private method to write file to desk """
    # Save the file
    print "Attempting to save " + file.getPath()
    try:
        f=open(file.getPath(), 'w')
        datalist = file.getData()
        for row in datalist:
            if row[0] is not None:
                c1 = row[0]
            else:
                c1 = ""
            if row[1] is not None:
                c2 = row[1]
            else:
                c2 = ""
            if row[0].strip().startswith("#"):
                f.write(c1 + c2 + "\n")
            else:
                f.write(c1 + " " + c2 + "\n")
        f.close()
        __fileSaved(file)
    except IOError, e:
        print >>stderr, "Error saving: ", e

def __fileSaved(file):
    """ Set the passed PackageFileObj as un-edited """
    file.setEditedState(False)
    lpath = file.getTreeRowRef().get_path()
    lmodel = file.getTreeRowRef().get_model()
    # mark as unedited
    lmodel[lpath][L_NAME] = file.getName()
    # remove from the modifiedFiles
    __removeModifiedFile(file)
    # Reflect in title
    if hasModified() is False:
        setTitleEdited(False)

def hasModified():
    """ Return whether the modifiedFiles list is empty """
    if len(modifiedFiles) == 0:
        return False
    else:
        return True

def revertSelected(*args):
    """ Reverts the currently selected file """
    # Discover file currently selected
    from helper import getCurrentFile
    file, model = getCurrentFile()
    if file in modifiedFiles:
        file.initData()
        __fileSaved(file) # Well, it is unedited...
        from rightpanel import setListModel
        setListModel(file.getData())

def revertAllModified(*args):
    """ Reverts all files that have been modified """
    from helper import getCurrentFile
    cfile, model = getCurrentFile()
    for file in modifiedFiles[:]:
        file.initData()
        __fileSaved(file)
        if file == cfile:
            from rightpanel import setListModel
            setListModel(file.getData())

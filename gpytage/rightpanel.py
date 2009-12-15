#!/usr/bin/env python
#
# GPytage rightpanel.py module
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

from helper import getMultiSelection, getCurrentFile
from PackageFileObj import L_NAME, L_FLAGS, L_REF
from fileOperations import fileEdited

rightview = gtk.TreeView()
rightselection = rightview.get_selection()

#set MULTIPLE selection mode
rightselection.set_mode(gtk.SELECTION_MULTIPLE)

def setListModel(ListStore): #we need to switch the model on click
    try:
        rightview.set_model() # Clear from view first
        rightview.set_model(ListStore) #example
        namecol.queue_resize()
    except:
        print 'RIGHTPANEL: setListModel(); failed'

rightview.set_search_column(L_NAME)

# TreeViewColumns
namecol = gtk.TreeViewColumn('Package')
useFlagCol = gtk.TreeViewColumn('Flags')

# Add TreeViewColumns to TreeView
rightview.append_column(namecol)
rightview.append_column(useFlagCol)

# CellRenderer construction
nameCell = gtk.CellRendererText()
nameCell.set_property('editable', True)
flagCell = gtk.CellRendererText()
flagCell.set_property('editable', True)

# Add CellRenderer to TreeViewColumns
namecol.pack_start(nameCell, True)
namecol.add_attribute(nameCell, 'text', L_NAME)
namecol.set_sizing(gtk.TREE_VIEW_COLUMN_AUTOSIZE)

useFlagCol.pack_start(flagCell, True)
useFlagCol.add_attribute(flagCell, 'text', L_FLAGS)
useFlagCol.set_expand(True)
useFlagCol.set_sizing(gtk.TREE_VIEW_COLUMN_AUTOSIZE)

# ScrolledWindow
scroll = gtk.ScrolledWindow()
scroll.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
scroll.add_with_viewport(rightview)

###########Drag and Drop####################
#===============================================================================
# rightview.set_reorderable(True) # allow inline drag and drop
# rightview.enable_model_drag_source(gtk.gdk.BUTTON1_MASK, [('text/plain', 0, 0)], gtk.gdk.ACTION_DEFAULT | gtk.gdk.ACTION_MOVE)
# rightview.enable_model_drag_dest([('text/plain', 0, 0)], gtk.gdk.ACTION_DEFAULT)
# import panelfunctions
# rightview.connect("drag_begin", panelfunctions.drag_begin_signal)
# rightview.connect("drag_data_delete", panelfunctions.drag_data_delete_signal)
# rightview.connect("drag_data_received", panelfunctions.get_dragdestdata)
#===============================================================================

# Callbacks
def edited_cb(cell, path, new_text, col):
    """ Indicate file has been edited """
    model = rightview.get_model()
    model[path][col] = new_text
    file = model[path][L_REF]
    # Indicate file status in TreeView
    fileEdited(file)

def insertRow(arg):
    """ Insert row below selected row(s) """
    rowReferences = getMultiSelection(rightview)
    try:
        lastRowSelectedPath = rowReferences[-1].get_path()
        model = rowReferences[-1].get_model()
    except:
        # Well, we got a blank file
        PackageFile, lModel = getCurrentFile()
        if PackageFile == None: # No file is actually selected
            return
        model = rightview.get_model()
        if model == None: # A folder is selected
            return
        newRow = model.append([None, None, PackageFile])
        # Set the cursor on the new row and start editing the name column
        path = model.get_path(newRow)
        rightview.set_cursor(path, namecol, True)
        # Fire off the edited methods
        fileEdited(PackageFile)
        return
    
    lastRowIter = model.get_iter(lastRowSelectedPath)
    # We need to link this new row with its PackageFile Object
    PackageFile = model.get_value(lastRowIter, L_REF)
    # Insert into the model
    newRow = model.insert_after(lastRowIter, [None, None, PackageFile])
    # Set the cursor on the new row and start editing the name column
    path = model.get_path(newRow)
    rightview.set_cursor(path, namecol, True)
    # Fire off the edited methods
    fileEdited(PackageFile)

def deleteRow(arg):
    """ Delete selected row(s) """
    rowReferences = getMultiSelection(rightview)
    model = rightview.get_model()
    PackageFile, lModel = getCurrentFile()
    for ref in rowReferences:
        iter = model.get_iter(ref.get_path())
        model.remove(iter)
    # If nothing is deleted we shouldn't show 
    if len(rowReferences) > 0:
        fileEdited(PackageFile)

def commentRow(window):
    """ Comment selected row(s) """
    rowReferences = getMultiSelection(rightview)
    model = rightview.get_model()
    PackageFile, lModel = getCurrentFile()
    # Is anything even selected?
    if len(rowReferences) == 0:
        return
    for ref in rowReferences:
        iter = model.get_iter(ref.get_path())
        cText = model.get_value(iter, L_NAME)
        if not cText.startswith("#"):
            model.set_value(iter, L_NAME, "#"+cText)
    fileEdited(PackageFile)

def uncommentRow(window):
    """ Uncomment selected row(s) """
    rowReferences = getMultiSelection(rightview)
    model = rightview.get_model()
    PackageFile, lModel = getCurrentFile()
    # Is anything even selected?
    if len(rowReferences) == 0:
        return
    for ref in rowReferences:
        iter = model.get_iter(ref.get_path())
        cText = model.get_value(iter, L_NAME)
        if cText.startswith("#"):
            model.set_value(iter, L_NAME, cText[1:])
    fileEdited(PackageFile)

def toggleComment(*args):
    """ Toggle comments on selected rows based on the first row """
    rowReferences = getMultiSelection(rightview)
    model = rightview.get_model()
    file, lModel = getCurrentFile()
    comment = True
    # Is anything even selected?
    if len(rowReferences) == 0:
        return
    # Lets see what the first comment is
    ref = rowReferences[0]
    iter = model.get_iter(ref.get_path())
    cText = model.get_value(iter, L_NAME)
    if cText.startswith("#"):
        comment = False
    # Lets proceed now
    if comment: # Comment all lines
        for ref in rowReferences:
            iter = model.get_iter(ref.get_path())
            cText = model.get_value(iter, L_NAME)
            if not cText.startswith("#"):
                model.set_value(iter, L_NAME, "#"+cText)
    else: # Uncomment all lines
        for ref in rowReferences:
            iter = model.get_iter(ref.get_path())
            cText = model.get_value(iter, L_NAME)
            if cText.startswith("#"):
                model.set_value(iter, L_NAME, cText[1:])
    fileEdited(file)

def __rightClicked(view, event):
    """ Right click menu for package options """
    if event.button == 3:
        menu = gtk.Menu()
        irow = gtk.MenuItem("Insert Package")
        irow.connect("activate", insertRow)
        drow = gtk.MenuItem("Delete Package")
        drow.connect("activate", deleteRow)
        menu.append(irow)
        menu.append(drow)
        separator = gtk.MenuItem()
        crow = gtk.MenuItem("Comment Package")
        urow = gtk.MenuItem("Uncomment Package")
        crow.connect("activate", commentRow)
        urow.connect("activate", uncommentRow)
        menu.append(separator)
        menu.append(crow)
        menu.append(urow)
        menu.show_all()
        menu.popup(None, None, None, event.button, event.time)

def __handleKeyPress(widget, event):
    modifiers = gtk.accelerator_get_default_mod_mask()  
    # copy
    if event.keyval == gtk.gdk.keyval_from_name("c"):
        if (modifiers & event.state) == gtk.gdk.CONTROL_MASK:
            from window import clipboard
            clipboard.copyToClipboard(rightview)
    # paste
    if event.keyval == gtk.gdk.keyval_from_name("p"):
        if (modifiers & event.state) == gtk.gdk.CONTROL_MASK:
            pass
    # cut
    if event.keyval == gtk.gdk.keyval_from_name("x"):
        if (modifiers & event.state) == gtk.gdk.CONTROL_MASK:
            from window import clipboard
            clipboard.cutToClipboard(rightview)


#Signals
nameCell.connect("edited", edited_cb, L_NAME)
flagCell.connect("edited", edited_cb, L_FLAGS)
rightview.connect("button_press_event", __rightClicked)
rightview.connect("key_press_event", __handleKeyPress)

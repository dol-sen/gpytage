#!/usr/bin/env python
#
############################################################################
#    Copyright (C) 2012 by Kenneth Prugh                                   #
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

import gi
from gi.repository import Gtk

class KColEditor(object):
    C_NAME = 0
    C_FLAGS = 1
    C_REF = 2 #the kfile reference

    def __init__(self, gp):
        self.gp = gp

        self.view = Gtk.TreeView()
        self.nameCol = Gtk.TreeViewColumn('Package')
        self.flagCol = Gtk.TreeViewColumn('Flags')

        self.view.append_column(self.nameCol)
        self.view.append_column(self.flagCol)

        self.nameCell = Gtk.CellRendererText()
        self.nameCell.set_property('editable', True)
        self.flagCell = Gtk.CellRendererText()
        self.flagCell.set_property('editable', True)

        self.nameCell.connect("edited", self.__edited_cb, self.C_NAME)
        self.flagCell.connect("edited", self.__edited_cb, self.C_FLAGS)

        self.nameCol.pack_start(self.nameCell, True)
        self.nameCol.add_attribute(self.nameCell, 'text', self.C_NAME)
        self.nameCol.set_sizing(Gtk.TreeViewColumnSizing.AUTOSIZE)

        self.flagCol.pack_start(self.flagCell, True)
        self.flagCol.add_attribute(self.flagCell, 'text', self.C_FLAGS)
        self.flagCol.set_expand(True)
        self.flagCol.set_sizing(Gtk.TreeViewColumnSizing.AUTOSIZE)

        self.container = Gtk.ScrolledWindow()
        self.container.add_with_viewport(self.view)

    def setBuffer(self, kstore):
        self.view.set_model()
        self.view.set_model(kstore)
        self.nameCol.queue_resize()

    def __edited_cb(self, cell, path, new_text, col):
        """ Indicate file has been edited """
        model = self.view.get_model()
        model[path][col] = new_text
        kfile = model[path][self.C_REF]
        # Indicate file status in TreeView
        self.gp.ftree.setEdited(kfile)

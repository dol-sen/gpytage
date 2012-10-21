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

import gtk

class KColEditor(object):
    C_NAME = 0
    C_FLAGS = 1

    def __init__(self, gp):
        self.gp = gp

        self.view = gtk.TreeView()
        self.nameCol = gtk.TreeViewColumn('Package')
        self.flagCol = gtk.TreeViewColumn('Flags')

        self.view.append_column(self.nameCol)
        self.view.append_column(self.flagCol)

        self.nameCell = gtk.CellRendererText()
        self.nameCell.set_property('editable', True)
        self.flagCell = gtk.CellRendererText()
        self.flagCell.set_property('editable', True)

        self.nameCol.pack_start(self.nameCell, True)
        self.nameCol.add_attribute(self.nameCell, 'text', self.C_NAME)
        self.nameCol.set_sizing(gtk.TREE_VIEW_COLUMN_AUTOSIZE)

        self.flagCol.pack_start(self.flagCell, True)
        self.flagCol.add_attribute(self.flagCell, 'text', self.C_FLAGS)
        self.flagCol.set_expand(True)
        self.flagCol.set_sizing(gtk.TREE_VIEW_COLUMN_AUTOSIZE)

        self.container = gtk.ScrolledWindow()
        self.container.add_with_viewport(self.view)

    def setBuffer(self, kstore):
        self.view.set_model()
        self.view.set_model(kstore)
        self.nameCol.queue_resize()

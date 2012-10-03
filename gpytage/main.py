#!/usr/bin/env python
#
############################################################################
#    Copyright (C) 2008-2012 by Kenneth Prugh                              #
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

from backend import Backend
from UIbar import UIbar
from filetree import FileTree
from editor import KEditor
import gtk

class GPytage(object):
    def __init__(self, config):
        self.backend = Backend(config)

        self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.window.set_title("GPytage")
        # The *[] syntax is required for this function. It wants a Glist.
        gtk.window_set_default_icon_list(
                *[gtk.gdk.pixbuf_new_from_file(f) for f in
                    self.backend.config.iconlist]
                )
        self.window.set_default_size(800, 500)
        self.window.connect("destroy", self.quit)
        self.window.connect("delete_event", self.quit)

        self.UI = UIbar()

        self.ftree = FileTree(self)

        self.keditor = KEditor(self)

        hbox = gtk.HBox()

        hbox.pack_start(self.ftree.treeContainer, True, True)
        hbox.pack_start(self.keditor.Container, True, True)

        self.window.add(hbox)
        self.window.show_all()
        gtk.main()

    #This will need to probably swap the entire window type and set the
    #appropriate buffer
    def loadBuffer(self, kfile):
        self.keditor.setBuffer(kfile.getData())

    def quit(self, *args):
        #todo: check for unsaved changes etc.
        gtk.main_quit()

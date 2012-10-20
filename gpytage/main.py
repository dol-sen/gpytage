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

import backend
import filetree
import editor
import UIbar
import gtk

class GPytage(object):
    T_EDIT = 0
    T_COL = 1

    def __init__(self, config):
        self.backend = backend.Backend(config)

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

        self.UI = UIbar.UIBar()

        self.ftree = filetree.FileTree(self)

        self.keditor = editor.KEditor(self)

        # Keep track of the active window type for the right side, either the
        # flat editor or the 2col editor
        self.activeType = GPytage.T_EDIT
        self.hbox = gtk.HBox()

        self.hbox.pack_start(self.ftree.treeContainer, True, True)
        self.hbox.pack_start(self.keditor.Container, True, True)

        self.window.add(self.hbox)
        self.window.show_all()
        gtk.main()

    #This will need to probably swap the entire window type and set the
    #appropriate buffer
    def loadBuffer(self, kfile):
        # EDIT file type
        if (kfile.ftype == kfile.T_EDIT):
            if (self.activeType != GPytage.T_EDIT):
                #self.hbox.remove(kcoleditor)
                self.hbox.pack_start(self.keditor.container, True, True)
            self.keditor.setBuffer(kfile.getData())
        else:
            # COL file type
            pass

    def quit(self, *args):
        #todo: check for unsaved changes etc.
        gtk.main_quit()

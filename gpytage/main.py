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

from . import backend
from . import filetree
from . import editor
from . import kcoleditor
from . import UIbar
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

        self.UI = UIbar.UIBar(self)
        self.window.add_accel_group(self.UI.accelgroup)

        self.ftree = filetree.FileTree(self)

        self.keditor = editor.KEditor(self)
        self.kcoleditor = kcoleditor.KColEditor(self)

        # Keep track of the active window type for the right side, either the
        # flat editor or the 2col editor
        self.activeType = GPytage.T_EDIT

        self.vbox = gtk.VBox()

        self.hbox = gtk.HBox()
        self.hbox.set_homogenous = False

        self.hbox.pack_start(self.ftree.treeContainer, False, True)
        # Size hack for now, perhaps calculate longest file name or similar?
        # Without this its too small if the above expand is set to False. If its
        # set to true they are the same width which is silly
        self.ftree.treeContainer.set_size_request(250, -1)
        self.hbox.pack_start(self.keditor.container, True, True)

        
        self.vbox.pack_start(self.UI.getMenuBar(), False, True)
        self.vbox.add(self.hbox)
        self.window.add(self.vbox)
        self.window.show_all()
        gtk.main()

    #This will need to probably swap the entire window type and set the
    #appropriate buffer
    def loadBuffer(self, kfile):
        # EDIT file type
        if (kfile.ftype == kfile.T_EDIT):
            if (self.activeType != GPytage.T_EDIT):
                self.hbox.remove(self.kcoleditor.container)
                self.hbox.pack_start(self.keditor.container, True, True)
                self.window.show_all()
            self.keditor.setBuffer(kfile.getData())
            self.activeType = GPytage.T_EDIT
        else:
            # COL file type
            if (self.activeType != GPytage.T_COL):
                self.hbox.remove(self.keditor.container)
                self.hbox.pack_start(self.kcoleditor.container, True, True)
                self.window.show_all()
            self.kcoleditor.setBuffer(kfile.getData())
            self.activeType = GPytage.T_COL


    def quit(self, *args):
        #todo: check for unsaved changes etc.
        gtk.main_quit()

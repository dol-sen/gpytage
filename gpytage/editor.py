#!/usr/bin/env python
#
############################################################################
#    Copyright (C) 2011 by Kenneth Prugh                                   #
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

class KEditor(object):
    def __init__(self, gp):
        self.gp = gp

        self.defaultbuf = gtk.TextBuffer()
        self.defaultbuf.set_text("<i>Welcome to GPytage</i>");

        self.editor = gtk.TextView()
        self.editor.set_editable(True)
        self.editor.set_buffer(self.defaultbuf)

        self.markupTable = gtk.TextTagTable()

        self.__initMarkupTable()

        self.container = gtk.ScrolledWindow()
        self.container.add_with_viewport(self.editor)

    def __initMarkupTable(self):
        pass

    def setBuffer(self, buffer):
        self.editor.set_buffer(buffer)
        self.editor.set_editable(True)

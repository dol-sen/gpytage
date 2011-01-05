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
from kfile import kfile
import os
from sys import stderr

class backend(object):
    def __init__(self, config):
        self.config = config
        self.dataModel = gtk.TreeStore(
                str,            # 0 entry name
                gtk.gdk.Pixbuf, # 1 icon via name type [d/f]
                object,         # 2 kfile reference
                )

        self.initBackend()

    def initBackend(self):
        folderRefMap = {}
        for rootDir, folders, files in os.walk(self.config.portconf, topdown=True):
            root = False
            #rootDir is the current level 
            if (rootDir == self.config.portconf):
                #sanitize top level descent
                root = True

                for f in folders[:]:
                    if f not in self.config.portconfFiles:
                        folders.remove(f) #ignore unrelated folders
                for f in files[:]:
                    if f not in self.config.portconfFiles:
                        files.remove(f) #ignore unrelated files
            
            for f in folders:
                data = self.__getDataForModel(f, rootDir, True)
                path = os.path.join(rootDir, f)
                if (root):
                    fiter = self.dataModel.append(None, data)
                else:
                    parent = self.getIterbyRef(folderRefMap[rootDir])
                    fiter = self.dataModel.append(parent, data)
                folderRefMap[path] = self.getTreeRef(fiter)

            for f in files:
                try:
                    data = self.__getDataForModel(f, rootDir, False)
                except IOError, e:
                    print >> stderr, e
                    continue
                parent = self.getIterbyRef(folderRefMap[rootDir])
                self.dataModel.append(parent, data)

    def getTreeRef(self, giter):
        path = self.dataModel.get_path(giter)
        return gtk.TreeRowReference(self.dataModel, path)

    def getIterbyRef(self, ref):
        path = ref.get_path()
        return self.dataModel.get_iter(path)

    def __getDataForModel(self, f, rpath, bFolder):
        name = f
        path = os.path.join(rpath, f)

        theme = gtk.icon_theme_get_default()
        if bFolder:
            icon = theme.load_icon(gtk.STOCK_DIRECTORY, gtk.ICON_SIZE_MENU, 0)
            kobj = None
        else:
            icon = theme.load_icon(gtk.STOCK_FILE, gtk.ICON_SIZE_MENU, 0)
            kobj = kfile(name, path)

        return [name, icon, kobj]


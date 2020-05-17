#!/usr/bin/env python
#
# GPytage config.py module
#
############################################################################
#    Copyright (C) 2008-2011 by Kenneth Prugh, Brian Dolbec                #
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

import portage

VERSION = "3.1-dev"

class Config(object):
    def __init__(self):
        # eg: /usr/portage/
        self.portdir = portage.config(clone=portage.settings).environ()['PORTDIR'] + "/"
        # eg: /etc/portage/
        self.portconf = "/" + portage.const.USER_CONFIG_PATH + "/"

        self.pixpath = "/usr/share/pixmaps/gpytage/"

        self.__icons = ["gpytage-16x16.png", "gpytage-24x24.png",
                "gpytage-32x32.png", "gpytage-48x48.png", "gpytage-64x64.png",
                "gpytage-128x128.png"]

        self.iconlist = [self.pixpath+icon for icon in self.__icons]

        self.portconfFiles = ['bashrc', 'categories', 'color.map', 'mirrors', \
                'modules', 'package.keywords', 'package.license', 'package.mask', \
                'package.properties', 'package.unmask', 'package.use', 'repos.conf', \
                'profile', 'sets']

        print(("Config: portage version = " + portage.VERSION))

    def setPixPath(self, path):
        self.pixpath = path
        self.iconlist = [self.pixpath+icon for icon in self.__icons]


#!/usr/bin/env python
#
# GPytage config.py module
#
############################################################################
#    Copyright (C) 2008-2010 by Kenneth Prugh, Brian Dolbec                #
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

from sys import exit, stderr

config_files = ['bashrc', 'categories', 'color.map', 'mirrors', 'modules', \
        'package.keywords', 'package.license', 'package.mask',\
        'package.properties', 'package.unmask', 'package.use', 'repos.conf',\
        'profile', 'sets']

test_path = '/etc/testportage/'

try: # >=portage 2.1 modules
    import portage
    import portage.const
except ImportError as e:
    print("Portage Import Error: ", e, file=stderr)
    exit('Could not find portage module.\n'
         'Are you sure this is a Gentoo system?')

print(("Config: portage version = " + portage.VERSION), file=stderr)

config_path = "/" + portage.const.USER_CONFIG_PATH + "/"
PORTDIR=portage.config(clone=portage.settings).environ()['PORTDIR']

# house cleaning no longer needed imports
del portage

def set_test_path():
    global config_path, test_path
    config_path = test_path
    print("CONFIG: new config_path = " + config_path)

def get_config_path():
    return config_path

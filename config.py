#!/usr/bin/env python
#
# GPytage config.py module
#
############################################################################
#    Copyright (C) 2007 by Kenneth Prugh, Brian Dolbec                     #
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

config_files = ['package.keywords', 'package.unmask', 'package.mask', 'package.use', 'sets', 'bashrc', \
		'color.map', 'modules', 'mirrors', 'categories']
test_path = '/etc/testportage/'

try:
	import portage
	import portage_const
	print >>stderr, ("Config: portage version = " + portage.VERSION)
except ImportError:
	exit(_('Could not find portage module.\n'
		'Are you sure this is a Gentoo system?'))

portage_path = portage_const.USER_CONFIG_PATH
#portage_path = '/etc/portage/'

config_path = portage_path + '/'
PORTDIR=portage.config(clone=portage.settings).environ()['PORTDIR']

# house cleaning no longer needed imports
del portage, portage_const

def set_test_path():
	global config_path, test_path
	config_path = test_path
	print "CONFIG: new config_path = " + config_path

def get_config_path():
	return config_path

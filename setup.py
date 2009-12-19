#!/usr/bin/env python
#
#   GPytage setup script
#
############################################################################
#    Copyright (C) 2008-2009 by Kenneth Prugh                              #
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

from distutils.core import setup
from gpytage.version import version as p_version

setup(name="gpytage",
	version=p_version,
	description="GTK Utility to help manage Portage's user config files",
	license="GPL-2",
	author="Kenneth Prugh",
	author_email="ken69267@gmail.com",
	url="https://gna.org/projects/gpytage/",
	download_url="http://download.gna.org/gpytage/gpytage-" + p_version + ".tar.gz",
	packages=['gpytage'],
	package_dir={'gpytage':'gpytage'},
	scripts=["scripts/gpytage"],
	data_files=[("/usr/share/pixmaps", ["gpytage/pixmaps/gpytage-64x64.png"]),
			    ("/usr/share/applications", ["gpytage.desktop"]),
			    ("/usr/share/gpytage/pixmaps", ["gpytage/pixmaps/gpytage-16x16.png","gpytage/pixmaps/gpytage-24x24.png","gpytage/pixmaps/gpytage-32x32.png","gpytage/pixmaps/gpytage-48x48.png","gpytage/pixmaps/gpytage-64x64.png","gpytage/pixmaps/gpytage-128x128.png"])
			    ,],
)

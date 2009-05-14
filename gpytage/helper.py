#!/usr/bin/env python
#
# GPytage helper.py module
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

from window import setTitleEdited
from PackageFileObj import L_NAME, L_FLAGS, L_REF

def fileEdited(file):
	lpath = file.getTreeRowRef().get_path()
	lmodel = file.getTreeRowRef().get_model()
	treename = lmodel[lpath][L_NAME]
	if treename == file.getName():
		# mark as edited
		lmodel[lpath][L_NAME] = "*" + treename
	# Reflect in title
	setTitleEdited(True)

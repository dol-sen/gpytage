#!/usr/bin/env python

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
			    ("/usr/share/gpytage/glade", ["gpytage/glade/convertfile.glade","gpytage/glade/deletefile.glade","gpytage/glade/newsubfile.glade","gpytage/glade/renamefile.glade"]),
			    ("/usr/share/gpytage/pixmaps", ["gpytage/pixmaps/gpytage-16x16.png","gpytage/pixmaps/gpytage-24x24.png","gpytage/pixmaps/gpytage-32x32.png","gpytage/pixmaps/gpytage-48x48.png","gpytage/pixmaps/gpytage-64x64.png","gpytage/pixmaps/gpytage-128x128.png"])
			    ,],
)

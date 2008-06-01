#!/usr/bin/env python

from distutils.core import setup
from version import version as p_version

setup(name="gpytage",
	version=p_version,
	description="GTK Utility to help manage Portage's user config files",
	license="GPL-2",
	author="Kenneth Prugh",
	author_email="ken69267@gmail.com",
	url="https://gna.org/projects/gpytage/",
	download_url="http://download.gna.org/gpytage/gpytage-" + p_version + ".tar.gz",
	packages=['gpytage'],
	package_dir={'gpytage':''},
	package_data={'gpytage': ['glade/*.glade']},
	scripts=["gpytage"],
	data_files=[("/usr/share/applications", ["gpytage.desktop"])],
)

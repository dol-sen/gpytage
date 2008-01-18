#!/usr/bin/env python

from distutils.core import setup

setup(name="gpytage",
	version="0.2.0_beta",
	description="GTK Utility to help manage Portage's package files",
	license="GPL-2",
	author="Kenneth Prugh",
	author_email="ken69267@gmail.com",
	url="https://gna.org/projects/gpytage/",
	download_url="http://download.gna.org/gpytage/gpytage-0.2.0_beta.tar.gz",
	package_dir={'gpytage':''},
	packages=['gpytage'],
	scripts=["gpytage"],
)

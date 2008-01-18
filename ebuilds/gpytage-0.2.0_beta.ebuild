# Copyright 1999-2008 Gentoo Foundation
# Distributed under the terms of the GNU General Public License v2
# $Header: $

inherit distutils

DESCRIPTION="GTK Utility to help manage Portage's package files"
HOMEPAGE="https://gna.org/projects/gpytage/"
SRC_URI="http://download.gna.org/${PN}/${P}.tar.gz"

LICENSE="GPL-2"
SLOT="0"
KEYWORDS="~amd64"
IUSE=""

RDEPEND=">=dev-lang/python-2.4"
DEPEND=""

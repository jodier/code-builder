#############################################################################
# Author  : Jerome ODIER, Christophe SMEKENS
# Email   : odier@hypnos3d.com, smekens@hypnos3d.com
#
# Version : 1.0 beta (2012)
#
#
# This file is part of CODE-BUILDER.
#
#  u-autotool is free software; you can redistribute it and/or modify
#  it under the terms of the GNU Lesser General Public License as published
#  by the Free Software Foundation; either version 3 of the License, or
#  (at your option) any later version.
#
#  u-autotool is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU Lesser General Public License for more details.
#
#  You should have received a copy of the GNU Lesser General Public License
#  along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
#############################################################################

import re, cb.utils

#############################################################################

HAS_HEADERS = False

#############################################################################

HEADER_EXT = 'cs'
SOURCE_EXT = 'cs'

#############################################################################

PRIMITIVES = set([
	'void',
	'char',
	'sbyte',
	'byte',
	'short',
	'ushort',
	'int',
	'uint',
	'long',
	'ulong',
	'float',
	'double',
	'bool',
	'string',
	'Char',
	'SByte',
	'Byte',
	'Int16',
	'UInt16',
	'Int32',
	'UInt32',
	'Int64',
	'UInt64',
	'Single',
	'Double',
	'Bool',
	'String',
	'System.Char',
	'System.SByte',
	'System.Byte',
	'System.Int16',
	'System.UInt16',
	'System.Int32',
	'System.UInt32',
	'System.Int64',
	'System.UInt64',
	'System.Single',
	'System.Double',
	'System.Bool',
	'System.String',
])

#############################################################################

QUALIFIERS = set([
	'const',
])

#############################################################################


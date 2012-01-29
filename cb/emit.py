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

import cb.utils

#############################################################################
# INTERFACE								    #
#############################################################################

def interface(ctx):
	LANG = ctx['lang']

	INT_TYPES_TYPES   = ctx['int_types']['types'  ]
	INT_TYPES_ENUMS   = ctx['int_types']['enums'  ]
	INT_TYPES_STRUCTS = ctx['int_types']['structs']

	#####################################################################
	# PROLOG							    #
	#####################################################################

	LANG.generate_prolog(ctx)

	#####################################################################
	# TYPES								    #
	#####################################################################

	LANG.generate_COMMENT(ctx, 'TYPES')

	for t in INT_TYPES_TYPES.iteritems():
		LANG.generate_type(ctx, t)

	print('')

	LANG.generate_separator(ctx)

	for t in INT_TYPES_ENUMS.iteritems():
		LANG.generate_enum(ctx, t)
		print('')

	LANG.generate_separator(ctx)

	for t in INT_TYPES_STRUCTS.iteritems():
		LANG.generate_struct(ctx, t)
		print('')

	#####################################################################
	# DEFINITIONS							    #
	#####################################################################

	LANG.generate_COMMENT(ctx, 'IMPLEMENTATION')

	LANG.generate_definitions(ctx)

	#####################################################################
	# EXTENSION STRUCTS						    #
	#####################################################################

	LANG.generate_separator(ctx)

	LANG.generate_extension_structs(ctx)

	#####################################################################
	# EXTENSION PROFILES						    #
	#####################################################################

	LANG.generate_separator(ctx)

	LANG.generate_extension_profiles(ctx)

	#####################################################################
	# PROFILES							    #
	#####################################################################

	LANG.generate_separator(ctx)

	LANG.generate_global_methods(ctx)

	#####################################################################
	# EPILOG							    #
	#####################################################################

	LANG.generate_separator(ctx)

	LANG.generate_epilog(ctx)

#############################################################################
# IMPLEMENTATION							    #
#############################################################################

def implementation(ctx):
	pass

#############################################################################


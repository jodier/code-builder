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

def interface(ctx):
	LANG = ctx['lang']

	try:
		fp = open('%s.h' % ctx['name'], 'wt')

		#############################################################
		# PROLOG						    #
		#############################################################

		LANG.generate_prolog(ctx, fp)

		#############################################################
		# TYPES							    #
		#############################################################

		LANG.generate_COMMENT(ctx, fp, 'TYPES')

		for t in ctx['int_types']['types'].iteritems():
			LANG.generate_type(ctx, fp, t)

		cb.utils.writeline(fp, '')

		LANG.generate_separator(ctx, fp)

		for t in ctx['int_types']['enums'].iteritems():
			LANG.generate_enum(ctx, fp, t)
			cb.utils.writeline(fp, '')

		LANG.generate_separator(ctx, fp)

		for t in ctx['int_types']['structs'].iteritems():
			LANG.generate_struct(ctx, fp, t)
			cb.utils.writeline(fp, '')

		#############################################################
		# DEFINITIONS						    #
		#############################################################

		LANG.generate_COMMENT(ctx, fp, 'IMPLEMENTATION')

		LANG.generate_definitions(ctx, fp)

		#############################################################
		# EXTENSION STRUCTS					    #
		#############################################################

		LANG.generate_separator(ctx, fp)

		LANG.generate_extension_structs(ctx, fp)

		#############################################################
		# EXTENSION PROFILES					    #
		#############################################################

		LANG.generate_separator(ctx, fp)

		LANG.generate_extension_profiles(ctx, fp)

		#############################################################
		# PROFILES						    #
		#############################################################

		LANG.generate_separator(ctx, fp)

		LANG.generate_global_methods(ctx, fp)

		#############################################################
		# EPILOG						    #
		#############################################################

		LANG.generate_separator(ctx, fp)

		LANG.generate_epilog(ctx, fp)

		#############################################################

		fp.close()

	except IOError:
		cb.utils.error('Could not open \'%s.h\' !' % ctx['name'])

#############################################################################

def implementation(ctx):
	pass

#############################################################################


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

		LANG.emit_prologPubInt(ctx, fp)

		#############################################################
		# TYPES							    #
		#############################################################

		LANG.emit_COMMENT(ctx, fp, 'TYPES')

		for t in ctx['int_types']['types'].iteritems():
			LANG.emit_type(ctx, fp, t)

		LANG.emit_separator(ctx, fp)

		for t in ctx['int_types']['enums'].iteritems():
			LANG.emit_enum(ctx, fp, t)

		LANG.emit_separator(ctx, fp)

		for t in ctx['int_types']['structs'].iteritems():
			LANG.emit_struct(ctx, fp, t)

		#############################################################
		# DEFINITIONS						    #
		#############################################################

		LANG.emit_COMMENT(ctx, fp, 'IMPLEMENTATION')
		LANG.emit_definitions(ctx, fp)

		#############################################################
		# EXTENSION STRUCTS					    #
		#############################################################

		LANG.emit_separator(ctx, fp)
		LANG.emit_extension_structs(ctx, fp)

		#############################################################
		# EXTENSION PROFILES					    #
		#############################################################

		LANG.emit_separator(ctx, fp)
		LANG.emit_extension_profiles(ctx, fp)

		#############################################################
		# METHODS						    #
		#############################################################

		LANG.emit_separator(ctx, fp)
		LANG.emit_global_methods(ctx, fp)

		#############################################################
		# EPILOG						    #
		#############################################################

		LANG.emit_separator(ctx, fp)
		LANG.emit_epilogPubInt(ctx, fp)

		#############################################################

		fp.close()

	except IOError:
		cb.utils.error('Could not open \'%s.h\' !' % ctx['name'])

#############################################################################

def implementation(ctx):
	LANG = ctx['lang']

	try:
		fp = open('%s_internal.h' % ctx['name'], 'wt')

		#############################################################
		# PROLOG						    #
		#############################################################

		LANG.emit_prologPrivInt(ctx, fp)

		#############################################################
		# CONSTRAINTS						    #
		#############################################################

		LANG.emit_separator(ctx, fp)
		LANG.emit_constraints(ctx, fp)

		#############################################################
		# METHODS						    #
		#############################################################

		LANG.emit_separator(ctx, fp)
		LANG.emit_internal_methods(ctx, fp)

		#############################################################
		# EPILOG						    #
		#############################################################

		LANG.emit_separator(ctx, fp)
		LANG.emit_epilogPrivInt(ctx, fp)

		#############################################################

		fp.close()

	except IOError:
		cb.utils.error('Could not open \'%s_internal.h\' !' % ctx['name'])

	##

	try:
		fp = open('%s.c' % ctx['name'], 'wt')

		#############################################################
		# PROLOG						    #
		#############################################################

		LANG.emit_prologImp(ctx, fp)

		#############################################################
		# CONSTRAINTS						    #
		#############################################################

		LANG.emit_separator(ctx, fp)
		LANG.emit_global_constraints(ctx, fp)

		#############################################################
		# CTORS							    #
		#############################################################

		LANG.emit_separator(ctx, fp)
		LANG.emit_global_ctor(ctx, fp)

		#############################################################
		# DTORS							    #
		#############################################################

		LANG.emit_separator(ctx, fp)
		LANG.emit_global_dtor(ctx, fp)

		#############################################################
		# EPILOG						    #
		#############################################################

		LANG.emit_separator(ctx, fp)
		LANG.emit_epilogImp(ctx, fp)

		#############################################################

		fp.close()

	except IOError:
		cb.utils.error('Could not open \'%s_internal.h\' !' % ctx['name'])

	##

	for p in ctx['imp_profiles']:

		try:
			fp = open('%s_%s.c' % (ctx['name'], p), 'wt')

			#####################################################
			# PROLOG					    #
			#####################################################

			LANG.emit_prologImp(ctx, fp)

			#####################################################
			# PROFILE					    #
			#####################################################

			LANG.emit_separator(ctx, fp)
			LANG.emit_global_profile(ctx, fp, p)

			#####################################################
			# METHODS					    #
			#####################################################

			LANG.emit_separator(ctx, fp)
			LANG.emit_methods(ctx, fp, p)

			#####################################################
			# CTORS						    #
			#####################################################

			LANG.emit_separator(ctx, fp)
			LANG.emit_profile_ctor(ctx, fp, p)

			#####################################################
			# DTORS						    #
			#####################################################

			LANG.emit_separator(ctx, fp)
			LANG.emit_profile_dtor(ctx, fp, p)

			#####################################################
			# EPILOG					    #
			#####################################################

			LANG.emit_separator(ctx, fp)
			LANG.emit_epilogImp(ctx, fp)

			#####################################################

			fp.close()

		except IOError:
			cb.utils.error('Could not open \'%s_internal.h\' !' % ctx['name'])

#############################################################################


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

	#####################################################################

	try:
		fp = open('%s.h' % ctx['name'], 'wt')

		#############################################################
		# PROLOG						    #
		#############################################################

		LANG.emit_intPubProlog(ctx, fp)

		#############################################################
		# TYPES							    #
		#############################################################

		LANG.emit_COMMENT(ctx, fp, 'TYPES')
		LANG.emit_impPubTypes(ctx, fp)

		#############################################################
		# DEFINITIONS						    #
		#############################################################

		LANG.emit_COMMENT(ctx, fp, 'IMPLEMENTATION')
		LANG.emit_impPubDefinitions(ctx, fp)

		#############################################################
		# EXTENSION STRUCTS					    #
		#############################################################

		LANG.emit_separator(ctx, fp)
		LANG.emit_impPubExtensionStructs(ctx, fp)

		#############################################################
		# METHOD PROTOTYPES					    #
		#############################################################

		LANG.emit_separator(ctx, fp)
		LANG.emit_impPubMethodPrototypes(ctx, fp)

		#############################################################
		# EPILOG						    #
		#############################################################

		LANG.emit_separator(ctx, fp)
		LANG.emit_intPubEpilog(ctx, fp)

		#############################################################

		fp.close()

	except IOError:
		cb.utils.error('Could not open \'%s.h\' !' % ctx['name'])

	#####################################################################

	try:
		fp = open('%s_internal.h' % ctx['name'], 'wt')

		#############################################################
		# PROLOG						    #
		#############################################################

		LANG.emit_intPrivProlog(ctx, fp)

		#############################################################
		# CONSTRAINTS						    #
		#############################################################

		LANG.emit_separator(ctx, fp)
		LANG.emit_impPrivConstraints(ctx, fp)

		#############################################################
		# METHOD PROTOTYPES					    #
		#############################################################

		LANG.emit_separator(ctx, fp)
		LANG.emit_impPrivMethodPrototypes(ctx, fp)

		#############################################################
		# EPILOG						    #
		#############################################################

		LANG.emit_separator(ctx, fp)
		LANG.emit_intPrivEpilog(ctx, fp)

		#############################################################

		fp.close()

	except IOError:
		cb.utils.error('Could not open \'%s_internal.h\' !' % ctx['name'])

#############################################################################

def implementation(ctx):
	LANG = ctx['lang']

	#####################################################################

	try:
		fp = open('%s.c' % ctx['name'], 'wt')

		#############################################################
		# PROLOG						    #
		#############################################################

		LANG.emit_impProlog(ctx, fp)

		#############################################################
		# CONSTRAINTS						    #
		#############################################################

		LANG.emit_separator(ctx, fp)
		LANG.emit_impConstraints(ctx, fp)

		#############################################################
		# DTORS							    #
		#############################################################

		LANG.emit_separator(ctx, fp)
		LANG.emit_impDtor(ctx, fp)

		#############################################################
		# CTORS							    #
		#############################################################

		LANG.emit_separator(ctx, fp)
		LANG.emit_impCtor(ctx, fp)

		#############################################################
		# HIGH LEVEL METHODS					    #
		#############################################################

		LANG.emit_separator(ctx, fp)
		LANG.emit_impHighLevelMethods(ctx, fp)

		#############################################################
		# EPILOG						    #
		#############################################################

		LANG.emit_separator(ctx, fp)
		LANG.emit_impEpilog(ctx, fp)

		#############################################################

		fp.close()

	except IOError:
		cb.utils.error('Could not open \'%s_internal.h\' !' % ctx['name'])

	#####################################################################

	for p in ctx['imp_profiles']:

		try:
			fp = open('%s_%s.c' % (ctx['name'], p), 'wt')

			#####################################################
			# PROLOG					    #
			#####################################################

			LANG.emit_impProfileProlog(ctx, fp, p)

			#####################################################
			# METHODS					    #
			#####################################################

			LANG.emit_separator(ctx, fp)
			LANG.emit_impProfileMethods(ctx, fp, p)

			#####################################################
			# DTORS						    #
			#####################################################

			LANG.emit_separator(ctx, fp)
			LANG.emit_impProfileDtor(ctx, fp, p)

			#####################################################
			# CTORS						    #
			#####################################################

			LANG.emit_separator(ctx, fp)
			LANG.emit_impProfileCtor(ctx, fp, p)

			#####################################################
			# EPILOG					    #
			#####################################################

			LANG.emit_separator(ctx, fp)
			LANG.emit_impEpilog(ctx, fp)

			#####################################################

			fp.close()

		except IOError:
			cb.utils.error('Could not open \'%s_internal.h\' !' % ctx['name'])

#############################################################################


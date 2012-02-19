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
	#####################################################################

	NAME = ctx.name
	LANG = ctx.lang

	#####################################################################

	try:
		fp = open('%s.%s' % (NAME, ctx.intext), 'wt')

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

		LANG.emit_COMMENT(ctx, fp, 'INTERFACE')
		LANG.emit_impPubDefinitions(ctx, fp)

		#############################################################
		# METHODS						    #
		#############################################################

		LANG.emit_COMMENT(ctx, fp, 'METHODS')
		LANG.emit_impPubMethods(ctx, fp)

		#############################################################
		# EPILOG						    #
		#############################################################

		LANG.emit_separator(ctx, fp)
		LANG.emit_intPubEpilog(ctx, fp)

		#############################################################

		fp.close()

	except IOError:
		cb.utils.error('Could not open \'%s.h\' !' % NAME)

	#####################################################################

	try:
		fp = open('%s_internal.%s' % (NAME, ctx.intext), 'wt')

		#############################################################
		# PROLOG						    #
		#############################################################

		LANG.emit_intPrivProlog(ctx, fp)

		#############################################################
		# TYPES							    #
		#############################################################

		LANG.emit_COMMENT(ctx, fp, 'TYPES')
		LANG.emit_impPrivTypes(ctx, fp)

		#############################################################
		# CONSTRAINTS						    #
		#############################################################

		LANG.emit_separator(ctx, fp)
		LANG.emit_impPrivConstraints(ctx, fp)

		#############################################################
		# METHODS						    #
		#############################################################

		LANG.emit_separator(ctx, fp)
		LANG.emit_impPrivMethods(ctx, fp)

		#############################################################
		# EPILOG						    #
		#############################################################

		LANG.emit_separator(ctx, fp)
		LANG.emit_intPrivEpilog(ctx, fp)

		#############################################################

		fp.close()

	except IOError:
		cb.utils.error('Could not open \'%s_internal.h\' !' % NAME)

#############################################################################

def implementation(ctx):
	#####################################################################

	NAME = ctx.name
	LANG = ctx.lang

	#####################################################################

	try:
		fp = open('%s.%s' % (NAME, ctx.impext), 'wt')

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
		# METHODS						    #
		#############################################################

		LANG.emit_separator(ctx, fp)
		LANG.emit_impMethods(ctx, fp)

		#############################################################
		# EPILOG						    #
		#############################################################

		LANG.emit_separator(ctx, fp)
		LANG.emit_impEpilog(ctx, fp)

		#############################################################

		fp.close()

	except IOError:
		cb.utils.error('Could not open \'%s_internal.h\' !' % NAME)

	#####################################################################

	for p in ctx.imp_profiles:

		try:
			fp = open('%s_%s.%s' % (NAME, p, ctx.impext), 'wt')
	
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
			cb.utils.error('Could not open \'%s_internal.h\' !' % NAME)

#############################################################################


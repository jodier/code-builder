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

def checkTypes(ctx, TYPES):
	#####################################################################
	# PASS ONE							    #
	#####################################################################

	for t in TYPES:

		if t['name'] in ctx.primitives:
			cb.utils.error(ctx, 'Duplicated type \'%s\' !' % t['name'])
		else:
			ctx.primitives.add(t['name'])

	#####################################################################
	# PASS TWO							    #
	#####################################################################

	for t in TYPES:
		#############################################################
		# BASE TYPE						    #
		#############################################################

		if t['class'] == 'base':

			types = cb.utils.extractTypes(ctx, t['from'])

			for type in types:

				if type in ctx.primitives:
					if type == t['name']:
						cb.utils.error(ctx, 'Recursif type \'%s\' !' % type)
				else:
					cb.utils.error(ctx, 'Undefined type \'%s\' !' % type)

		#############################################################
		# ENUM TYPE						    #
		#############################################################

		if t['class'] == 'enum':

			values = t['values']

			for i in xrange(0 + 0, len(values)):
				for j in xrange(i + 1, len(values)):

					if values[i]['name'] == values[j]['name']:
						cb.utils.error(ctx, 'Duplicated values \'%s\' for type \'%s\' !' % (values[i]['name'], t['name']))

		#############################################################
		# STRUCT TYPE						    #
		#############################################################

		if t['class'] == 'struct':

			fields = t['fields']

			for i in xrange(0 + 0, len(fields)):
				for j in xrange(i + 1, len(fields)):

					if fields[i]['name'] == fields[j]['name']:
						cb.utils.error(ctx, 'Duplicated fields \'%s\' for type \'%s\' !' % (fields[i]['name'], t['name']))

			##

			for f in fields:

				types = cb.utils.extractTypes(ctx, f['type'])

				for type in types:

					if type in ctx.primitives:
						if type == t['name']:
							cb.utils.debug(ctx, 'Recursif type \'%s\' !' % type)
					else:
						cb.utils.error(ctx, 'Undefined type \'%s\' !' % type)

#############################################################################

def checkInterfacePublic(ctx):
	#####################################################################
	# TYPES								    #
	#####################################################################

	checkTypes(ctx, ctx.int_pub_types)

	#####################################################################
	# EXTENSIONS							    #
	#####################################################################

	INT_EXTENSIONS = ctx.int_pub_extensions

	#####################################################################

	for e in INT_EXTENSIONS:

		for m in e['methods']:

			for p in m['params']:

				types = cb.utils.extractTypes(ctx, p['type'])

				for type in types:

					if not type in ctx.primitives:
						cb.utils.error(ctx, 'Undefined type \'%s\' !' % type)

			##

			ps = m['params']

			for i in xrange(0 + 0, len(ps)):
				for j in xrange(i + 1, len(ps)):

					if ps[i]['name'] == ps[j]['name']:
						cb.utils.error(ctx, 'Duplicated param \'%s\' !' % ps[i]['name'])

		ms = e['methods']

		for i in xrange(0 + 0, len(ms)):
			for j in xrange(i + 1, len(ms)):

				if ms[i]['name'] == ms[j]['name']:
					cb.utils.error(ctx, 'Duplicated method \'%s\' !' % ms[i]['name'])

	es = INT_EXTENSIONS

	for i in xrange(0 + 0, len(es)):
		for j in xrange(i + 1, len(es)):

			if es[i]['name'] == es[j]['name']:
				cb.utils.error(ctx, 'Duplicated extension \'%s\' !' % es[i]['name'])

	#####################################################################
	# PROFILES							    #
	#####################################################################

	INT_PROFILES = ctx.int_pub_profiles

	#####################################################################

	for p in INT_PROFILES:

		for cp in p['ctor_params']:

			types = cb.utils.extractTypes(ctx, cp['type'])

			for type in types:

				if not type in ctx.primitives:
					cb.utils.error(ctx, 'Undefined type \'%s\' !' % type)

		##

		for dp in p['dtor_params']:

			types = cb.utils.extractTypes(ctx, dp['type'])

			for type in types:

				if not type in ctx.primitives:
					cb.utils.error(ctx, 'Undefined type \'%s\' !' % type)

		##

		cps = p['ctor_params']

		for i in xrange(0 + 0, len(cps)):
			for j in xrange(i + 1, len(cps)):

				if cps[i]['name'] == cps[j]['name']:
					cb.utils.error(ctx, 'Duplicated ctor_param \'%s\' !' % cps[i]['name'])

		##

		dps = p['dtor_params']

		for i in xrange(0 + 0, len(dps)):
			for j in xrange(i + 1, len(dps)):

				if dps[i]['name'] == dps[j]['name']:
					cb.utils.error(ctx, 'Duplicated dtor_param \'%s\' !' % dps[i]['name'])

#############################################################################

def checkInterfacePrivate(ctx):
	#####################################################################
	# TYPES								    #
	#####################################################################

	checkTypes(ctx, ctx.int_priv_types)

#############################################################################

def checkExtraXtor(ctx, EXTRAS, CTORS, DTORS):
	#####################################################################
	# EXTRAS							    #
	#####################################################################

	if len(EXTRAS) > 1:
		cb.utils.error(ctx, 'Only one extra allowed !')

	for e in EXTRAS:
		for c in e:
			if len(c['txts']) == 0:
				cb.utils.error(ctx, 'At least one CDATA node needed for extra !')

			if len(c['condition'].strip()) > 0:
				cb.utils.ooops(ctx, 'Only unconditional extra allowed !')

	#####################################################################
	# CTORS								    #
	#####################################################################

	if len(CTORS) > 1:
		cb.utils.error(ctx, 'Only one ctor allowed !')

	for x in CTORS:
		for c in x:
			if len(c['txts']) == 0:
				cb.utils.error(ctx, 'At least one CDATA node needed for ctor !')

	#####################################################################
	# DTORS								    #
	#####################################################################

	if len(DTORS) > 1:
		cb.utils.error(ctx, 'Only one dtor allowed !')

	for x in DTORS:
		for c in x:
			if len(c['txts']) == 0:
				cb.utils.error(ctx, 'At least one CDATA node needed for dtor !')

#############################################################################

def checkCodes(ctx, CODES):
	#####################################################################
	# CODES								    #
	#####################################################################

	for c in CODES:

		if len(c['txts']) == 0:
			cb.utils.error(ctx, 'Only one CDATA allowed for method !')

#############################################################################

def checkImplementation(ctx):
	#####################################################################
	# PROFILES							    #
	#####################################################################

	IMP_PROFILES = ctx.imp_profiles

	#####################################################################

	for p in IMP_PROFILES:

		PRO = cb.utils.int_getProfile(ctx, p)
		if PRO is None:
			cb.utils.error(ctx, 'Undefined profile \'%s\' !' % p)

		else:
			#####################################################
			# EXTENSIONS					    #
			#####################################################

			IMP_EXTENSIONS = IMP_PROFILES[p]['extensions']

			#####################################################

			for e in IMP_EXTENSIONS:

				EXT = cb.utils.int_getExtension(ctx, e)
				if EXT is None:
					cb.utils.error(ctx, 'Undefined extension \'%s\' !' % e)

				else:
					#####################################
					# METHODS			    #
					#####################################

					IMP_METHODS = IMP_EXTENSIONS[e]['methods']

					#####################################

					for m in IMP_METHODS:

						MET = cb.utils.int_getMethod(EXT, m)
						if MET is None:
							cb.utils.error(ctx, 'Undefined method \'%s\' !' % m)

						checkCodes(ctx,
							IMP_METHODS[m]
						)

				checkExtraXtor(ctx,
					IMP_EXTENSIONS[e]['extras'],
					IMP_EXTENSIONS[e]['ctors'],
					IMP_EXTENSIONS[e]['dtors']
				)

		checkExtraXtor(ctx,
			IMP_PROFILES[p]['extras'],
			IMP_PROFILES[p]['ctors'],
			IMP_PROFILES[p]['dtors']
		)

	#####################################################################

	checkExtraXtor(ctx,
		ctx.imp_extras,
		ctx.imp_ctors,
		ctx.imp_dtors
	)

#############################################################################


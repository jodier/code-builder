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
	#####################################################################
	# TYPES								    #
	#####################################################################

	INT_TYPE = ctx['int_types']

	#####################################################################

	L = list(ctx['lang'].PRIMITIVES)

	#####################################################################

	for t in INT_TYPE:

		T = t['name']

		if T in L:
			cb.utils.error(ctx, 'Re-defined type \'%s\' !' % T)
		else:
			L.append(T)

	#####################################################################

	for t in INT_TYPE:

		#############################################################
		# BASE TYPE						    #
		#############################################################

		if t['class'] == 'base':

			name = t['from']

			if name in L:
				if name == t['name']:
					cb.utils.error(ctx, 'Recursif type \'%s\' !' % name)
			else:
				cb.utils.error(ctx, 'Undefined type \'%s\' !' % name)

		#############################################################
		# ENUM TYPE						    #
		#############################################################

		if t['class'] == 'enum':

			values = t['values']

			for i in xrange(0 + 0, len(values)):
				for j in xrange(i + 1, len(values)):

					if values[i]['name'] == values[j]['name']:
						cb.utils.error(ctx, 'Duplicated values \'%s\' !' % values[i]['name'])

		#############################################################
		# STRUCT TYPE						    #
		#############################################################

		if t['class'] == 'struct':

			fields = t['fields']

			for i in xrange(0 + 0, len(fields)):
				for j in xrange(i + 1, len(fields)):

					if fields[i]['name'] == fields[j]['name']:
						cb.utils.error(ctx, 'Duplicated fields \'%s\' !' % fields[i]['name'])

			##

			for f in fields:

				name = f['type']

				if name in L:
					if name == t['name']:
						cb.utils.debug(ctx, 'Recursif type \'%s\' !' % name)
				else:
					cb.utils.error(ctx, 'Undefined type \'%s\' !' % name)

	#####################################################################
	# EXTENSIONS							    #
	#####################################################################

	INT_EXTENSIONS = ctx['int_extensions']

	#####################################################################

	for e in INT_EXTENSIONS:

		for m in e['methods']:

			for p in m['params']:

				if not p['type'] in L:
					cb.utils.error(ctx, 'Undefined type \'%s\' !' % p['type'])

			##

			p = m['params']

			for i in xrange(0 + 0, len(p)):
				for j in xrange(i + 1, len(p)):

					if p[i]['name'] == p[j]['name']:
						cb.utils.error(ctx, 'Duplicated param \'%s\' and \'%s\' !' % (p[i]['name'], p[j]['name']))

		m = e['methods']

		for i in xrange(0 + 0, len(m)):
			for j in xrange(i + 1, len(m)):

				if m[i]['name'] == m[j]['name']:
					cb.utils.error(ctx, 'Duplicated method \'%s\' and \'%s\' !' % (m[i]['name'], m[j]['name']))

	e = INT_EXTENSIONS

	for i in xrange(0 + 0, len(e)):
		for j in xrange(i + 1, len(e)):

			if e[i]['name'] == e[j]['name']:
				cb.utils.error(ctx, 'Duplicated extension \'%s\' and \'%s\' !' % (e[i]['name'], e[j]['name']))

#############################################################################
# IMPLEMENTATION							    #
#############################################################################

def checkExtraXtor(ctx, extras, ctors, dtors):

	if len(extras) > 1:
		cb.utils.error(ctx, 'Only one extra code allowed !')
	elif len(extras) == 1:
		for c in extras[0]:
			if c['condition'] != '':
				cb.utils.error(ctx, 'Only unconditional extra allowed !')
			if len(c['txts']) > 1:
				cb.utils.error(ctx, 'Only one CDATA allowed in extra !')

	if len(ctors) > 1:
		cb.utils.error(ctx, 'Only one ctors code allowed !')
	elif len(ctors) == 1:
		for c in ctors[0]:
			if len(c['txts']) > 1:
				cb.utils.error(ctx, 'Only one CDATA allowed in ctor !')

	if len(dtors) > 1:
		cb.utils.error(ctx, 'Only one dtors code allowed !')
	elif len(dtors) == 1:
		for c in dtors[0]:
			if len(c['txts']) > 1:
				cb.utils.error(ctx, 'Only one CDATA allowed in dtor !')

#############################################################################

def implementation(ctx):
	#####################################################################
	# IMPLEMENTATION						    #
	#####################################################################

	checkExtraXtor(ctx,
		ctx['imp_extras'],
		ctx['imp_ctors'],
		ctx['imp_dtors']
	)

	#####################################################################
	# PROFILES							    #
	#####################################################################

	IMP_PROFILES = ctx['imp_profiles']

	for p in IMP_PROFILES:

		PRO = cb.utils.int_getProfile(ctx, p)
		if PRO is None:
			cb.utils.error(ctx, 'Undefined profile \'%s\' !' % p)

		##

		IMP_EXTENSIONS = IMP_PROFILES[p]['extensions']

		for e in IMP_EXTENSIONS:

			EXT = cb.utils.int_getExtension(ctx, e)
			if EXT is None:
				cb.utils.error(ctx, 'Undefined extension \'%s\' !' % e)

			else:
				IMP_METHODS = IMP_EXTENSIONS[e]['methods']

				for m in IMP_METHODS:

					MET = cb.utils.int_getMethod(EXT, m)
					if MET is None:
						cb.utils.error(ctx, 'Undefined method \'%s\' !' % m)

					for met in IMP_METHODS[m]:

						if len(met['txts']) > 1:
							cb.utils.error(ctx, 'Only one CDATA allowed in method \'%s\' !' % m)

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

#############################################################################


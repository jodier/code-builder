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

	INT_TYPES_TYPES   = ctx['int_types']['types'  ]
	INT_TYPES_ENUMS   = ctx['int_types']['enums'  ]
	INT_TYPES_STRUCTS = ctx['int_types']['structs']

	#####################################################################

	L = []

	for name in INT_TYPES_TYPES:
		L.append(name)
	for name in INT_TYPES_ENUMS:
		L.append(name)
	for name in INT_TYPES_STRUCTS:
		L.append(name)

	L.extend(ctx['lang'].PRIMITIVES)

	#####################################################################

	for t in INT_TYPES_TYPES:

		T = INT_TYPES_TYPES[t]['from']

		if T in L:
			if T == t:
				cb.utils.error(ctx, 'Recursif type \'%s\' !' % T)
		else:
			cb.utils.error(ctx, 'Undefined type \'%s\' !' % T)

	#####################################################################

	for t in INT_TYPES_ENUMS:

		for u in INT_TYPES_ENUMS[t]:

			v = INT_TYPES_ENUMS[t][u]

			for i in xrange(0 + 0, len(v)):
				for j in xrange(i + 1, len(v)):

					if v[i]['name'] == v[j]['name']:
						cb.utils.error(ctx, 'Duplicated values \'%s\' and \'%s\' !' % (v[i]['name'], v[j]['name']))

	#####################################################################

	for t in INT_TYPES_STRUCTS:

		for u in INT_TYPES_STRUCTS[t]:

			v = INT_TYPES_STRUCTS[t][u]

			for i in xrange(0 + 0, len(v)):
				for j in xrange(i + 1, len(v)):

					if v[i]['name'] == v[j]['name']:
						cb.utils.error(ctx, 'Duplicated fields \'%s\' and \'%s\' !' % (v[i]['name'], v[j]['name']))

			##

			for w in v:

				T = w['type']

				if T in L:
					if T == t:
						cb.utils.debug(ctx, 'Undefined type \'%s\' !' % T)
				else:
					cb.utils.error(ctx, 'Undefined type \'%s\' !' % T)

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

def implementation(ctx):

	#####################################################################
	# EXTENSIONS							    #
	#####################################################################

	INT_PROFILES = ctx['int_profiles']
	IMP_PROFILES = ctx['imp_profiles']

	#####################################################################

	for p in IMP_PROFILES:

		if not INT_PROFILES.has_key(p):
			cb.utils.error(ctx, 'Undefined profile \'%s\' !' % p)

		##

		for e in IMP_PROFILES[p]['extensions']:

			EXT = cb.utils.getExtension(ctx, e)

			if EXT is None:
				cb.utils.error(ctx, 'Undefined extension \'%s\' !' % EXT)

			else:
				for m in IMP_PROFILES[p]['extensions'][e]['methods']:

					MET = cb.utils.getMethod(EXT, m)

					if MET is None:
						cb.utils.error(ctx, 'Undefined method \'%s\' !' % MET)

#############################################################################


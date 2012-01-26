#############################################################################
# Author  : Jerome ODIER, Christophe SMEKENS, Francois SMEKENS
# Email   : ---@gmail.com, ---@gmail.com, ---@gmail.com
#
# Version : 1.0 beta (2012)
#
#
# This file is part of API-BUILDER.
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

PRIMITIVE = [
	'void',
	'int8_t',
	'uint8_t',
	'int16_t',
	'uint16_t',
	'int32_t',
	'uint32_t',
	'int64_t',
	'uint64_t',
	'bool',
	'float',
	'double',
]

#############################################################################

QUALIFIER = [
	'const',
	'register',
	'volatile',
]

#############################################################################

def generate_prolog(name, major, minor, a):
	print('/* Authors : %s' % a['authors'])
	print(' * Emails  : %s' % a['emails'])
	print(' *')
	print(' * Version : %d.%d (%s)' % (major, minor, a['date']))
	print(' *')
	print(' * %s' % a['description'])	
	print(' */')
	print('')

	generate_separator()

	print('#ifndef __%s_H' % name.upper())
	print('#define __%s_H' % name.upper())
	print('')

	generate_separator()

	print('#include <stddef.h>')
	print('')

#############################################################################

def generate_epilog(name):

	print('#endif /* __%s_H */' % name.upper())

	print('')
	generate_separator()

#############################################################################

def generate_separator():
	print('/*-------------------------------------------------------------------------*/')
	print('')

#############################################################################

def generate_comment(s):
	print('/* %s */' % s)
	print('')

#############################################################################

def generate_box(s):
	nr = 8 - len(s) / 8

	print('/*-------------------------------------------------------------------------*/')
	print('/* %s%s   */' % (s, ''.join(['\t' for i in xrange(nr)])))
	print('/*-------------------------------------------------------------------------*/')
	print('')

#############################################################################

def generate_type(t):
	print('typedef %s %s;' % (t[0], t[1]['from']))

#############################################################################

def generate_enum(t, incCnt):
	print('typedef enum %s' % t[0])
	print('{')

	for u in t[1]:
		for v in t[1][u]:
			print('\t%s = 0x%X,' % (v['name'], incCnt()))

	print('')
	print('} %s;' % t[0])

#############################################################################

def generate_struct(t):
	print('typedef struct %s' % t[0])
	print('{')

	for u in t[1]:
		for v in t[1][u]:
			print('\t%s %s;' % (v['type'], v['name']))

	print('')
	print('} %s;' % t[0])

#############################################################################

def generate_profile(p, incCnt):
	print('#define PROFILE_%s 0x%X' % (p.upper(), incCnt()))

#############################################################################

def generate_prototype(m, prefix, suffix = None):

	if suffix is None:
		proto = '%s %s_%s' % (m['type'], prefix, m['name'])
	else:
		proto = '%s %s_%s_%s' % (m['type'], prefix, m['name'], suffix)

	proto += '('

	if len(m['params']) > 0:
		for p in m['params']:
			proto += '%s %s,' % (p['type'], p['name'])
	else:
		proto += 'void,'

	print(proto[: -1] + ');')

#############################################################################


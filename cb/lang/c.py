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

PRIMITIVES = [
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

QUALIFIERS = [
	'const',
	'register',
	'volatile',
]

#############################################################################

def generate_separator(ctx):
	print('/*-------------------------------------------------------------------------*/')
	print('')

#############################################################################

def generate_COMMENT(ctx, s):
	print('/*-------------------------------------------------------------------------*/')
	print('/* %s%s   */' % (s, ''.join([' ' for i in xrange(69 - len(s))])))
	print('/*-------------------------------------------------------------------------*/')
	print('')

#############################################################################

def generate_comment(ctx, s):
	n = 5
	l = len(s)

	if l > 5:
		n -= 1
		l -= 5

	print('/*----------------------------------*/')
	print('/* %s%s   */' % (s, ''.join([' ' for i in xrange(30 - len(s))])))
	print('/*----------------------------------*/')
	print('')

#############################################################################

def generate_prolog(ctx):
	INT_ASSET = ctx['int_asset']

	print('/* Authors : %s' % INT_ASSET['authors'])
	print(' * Emails  : %s' % INT_ASSET['emails'])
	print(' *')
	print(' * Version : %d.%d (%s)' % (ctx['major'], ctx['minor'], INT_ASSET['date']))
	print(' *')
	print(' * %s' % INT_ASSET['description'])	
	print(' */')
	print('')

	generate_separator(ctx)

	print('#ifndef __%s_H' % ctx['name'].upper())
	print('#define __%s_H' % ctx['name'].upper())
	print('')

	generate_separator(ctx)

	print('#include <stddef.h>')
	print('')

#############################################################################

def generate_epilog(ctx):
	print('#endif /* __%s_H */' % ctx['name'].upper())

	print('')
	generate_separator(ctx)

#############################################################################

def generate_type(ctx, t):
	print('typedef %s %s;' % (t[0], t[1]['from']))

#############################################################################

def generate_enum(ctx, t):
	print('typedef enum %s' % t[0])
	print('{')

	for u in t[1]:
		for v in t[1][u]:
			print('\t%s = 0x%X,' % (v['name'], cb.utils.getCnt(ctx)))

	print('')
	print('} %s;' % t[0])

#############################################################################

def generate_struct(ctx, t):
	print('typedef struct %s' % t[0])
	print('{')

	for u in t[1]:
		for v in t[1][u]:
			print('\t%s %s;' % (v['type'], v['name']))

	print('')
	print('} %s;' % t[0])

#############################################################################

def generate_definitions(ctx):
	name = ctx['name']
	NAME = ctx['name'].upper()

	#####################################################################
	# PROFILES							    #
	#####################################################################

	generate_comment(ctx, 'PROFILES')

	print('typedef enum %s_profiles_e' % name)
	print('{')

	for p in ctx['int_profiles']:
		print('\t%s_%s\t= 0x%X,' % (NAME, p.upper(), cb.utils.getCnt(ctx)))

	print('')
	print('} %s_profiles_t;' % name)

	print('')

	#####################################################################
	# EXTENTIONS							    #
	#####################################################################

	generate_comment(ctx, 'EXTENTIONS')

	print('typedef enum %s_extentions_e' % name)
	print('{')

	for e in ctx['int_extensions']:
		print('\t%s_%s\t= 0x%X,' % (NAME, e['name'].upper(), cb.utils.getCnt(ctx)))

	print('')
	print('} %s_extentions_t;' % name)

	print('')

	#####################################################################
	# METHODS							    #
	#####################################################################

	generate_comment(ctx, 'METHODS')

	print('typedef enum %s_methods_e' % name)
	print('{')

	for e in ctx['int_extensions']:

		for m in e['methods']:
			print('\t%s_%s_%s\t= 0x%X,' % (NAME, e['name'].upper(), m['name'].upper(), cb.utils.getCnt(ctx)))

	print('')
	print('} %s_methods_t;' % name)

#############################################################################

def generate_extension_struct(ctx):
	print('typedef struct %s_s' % ctx['name'])
	print('{')

	for e in ctx['int_extensions']:

		print('\tstruct {')

		for m in e['methods']:

			print('\t\t'),
			generate_prototype1(ctx, m, None, None)
			print('\t\t'),
			generate_prototype1(ctx, m, None, 'check')
			print('\t\t'),
			generate_prototype1(ctx, m, None, 'best')
			print('')

		print('\t} %s;\n' % e['name'])		

	print('} %s_t;' % ctx['name'])

#############################################################################

def generate_extension_profiles(ctx):

	for e in ctx['int_profiles']:

		print('extern %s_t %s_%s;' % (ctx['name'], ctx['name'], e))

#############################################################################

def generate_global_methods(ctx):
	name = ctx['name']

	generate_comment(ctx, 'LOW LEVEL METHODS')

	print('bool %s_initialize(void);' % name)
	print('bool %s_finalize(void);' % name)
	print('')
	print('int %s_getMajor(void);' % name)
	print('int %s_getMinor(void);' % name)
	print('')
	print('int %s_getProNr(void);' % name)
	print('const char *%s_getProName(int);' % name)
	print('const char *%s_getProDesc(int);' % name)
	print('')
	print('int %s_getExtNr(int);' % name)
	print('const char *%s_getExtName(int, int);' % name)
	print('const char *%s_getExtDesc(int, int);' % name)
	print('')
	print('int %s_getMetNr(int, int);' % name)
	print('const char *%s_getMetName(int, int, int);' % name)
	print('const char *%s_getMetDesc(int, int, int);' % name)

	print('')

	generate_comment(ctx, 'HIGH LEVEL METHODS')

	print('%s_t *%s_getInterface(%s_profiles_t);' % (name, name, name))
	print('')
	print('bool %s_checkExt(%s_profiles_t, %s_extentions_t);' % (name, name, name))
	print('const char *%s_getExtName(%s_profiles_t, %s_extentions_t);' % (name, name, name))
	print('const char *%s_getExtDesc(%s_profiles_t, %s_extentions_t);' % (name, name, name))
	print('')
	print('bool %s_checkMet(%s_profiles_t, %s_methods_t);' % (name, name, name))
	print('const char *%s_getMetName(%s_profiles_t, %s_methods_t);' % (name, name, name))
	print('const char *%s_getMetDesc(%s_profiles_t, %s_methods_t);' % (name, name, name))

	print('')

#############################################################################

def generate_prototype1(ctx, m, prefix = None, suffix = None):

	proto = '%s (* ' % m['type']

	if not prefix is None:
		proto += '%s_' % prefix
	proto += m['name']
	if not suffix is None:
		proto += '_%s' % suffix

	proto += ')('

	if len(m['params']) > 0:
		for p in m['params']:
			proto += '%s %s,' % (p['type'], p['name'])
	else:
		proto += 'void,'

	print(proto[: -1] + ');')

#############################################################################

def generate_prototype2(ctx, m, prefix = None, suffix = None):

	proto = '%s ' % m['type']

	if not prefix is None:
		proto += '%s_' % prefix
	proto += m['name']
	if not suffix is None:
		proto += '_%s' % suffix

	proto += '('

	if len(m['params']) > 0:
		for p in m['params']:
			proto += '%s %s,' % (p['type'], p['name'])
	else:
		proto += 'void,'

	print(proto[: -1] + ');')

#############################################################################


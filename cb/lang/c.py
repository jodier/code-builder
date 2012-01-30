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

def generate_separator(ctx, fp):
	cb.utils.writeline(fp, '/*-------------------------------------------------------------------------*/')
	cb.utils.writeline(fp, '')

#############################################################################

def generate_COMMENT(ctx, fp, s):
	cb.utils.writeline(fp, '/*-------------------------------------------------------------------------*/')
	cb.utils.writeline(fp, '/* %s%s   */' % (s, ''.join([' ' for i in xrange(69 - len(s))])))
	cb.utils.writeline(fp, '/*-------------------------------------------------------------------------*/')
	cb.utils.writeline(fp, '')

#############################################################################

def generate_comment(ctx, fp, s):
	n = 5
	l = len(s)

	if l > 5:
		n -= 1
		l -= 5

	cb.utils.writeline(fp, '/*----------------------------------*/')
	cb.utils.writeline(fp, '/* %s%s   */' % (s, ''.join([' ' for i in xrange(30 - len(s))])))
	cb.utils.writeline(fp, '/*----------------------------------*/')
	cb.utils.writeline(fp, '')

#############################################################################

def generate_prolog(ctx, fp):
	INT_ASSET = ctx['int_asset']

	cb.utils.writeline(fp, '/* Authors : %s' % INT_ASSET['authors'])
	cb.utils.writeline(fp, ' * Emails  : %s' % INT_ASSET['emails'])
	cb.utils.writeline(fp, ' *')
	cb.utils.writeline(fp, ' * Version : %d.%d (%s)' % (ctx['major'], ctx['minor'], INT_ASSET['date']))
	cb.utils.writeline(fp, ' *')
	cb.utils.writeline(fp, ' * %s' % INT_ASSET['description'])	
	cb.utils.writeline(fp, ' */')
	cb.utils.writeline(fp, '')

	generate_separator(ctx, fp)

	cb.utils.writeline(fp, '#ifndef __%s_H' % ctx['name'].upper())
	cb.utils.writeline(fp, '#define __%s_H' % ctx['name'].upper())
	cb.utils.writeline(fp, '')

	generate_separator(ctx, fp)

	cb.utils.writeline(fp, '#include <stddef.h>')
	cb.utils.writeline(fp, '')

#############################################################################

def generate_epilog(ctx, fp):
	cb.utils.writeline(fp, '#endif /* __%s_H */' % ctx['name'].upper())

	cb.utils.writeline(fp, '')
	generate_separator(ctx, fp)

#############################################################################

def generate_type(ctx, fp, t):
	cb.utils.writeline(fp, 'typedef %s %s;' % (t[0], t[1]['from']))

#############################################################################

def generate_enum(ctx, fp, t):
	cb.utils.writeline(fp, 'typedef enum %s' % t[0])
	cb.utils.writeline(fp, '{')

	for u in t[1]:
		for v in t[1][u]:
			cb.utils.writeline(fp, '\t%s = 0x%X,' % (v['name'], cb.utils.getCnt(ctx)))

	cb.utils.writeline(fp, '')
	cb.utils.writeline(fp, '} %s;' % t[0])

#############################################################################

def generate_struct(ctx, fp, t):
	cb.utils.writeline(fp, 'typedef struct %s' % t[0])
	cb.utils.writeline(fp, '{')

	for u in t[1]:
		for v in t[1][u]:
			cb.utils.writeline(fp, '\t%s %s;' % (v['type'], v['name']))

	cb.utils.writeline(fp, '')
	cb.utils.writeline(fp, '} %s;' % t[0])

#############################################################################

def generate_definitions(ctx, fp):
	name = ctx['name']
	NAME = ctx['name'].upper()

	#####################################################################
	# PROFILES							    #
	#####################################################################

	generate_comment(ctx, fp, 'PROFILES')

	cb.utils.writeline(fp, 'typedef enum %s_profiles_e' % name)
	cb.utils.writeline(fp, '{')

	for p in ctx['int_profiles']:
		cb.utils.writeline(fp, '\t%s_%s = 0x%X,' % (NAME, p.upper(), cb.utils.getCnt(ctx)))

	cb.utils.writeline(fp, '')
	cb.utils.writeline(fp, '} %s_profiles_t;' % name)

	cb.utils.writeline(fp, '')

	#####################################################################
	# EXTENTIONS							    #
	#####################################################################

	generate_comment(ctx, fp, 'EXTENTIONS')

	cb.utils.writeline(fp, 'typedef enum %s_extentions_e' % name)
	cb.utils.writeline(fp, '{')

	for e in ctx['int_extensions']:
		cb.utils.writeline(fp, '\t%s_%s = 0x%X,' % (NAME, e['name'].upper(), cb.utils.getCnt(ctx)))

	cb.utils.writeline(fp, '')
	cb.utils.writeline(fp, '} %s_extentions_t;' % name)

	cb.utils.writeline(fp, '')

	#####################################################################
	# METHODS							    #
	#####################################################################

	generate_comment(ctx, fp, 'METHODS')

	cb.utils.writeline(fp, 'typedef enum %s_methods_e' % name)
	cb.utils.writeline(fp, '{')

	for e in ctx['int_extensions']:

		for m in e['methods']:
			cb.utils.writeline(fp, '\t%s_%s_%s = 0x%X,' % (NAME, e['name'].upper(), m['name'].upper(), cb.utils.getCnt(ctx)))

	cb.utils.writeline(fp, '')
	cb.utils.writeline(fp, '} %s_methods_t;' % name)

	cb.utils.writeline(fp, '')

#############################################################################

def generate_extension_structs(ctx, fp):
	cb.utils.writeline(fp, 'typedef struct %s_s' % ctx['name'])
	cb.utils.writeline(fp, '{')

	for e in ctx['int_extensions']:

		cb.utils.writeline(fp, '\tstruct {')

		for m in e['methods']:

			cb.utils.write(fp, '\t\t'),
			generate_prototype1(ctx, fp, m, None, None)
			cb.utils.write(fp, '\t\t'),
			generate_prototype1(ctx, fp, m, None, 'check')
			cb.utils.write(fp, '\t\t'),
			generate_prototype1(ctx, fp, m, None, 'best')
			cb.utils.writeline(fp, '')

		cb.utils.writeline(fp, '\t} %s;\n' % e['name'])		

	cb.utils.writeline(fp, '} %s_t;' % ctx['name'])

	cb.utils.writeline(fp, '')

#############################################################################

def generate_extension_profiles(ctx, fp):

	for e in ctx['int_profiles']:

		cb.utils.writeline(fp, 'extern %s_t %s_%s;' % (ctx['name'], ctx['name'], e))

	cb.utils.writeline(fp, '')

#############################################################################

def generate_global_methods(ctx, fp):
	name = ctx['name']

	generate_comment(ctx, fp, 'LOW LEVEL METHODS')

	cb.utils.writeline(fp, 'bool %s_initialize(void);' % name)
	cb.utils.writeline(fp, 'bool %s_finalize(void);' % name)
	cb.utils.writeline(fp, '')
	cb.utils.writeline(fp, 'int %s_getMajor(void);' % name)
	cb.utils.writeline(fp, 'int %s_getMinor(void);' % name)
	cb.utils.writeline(fp, '')
	cb.utils.writeline(fp, 'int %s_getProNr(void);' % name)
	cb.utils.writeline(fp, 'const char *%s_getProName(int);' % name)
	cb.utils.writeline(fp, 'const char *%s_getProDesc(int);' % name)
	cb.utils.writeline(fp, '')
	cb.utils.writeline(fp, 'int %s_getExtNr(int);' % name)
	cb.utils.writeline(fp, 'const char *%s_getExtName(int, int);' % name)
	cb.utils.writeline(fp, 'const char *%s_getExtDesc(int, int);' % name)
	cb.utils.writeline(fp, '')
	cb.utils.writeline(fp, 'int %s_getMetNr(int, int);' % name)
	cb.utils.writeline(fp, 'const char *%s_getMetName(int, int, int);' % name)
	cb.utils.writeline(fp, 'const char *%s_getMetDesc(int, int, int);' % name)

	cb.utils.writeline(fp, '')

	generate_comment(ctx, fp, 'HIGH LEVEL METHODS')

	cb.utils.writeline(fp, '%s_t *%s_getInterface(%s_profiles_t);' % (name, name, name))
	cb.utils.writeline(fp, '')
	cb.utils.writeline(fp, 'bool %s_checkExt(%s_profiles_t, %s_extentions_t);' % (name, name, name))
	cb.utils.writeline(fp, 'const char *%s_getExtName(%s_profiles_t, %s_extentions_t);' % (name, name, name))
	cb.utils.writeline(fp, 'const char *%s_getExtDesc(%s_profiles_t, %s_extentions_t);' % (name, name, name))
	cb.utils.writeline(fp, '')
	cb.utils.writeline(fp, 'bool %s_checkMet(%s_profiles_t, %s_methods_t);' % (name, name, name))
	cb.utils.writeline(fp, 'const char *%s_getMetName(%s_profiles_t, %s_methods_t);' % (name, name, name))
	cb.utils.writeline(fp, 'const char *%s_getMetDesc(%s_profiles_t, %s_methods_t);' % (name, name, name))

	cb.utils.writeline(fp, '')

#############################################################################

def generate_prototype1(ctx, fp, m, prefix = None, suffix = None):

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

	cb.utils.writeline(fp, proto[: -1] + ');')

#############################################################################

def generate_prototype2(ctx, fp, m, prefix = None, suffix = None):

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

	cb.utils.writeline(fp, proto[: -1] + ');')

#############################################################################


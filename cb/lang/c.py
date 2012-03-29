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

import re, cb.utils

#############################################################################

HAS_HEADERS = True

#############################################################################

INT_EXT = 'h'
IMP_EXT = 'c'

#############################################################################

PRIMITIVES = set([
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
	'char',
	'short',
	'int',
	'long',
	'float',
	'double',
	'...'
])

#############################################################################

QUALIFIERS = set([
	'const',
	'register',
	'volatile',
	'struct',
	'enum',
])

#############################################################################
# COMMENTS								    #
#############################################################################

def emit_separator(ctx, fp):
	cb.utils.printf(fp, '/*-------------------------------------------------------------------------*/')
	cb.utils.printf(fp, '')

#############################################################################

def emit_COMMENT(ctx, fp, s):
	cb.utils.printf(fp, '/*-------------------------------------------------------------------------*/')
	cb.utils.printf(fp, '/* %s%s   */' % (s, ''.join([' ' for i in xrange(69 - len(s))])))
	cb.utils.printf(fp, '/*-------------------------------------------------------------------------*/')
	cb.utils.printf(fp, '')

#############################################################################

def emit_comment(ctx, fp, s):
	n = 5
	l = len(s)

	if l > 5:
		n -= 1
		l -= 5

	cb.utils.printf(fp, '/*----------------------------------*/')
	cb.utils.printf(fp, '/* %s%s   */' % (s, ''.join([' ' for i in xrange(30 - len(s))])))
	cb.utils.printf(fp, '/*----------------------------------*/')
	cb.utils.printf(fp, '')

#############################################################################
# PROLOGS								    #
#############################################################################

def emit_extras(extras, fp):

	for e in extras:

		for c in e:

			for t in c['txts']:
				cb.utils.printf(fp, t)

	cb.utils.printf(fp, '')

#############################################################################

def emit_intPubProlog(ctx, fp):
	INT_ASSET = ctx.int_pub_asset

	cb.utils.printf(fp, '/* Authors : %s' % INT_ASSET['authors'])
	cb.utils.printf(fp, ' * Emails  : %s' % INT_ASSET['emails'])
	cb.utils.printf(fp, ' *')
	cb.utils.printf(fp, ' * Version : %d.%d (%s)' % (ctx.major, ctx.minor, INT_ASSET['date']))
	cb.utils.printf(fp, ' *')
	cb.utils.printf(fp, ' * %s' % INT_ASSET['description'])	
	cb.utils.printf(fp, ' */')
	cb.utils.printf(fp, '')

	emit_separator(ctx, fp)

	cb.utils.printf(fp, '#ifndef __%s_H' % ctx.name.upper())
	cb.utils.printf(fp, '#define __%s_H' % ctx.name.upper())
	cb.utils.printf(fp, '')

	emit_separator(ctx, fp)

	cb.utils.printf(fp, '#include <stddef.h>')
	cb.utils.printf(fp, '#include <stdint.h>')
	cb.utils.printf(fp, '#include <stdbool.h>')
	cb.utils.printf(fp, '')

	if len(ctx.int_pub_prologs) > 0:
		emit_separator(ctx, fp)

		emit_extras(ctx.int_pub_prologs, fp)

#############################################################################

def emit_intPrivProlog(ctx, fp):
	INT_ASSET = ctx.int_pub_asset

	cb.utils.printf(fp, '/* Authors : %s' % INT_ASSET['authors'])
	cb.utils.printf(fp, ' * Emails  : %s' % INT_ASSET['emails'])
	cb.utils.printf(fp, ' *')
	cb.utils.printf(fp, ' * Version : %d.%d (%s)' % (ctx.major, ctx.minor, INT_ASSET['date']))
	cb.utils.printf(fp, ' *')
	cb.utils.printf(fp, ' * %s' % INT_ASSET['description'])	
	cb.utils.printf(fp, ' */')
	cb.utils.printf(fp, '')

	emit_separator(ctx, fp)

	cb.utils.printf(fp, '#ifndef __%s_INTERNAL_H' % ctx.name.upper())
	cb.utils.printf(fp, '#define __%s_INTERNAL_H' % ctx.name.upper())
	cb.utils.printf(fp, '')

	emit_separator(ctx, fp)

	cb.utils.printf(fp, '#include "%s.h"' % ctx.name)
	cb.utils.printf(fp, '')

	if len(ctx.int_priv_prologs) > 0:
		emit_separator(ctx, fp)

		emit_extras(ctx.int_priv_prologs, fp)

#############################################################################

def emit_impProlog(ctx, fp):
	INT_ASSET = ctx.int_pub_asset

	cb.utils.printf(fp, '/* Authors : %s' % INT_ASSET['authors'])
	cb.utils.printf(fp, ' * Emails  : %s' % INT_ASSET['emails'])
	cb.utils.printf(fp, ' *')
	cb.utils.printf(fp, ' * Version : %d.%d (%s)' % (ctx.major, ctx.minor, INT_ASSET['date']))
	cb.utils.printf(fp, ' *')
	cb.utils.printf(fp, ' * %s' % INT_ASSET['description'])	
	cb.utils.printf(fp, ' */')
	cb.utils.printf(fp, '')

	emit_separator(ctx, fp)

	cb.utils.printf(fp, '#include <string.h>')
	cb.utils.printf(fp, '')
	cb.utils.printf(fp, '#include "%s_internal.h"' % ctx.name)
	cb.utils.printf(fp, '')

	if len(ctx.imp_extras) > 0:
		emit_separator(ctx, fp)

		emit_extras(ctx.imp_extras, fp)

#############################################################################

def emit_impProfileProlog(ctx, fp, p):
	INT_ASSET = ctx.int_pub_asset
	IMP_PROFILES = ctx.imp_profiles[p]
	IMP_EXTENSIONS = ctx.imp_profiles[p]['extensions']

	cb.utils.printf(fp, '/* Authors : %s' % INT_ASSET['authors'])
	cb.utils.printf(fp, ' * Emails  : %s' % INT_ASSET['emails'])
	cb.utils.printf(fp, ' *')
	cb.utils.printf(fp, ' * Version : %d.%d (%s)' % (ctx.major, ctx.minor, INT_ASSET['date']))
	cb.utils.printf(fp, ' *')
	cb.utils.printf(fp, ' * %s' % INT_ASSET['description'])	
	cb.utils.printf(fp, ' */')
	cb.utils.printf(fp, '')

	emit_separator(ctx, fp)

	cb.utils.printf(fp, '#include <stdlib.h>')
	cb.utils.printf(fp, '#include <string.h>')
	cb.utils.printf(fp, '')
	cb.utils.printf(fp, '#include "%s_internal.h"' % ctx.name)
	cb.utils.printf(fp, '')

	if len(IMP_PROFILES['extras']) > 0:
		emit_separator(ctx, fp)

		emit_extras(IMP_PROFILES['extras'], fp)

	for e in IMP_EXTENSIONS:

		if len(IMP_EXTENSIONS[e]['extras']) > 0:
			emit_separator(ctx, fp)

			emit_extras(IMP_EXTENSIONS[e]['extras'], fp)

#############################################################################
# EPILOGS								    #
#############################################################################

def emit_intPubEpilog(ctx, fp):

	if len(ctx.int_pub_epilogs) > 0:
		emit_extras(ctx.int_pub_epilogs, fp)

		emit_separator(ctx, fp)

	cb.utils.printf(fp, '#endif /* __%s_H */' % ctx.name.upper())
	cb.utils.printf(fp, '')

	emit_separator(ctx, fp)

#############################################################################

def emit_intPrivEpilog(ctx, fp):

	if len(ctx.int_priv_epilogs) > 0:
		emit_extras(ctx.int_priv_epilogs, fp)

		emit_separator(ctx, fp)

	cb.utils.printf(fp, '#endif /* __%s_INTERNAL_H */' % ctx.name.upper())
	cb.utils.printf(fp, '')

	emit_separator(ctx, fp)

#############################################################################
# UTILS
#############################################################################

def emit_pointerPrototype(ctx, fp, comma, m, prefix = '', suffix = ''):

	proto = '%s (* %s%s%s)(' % (m['type'], prefix, m['name'], suffix)

	if len(m['params']) > 0:

		i = 0

		for p in m['params']:

			if i > 0:
				proto += ', '

			if len(p['name']) == 0:
				proto += '%s' % (p['type'])
			else:
				if p['type'].find('*') >= 0:
					proto += '%s%s' % (p['type'], p['name'])
				else:
					proto += '%s %s' % (p['type'], p['name'])
			i += 1
	else:
		proto += 'void'

	if comma == False:
		cb.utils.printf(fp, proto + ')')
	else:
		cb.utils.printf(fp, proto + ');')

#############################################################################

def emit_functionPrototype(ctx, fp, comma, m, prefix = '', suffix = ''):

	proto = '%s %s%s%s(' % (m['type'], prefix, m['name'], suffix)

	if len(m['params']) > 0:

		i = 0

		for p in m['params']:

			if i > 0:
				proto += ', '

			if len(p['name']) == 0:
				proto += '%s' % (p['type'])
			else:
				if p['type'].find('*') >= 0:
					proto += '%s%s' % (p['type'], p['name'])
				else:
					proto += '%s %s' % (p['type'], p['name'])
			i += 1
	else:
		proto += 'void'

	if comma == False:
		cb.utils.printf(fp, proto + ')')
	else:
		cb.utils.printf(fp, proto + ');')

#############################################################################

def emit_ctorPrototype(ctx, fp, comma, p, name):

	proto = 'bool %s(struct %s_s *self' % (name, ctx.name)

	for cp in p['params']:

		proto += ', '

		if len(cp['name']) == 0:
			proto += '%s' % (cp['type'])
		else:
			if cp['type'].find('*') >= 0:
				proto += '%s%s' % (cp['type'], cp['name'])
			else:
				proto += '%s %s' % (cp['type'], cp['name'])

	if comma == False:
		cb.utils.printf(fp, proto + ')')
	else:
		cb.utils.printf(fp, proto + ');')

#############################################################################

def emit_dtorPrototype(ctx, fp, comma, p, name):

	proto = 'bool %s(struct %s_s *self' % (name, ctx.name)

	if comma == False:
		cb.utils.printf(fp, proto + ')')
	else:
		cb.utils.printf(fp, proto + ');')

#############################################################################

def emit_ctorCall(ctx, fp, p, name):

	proto = '%s(self' % name

	for cp in p['params']:

		proto += ', %s' % cp['name']

	cb.utils.writef(fp, proto + ')')

#############################################################################

def emit_dtorCall(ctx, fp, p, name):

	proto = '%s(self' % name

	cb.utils.writef(fp, proto + ')')

#############################################################################
# PUBLIC & PRIVATE INTERFACE						    #
#############################################################################

def emit_impTypes(types, fp):

	for t in types:

		#############################################################

		if t['class'] == 'base':

			re1 = re.compile('\(\s*\*\s*\)')
			re2 = re.compile('\[([^\]]*)\]')

			if   re1.search(t['from']):
				cb.utils.printf(fp, 'typedef %s;' % (
					re1.sub('(* %s)' % t['name'], t['from'])
				))

			elif re2.search(t['from']):
				if re2.sub('', t['from']).find('*') >= 0:
					cb.utils.printf(fp, 'typedef %s%s%s;' % (
						re2.sub('', t['from']), t['name'],
						''.join(['[%s]' % dim.strip() for dim in re2.findall(t['from'])])
					))
				else:
					cb.utils.printf(fp, 'typedef %s %s%s;' % (
						re2.sub('', t['from']), t['name'],
						''.join(['[%s]' % dim.strip() for dim in re2.findall(t['from'])])
					))
			else:
				if t['from'].find('*') >= 0:
					cb.utils.printf(fp, 'typedef %s%s;' % (t['from'], t['name']))
				else:
					cb.utils.printf(fp, 'typedef %s %s;' % (t['from'], t['name']))

			cb.utils.printf(fp, '')

		#############################################################

		if t['class'] == 'enum':
			cb.utils.printf(fp, 'typedef enum %s' % t['name'])
			cb.utils.printf(fp, '{')

			for v in t['values']:

				if len(v['init']) == 0:
					cb.utils.printf(fp, '\t%s,' % (v['name']))
				else:
					cb.utils.printf(fp, '\t%s = %s,' % (v['name'], v['init']))

			cb.utils.printf(fp, '')
			cb.utils.printf(fp, '} %s;' % t['name'])
			cb.utils.printf(fp, '')

		#############################################################

		if t['class'] == 'struct':
			cb.utils.printf(fp, 'typedef struct %s' % t['name'])
			cb.utils.printf(fp, '{')

			for f in t['fields']:
				cb.utils.printf(fp, '\t%s %s;' % (f['type'], f['name']))

			cb.utils.printf(fp, '')
			cb.utils.printf(fp, '} %s;' % t['name'])
			cb.utils.printf(fp, '')

#############################################################################
# PUBLIC INTERFACE							    #
#############################################################################

def emit_impPubTypes(ctx, fp):
	cb.utils.printf(fp, 'typedef struct %s_s %s_t;' % (ctx.name, ctx.name))
	cb.utils.printf(fp, '')

	emit_separator(ctx, fp)

	emit_impTypes(ctx.int_pub_types, fp)

#############################################################################

def emit_impPubDefinitions(ctx, fp):
	name = ctx.name
	NAME = ctx.name.upper()

	#####################################################################
	# GLOBALS							    #
	#####################################################################

	emit_comment(ctx, fp, 'GLOBAL ENUMS')

	cb.utils.printf(fp, 'typedef enum %s_status_e' % name)
	cb.utils.printf(fp, '{')

	cb.utils.printf(fp, '\t%s_STATUS_DEFINED = 0x%X,' % (NAME, cb.utils.getCnt(ctx)))
	cb.utils.printf(fp, '\t%s_STATUS_INCOMPLETE = 0x%X,' % (NAME, cb.utils.getCnt(ctx)))
	cb.utils.printf(fp, '\t%s_STATUS_UNDEFINED = 0x%X,' % (NAME, cb.utils.getCnt(ctx)))
	cb.utils.printf(fp, '')

	cb.utils.printf(fp, '} %s_status_t;' % name)
	cb.utils.printf(fp, '')

	#####################################################################
	# PROFILES							    #
	#####################################################################

	emit_comment(ctx, fp, 'PROFILE ENUMS')

	cb.utils.printf(fp, 'typedef enum %s_profiles_e' % name)
	cb.utils.printf(fp, '{')

	for p in ctx.int_pub_profiles:
		cb.utils.printf(fp, '\t%s_PROFILE_%s = 0x%X,' % (NAME, p['name'].upper(), cb.utils.getCnt(ctx)))

	cb.utils.printf(fp, '')
	cb.utils.printf(fp, '} %s_profiles_t;' % name)
	cb.utils.printf(fp, '')

	#####################################################################
	# EXTENTIONS							    #
	#####################################################################

	emit_comment(ctx, fp, 'EXTENTION ENUMS')

	cb.utils.printf(fp, 'typedef enum %s_extensions_e' % name)
	cb.utils.printf(fp, '{')

	for e in ctx.int_pub_extensions:
		cb.utils.printf(fp, '\t%s_EXTENSION_%s = 0x%X,' % (NAME, e['name'].upper(), cb.utils.getCnt(ctx)))

	cb.utils.printf(fp, '')
	cb.utils.printf(fp, '} %s_extensions_t;' % name)
	cb.utils.printf(fp, '')

	#####################################################################
	# METHODS							    #
	#####################################################################

	emit_comment(ctx, fp, 'METHOD ENUMS')

	cb.utils.printf(fp, 'typedef enum %s_methods_e' % name)
	cb.utils.printf(fp, '{')

	for e in ctx.int_pub_extensions:

		for m in e['methods']:
			cb.utils.printf(fp, '\t%s_METHOD_%s_%s = 0x%X,' % (NAME, e['name'].upper(), m['name'].upper(), cb.utils.getCnt(ctx)))

	cb.utils.printf(fp, '')
	cb.utils.printf(fp, '} %s_methods_t;' % name)
	cb.utils.printf(fp, '')

	#####################################################################
	# STRUCTURE							    #
	#####################################################################

	emit_comment(ctx, fp, 'STRUCTURE')

	cb.utils.printf(fp, 'struct %s_s' % ctx.name)
	cb.utils.printf(fp, '{')

	if(len(ctx.int_priv_constraints) > 0):
		cb.utils.printf(fp, '\tint constraints[%d];' % len(ctx.int_priv_constraints))
		cb.utils.printf(fp, '')

	for e in ctx.int_pub_extensions:

		cb.utils.printf(fp, '\tstruct {')

		for m in e['methods']:

			cb.utils.writef(fp, '\t\t'),
			emit_pointerPrototype(ctx, fp, True, m, '', '')

		cb.utils.printf(fp, '')
		cb.utils.printf(fp, '\t\tvoid *user;')
		cb.utils.printf(fp, '')
		cb.utils.printf(fp, '\t} %s;\n' % e['name'])

	cb.utils.printf(fp, '\tvoid *user;')

	cb.utils.printf(fp, '};')
	cb.utils.printf(fp, '')

#############################################################################

def emit_impPubMethods(ctx, fp):
	name = ctx.name

	cb.utils.printf(fp, 'int %s_getMajor(void);' % name)
	cb.utils.printf(fp, 'int %s_getMinor(void);' % name)
	cb.utils.printf(fp, '')

	for p in ctx.int_pub_profiles:
		emit_ctorPrototype(ctx, fp, True, p, '%s_%s_initialize' % (name, p['name']))
		emit_dtorPrototype(ctx, fp, True, p, '%s_%s_finalize' % (name, p['name']))

	cb.utils.printf(fp, '')

	cb.utils.printf(fp, 'enum %s_status_e %s_checkExtension(struct %s_s *, %s_extensions_t);' % (name, name, name, name))
	cb.utils.printf(fp, 'const char *%s_getExtName(struct %s_s *, %s_extensions_t);' % (name, name, name))
	cb.utils.printf(fp, 'const char *%s_getExtDesc(struct %s_s *, %s_extensions_t);' % (name, name, name))
	cb.utils.printf(fp, '')

	cb.utils.printf(fp, 'enum %s_status_e %s_checkMethod(struct %s_s *, %s_methods_t);' % (name, name, name, name))
	cb.utils.printf(fp, 'const char *%s_getMetName(struct %s_s *, %s_methods_t);' % (name, name, name))
	cb.utils.printf(fp, 'const char *%s_getMetDesc(struct %s_s *, %s_methods_t);' % (name, name, name))
	cb.utils.printf(fp, '')

#############################################################################
# PRIVATE INTERFACE							    #
#############################################################################

def emit_impPrivTypes(ctx, fp):
	emit_impTypes(ctx.int_priv_types, fp)

#############################################################################

def emit_impPrivProfiles(ctx, fp):

	for p in ctx.int_pub_profiles:
		cb.utils.printf(fp, '#define __IS_DEFINED_PROFILE_%s' % p['name'].upper())

	cb.utils.printf(fp, '')

#############################################################################

def emit_impPrivConstraints(ctx, fp):

	i = 0

	for c in ctx.int_priv_constraints:
		cb.utils.printf(fp, 'typedef enum %s_s' % c['name'])
		cb.utils.printf(fp, '{')

		for k in c['keys']:
			cb.utils.printf(fp, '\t%s,' % k['name'].upper())

		cb.utils.printf(fp, '')
		cb.utils.printf(fp, '} %s_t;' % c['name'])
		cb.utils.printf(fp, '')

		cb.utils.printf(fp, '#define %s(self) ((enum %s_s *) ((self)->constraints + %d))[0]' % (c['name'].upper(), c['name'], i))
		cb.utils.printf(fp, '')

		i += 1

#############################################################################

def emit_impPrivMethods(ctx, fp):

	cb.utils.printf(fp, 'bool __%s_ctor(struct %s_s *);' % (ctx.name, ctx.name))
	cb.utils.printf(fp, 'bool __%s_dtor(struct %s_s *);' % (ctx.name, ctx.name))
	cb.utils.printf(fp, '')

#############################################################################
# GLOBAL IMPLEMENTATION							    #
#############################################################################

def emit_impCtor(ctx, fp):

	i = 0

	for ctor in ctx.imp_ctors:

		for code in ctor:

			cb.utils.printf(fp, 'static bool __%s_ctor%d(%s_t *self)' % (ctx.name, i, ctx.name))
			cb.utils.printf(fp, '{')
			for t in code['txts']: cb.utils.printf(fp, '%s' % t)
			cb.utils.printf(fp, '}')
			cb.utils.printf(fp, '')

			emit_separator(ctx, fp)

			i += 1

	##

	i = 0

	cb.utils.printf(fp, 'bool __%s_ctor(%s_t *self)' % (ctx.name, ctx.name))
	cb.utils.printf(fp, '{')

	cb.utils.printf(fp, '\tmemset(self, 0x00, sizeof(%s_t));' % ctx.name)
	cb.utils.printf(fp, '')

	cb.utils.printf(fp, '\tbool result;')
	cb.utils.printf(fp, '')

	for ctor in ctx.imp_ctors:

		for code in ctor:

			if len(code['condition']) == 0:
				cb.utils.printf(fp, '\tif(1)')
			else:
				cb.utils.printf(fp, '\tif(%s)' % code['condition'])

			cb.utils.printf(fp, '\t{')
			for t in code['txts']: cb.utils.printf(fp, '\t\tresult = __%s_ctor%d(self);' % (ctx.name, i))
			cb.utils.printf(fp, '\t\tgoto __next;')
			cb.utils.printf(fp, '\t}')
			cb.utils.printf(fp, '')

			i += 1

	if i == 0:
		cb.utils.printf(fp, '\tresult = true;')
		cb.utils.printf(fp, '')
	else:
		cb.utils.printf(fp, '\tresult = false;')
		cb.utils.printf(fp, '')
		cb.utils.printf(fp, '__next:')

	##

	cb.utils.printf(fp, '\treturn result;')

	cb.utils.printf(fp, '}')
	cb.utils.printf(fp, '')

#############################################################################

def emit_impDtor(ctx, fp):

	i = 0

	for dtor in ctx.imp_dtors:

		for code in dtor:
			cb.utils.printf(fp, 'static bool __%s_dtor%d(%s_t *self)' % (ctx.name, i, ctx.name))
			cb.utils.printf(fp, '{')
			for t in code['txts']: cb.utils.printf(fp, '%s' % t)
			cb.utils.printf(fp, '}')
			cb.utils.printf(fp, '')

			emit_separator(ctx, fp)

			i += 1

	##

	i = 0

	cb.utils.printf(fp, 'bool __%s_dtor(%s_t *self)' % (ctx.name, ctx.name))
	cb.utils.printf(fp, '{')

	cb.utils.printf(fp, '\tbool result;')
	cb.utils.printf(fp, '')

	for dtor in ctx.imp_dtors:

		for code in dtor:

			if len(code['condition']) == 0:
				cb.utils.printf(fp, '\tif(1)')
			else:
				cb.utils.printf(fp, '\tif(%s)' % code['condition'])

			cb.utils.printf(fp, '\t{')
			for t in code['txts']: cb.utils.printf(fp, '\t\tresult = __%s_dtor%d(self);' % (ctx.name, i))
			cb.utils.printf(fp, '\t\tgoto __next;')
			cb.utils.printf(fp, '\t}')
			cb.utils.printf(fp, '')

			i += 1

	if i == 0:
		cb.utils.printf(fp, '\tresult = true;')
		cb.utils.printf(fp, '')
	else:
		cb.utils.printf(fp, '\tresult = false;')
		cb.utils.printf(fp, '')
		cb.utils.printf(fp, '__next:')

	##

	cb.utils.printf(fp, '\treturn result;')

	cb.utils.printf(fp, '}')
	cb.utils.printf(fp, '')

#############################################################################

def emit_impMethods(ctx, fp):

	name = ctx.name
	NAME = ctx.name.upper()

	#####################################################################

	cb.utils.printf(fp, 'int %s_getMajor(void)' % name)
	cb.utils.printf(fp, '{')
	cb.utils.printf(fp, '\treturn %d;' % ctx.major)
	cb.utils.printf(fp, '}')
	cb.utils.printf(fp, '')

	#####################################################################

	emit_separator(ctx, fp)

	#####################################################################

	cb.utils.printf(fp, 'int %s_getMinor(void)' % name)
	cb.utils.printf(fp, '{')
	cb.utils.printf(fp, '\treturn %d;' % ctx.minor)
	cb.utils.printf(fp, '}')
	cb.utils.printf(fp, '')

	#####################################################################

	emit_separator(ctx, fp)

	#####################################################################

	cb.utils.printf(fp, '%s_status_t %s_checkExtension(%s_t *__interface, %s_extensions_t extension)' % (name, name, name, name))
	cb.utils.printf(fp, '{')

	cb.utils.printf(fp, '\tint met_nr = 0;')
	cb.utils.printf(fp, '\tint met_cnt = 0;')
	cb.utils.printf(fp, '')

	cb.utils.printf(fp, '\t%s_status_t result;' % name)
	cb.utils.printf(fp, '')

	cb.utils.printf(fp, '\tswitch(extension)')
	cb.utils.printf(fp, '\t{')

	for e in ctx.int_pub_extensions:
		cb.utils.printf(fp, '\t\tcase %s_EXTENSION_%s:' % (name.upper(), e['name'].upper()))

		cb.utils.printf(fp, '\t\t\tmet_nr = %d;' % len(e['methods']))
		cb.utils.printf(fp, '')

		for m in e['methods']:
			cb.utils.printf(fp, '\t\t\tif(__interface->%s.%s != NULL) {' % (e['name'], m['name']))
			cb.utils.printf(fp, '\t\t\t\tmet_cnt++;')
			cb.utils.printf(fp, '\t\t\t}')

		cb.utils.printf(fp, '')
		cb.utils.printf(fp, '\t\t\tbreak;')
		cb.utils.printf(fp, '')

	cb.utils.printf(fp, '\t\tdefault:')
	cb.utils.printf(fp, '\t\t\tbreak;')

	cb.utils.printf(fp, '\t}')		
	cb.utils.printf(fp, '')

	cb.utils.printf(fp, '\t/**/ if(met_cnt == 0x0000) {')
	cb.utils.printf(fp, '\t\tresult = %s_STATUS_UNDEFINED;' % NAME)
	cb.utils.printf(fp, '\t}')
	cb.utils.printf(fp, '\telse if(met_cnt == met_nr) {')
	cb.utils.printf(fp, '\t\tresult = %s_STATUS_DEFINED;' % NAME)
	cb.utils.printf(fp, '\t}')
	cb.utils.printf(fp, '\telse {')
	cb.utils.printf(fp, '\t\tresult = %s_STATUS_INCOMPLETE;' % NAME)
	cb.utils.printf(fp, '\t}')
	cb.utils.printf(fp, '')

	cb.utils.printf(fp, '\treturn result;')

	cb.utils.printf(fp, '}')
	cb.utils.printf(fp, '')

	#####################################################################

	emit_separator(ctx, fp)

	#####################################################################

	cb.utils.printf(fp, 'enum %s_status_e %s_checkMethod(%s_t *__interface, %s_methods_t method)' % (name, name, name, name))
	cb.utils.printf(fp, '{')

	cb.utils.printf(fp, '\tbool result;')
	cb.utils.printf(fp, '')

	cb.utils.printf(fp, '\tswitch(method)')
	cb.utils.printf(fp, '\t{')

	for e in ctx.int_pub_extensions:

		for m in e['methods']:
			cb.utils.printf(fp, '\t\tcase %s_METHOD_%s_%s:' % (name.upper(), e['name'].upper(), m['name'].upper()))
			cb.utils.printf(fp, '\t\t\tresult = (__interface->%s.%s != NULL) ? %s_STATUS_DEFINED : %s_STATUS_UNDEFINED;' % (e['name'], m['name'], NAME, NAME))
			cb.utils.printf(fp, '\t\t\tbreak;')
			cb.utils.printf(fp, '')

	cb.utils.printf(fp, '\t\tdefault:')
	cb.utils.printf(fp, '\t\t\tresult = %s_STATUS_UNDEFINED;' % NAME)
	cb.utils.printf(fp, '\t\t\tbreak;')

	cb.utils.printf(fp, '\t}')		
	cb.utils.printf(fp, '')

	#####################################################################

	cb.utils.printf(fp, '\treturn result;')

	cb.utils.printf(fp, '}')
	cb.utils.printf(fp, '')

#############################################################################
# PROFILE IMPLEMENTATION						    #
#############################################################################

def emit_impProfileMethods(ctx, fp, p):
	IMP_PROFILES = ctx.imp_profiles

	##

	IMP_EXTENSIONS = IMP_PROFILES[p]['extensions']
	for e in IMP_EXTENSIONS:
		ext = cb.utils.int_getExtension(ctx, e)

		IMP_METHODS = IMP_EXTENSIONS[e]['methods']
		for m in IMP_METHODS:
			met = cb.utils.int_getMethod(ext, m)

			i = 0

			for c in IMP_METHODS[m]:

				emit_functionPrototype(ctx, fp, False, met, '__%s_%s_' % (p, e), '%d' % i)
  				cb.utils.printf(fp, '{')
				for t in c['txts']: cb.utils.printf(fp, t)
 				cb.utils.printf(fp, '}')
				cb.utils.printf(fp, '')

				emit_separator(ctx, fp)

				i += 1

#############################################################################

def emit_impProfileCtor(ctx, fp, p):
	pro = cb.utils.int_getProfile(ctx, p)
	IMP_PROFILES = ctx.imp_profiles[p]

	#####################################################################
	# PROFILE CTORS							    #
	#####################################################################

	i = 0

	for ctor in IMP_PROFILES['ctors']:

		for code in ctor:
			emit_ctorPrototype(ctx, fp, False, pro, '__%s_%s_ctor%d' % (ctx.name, p, i))
			cb.utils.printf(fp, '{')
			for t in code['txts']: cb.utils.printf(fp, '%s' % t)
			cb.utils.printf(fp, '}')
			cb.utils.printf(fp, '')

			emit_separator(ctx, fp)

			i += 1

	#####################################################################
	# EXTENSION CTORS						    #
	#####################################################################

	extCtorNr = 0

	for e in ctx.int_pub_extensions:

		if ctx.imp_profiles[p]['extensions'].has_key(e['name']) != False:

			emit_impExtensionXtor(ctx, fp, True, p, e['name'])

			emit_separator(ctx, fp)

			extCtorNr += 1

	#####################################################################
	# PROFILE CTOR							    #
	#####################################################################

	emit_ctorPrototype(ctx, fp, False, pro, '%s_%s_initialize' % (ctx.name, p))
	cb.utils.printf(fp, '{')

	#####################################################################

	cb.utils.printf(fp, '\tif(__%s_ctor(self) == false)' % ctx.name)
	cb.utils.printf(fp, '\t{')
	cb.utils.printf(fp, '\t\treturn false;')
	cb.utils.printf(fp, '\t}')
	cb.utils.printf(fp, '')

	cb.utils.printf(fp, '\tbool result;')
	cb.utils.printf(fp, '')

	#################################
	# PROFILE CTORS			#
	#################################

	i = 0

	for ctor in IMP_PROFILES['ctors']:

		for code in ctor:

			if len(code['condition']) == 0:
				cb.utils.printf(fp, '\tif(1)')
				cb.utils.printf(fp, '\t{')
				cb.utils.writef(fp, '\t\tresult = ') ; emit_ctorCall(ctx, fp, pro, '__%s_%s_ctor%d' % (ctx.name, p, i)) ; cb.utils.printf(fp, ';')
				cb.utils.printf(fp, '\t\tgoto __next;')
				cb.utils.printf(fp, '\t}')
				cb.utils.printf(fp, '')
			else:
				cb.utils.printf(fp, '\tif(%s)' % code['condition'])
				cb.utils.printf(fp, '\t{')
				cb.utils.writef(fp, '\t\tresult = ') ; emit_ctorCall(ctx, fp, pro, '__%s_%s_ctor%d' % (ctx.name, p, i)) ; cb.utils.printf(fp, ';')
				cb.utils.printf(fp, '\t\tgoto __next;')
				cb.utils.printf(fp, '\t}')
				cb.utils.printf(fp, '')

			i += 1

	if i == 0:
		cb.utils.printf(fp, '\tresult = true;')
		cb.utils.printf(fp, '')
	else:
		cb.utils.printf(fp, '\tresult = false;')
		cb.utils.printf(fp, '')
		cb.utils.printf(fp, '__next:')

	#################################
	# EXTENSION CTORS		#
	#################################

	if extCtorNr > 0:
		cb.utils.printf(fp, '\tresult = result \\')

		for e in ctx.int_pub_extensions:

			if ctx.imp_profiles[p]['extensions'].has_key(e['name']) != False:

				cb.utils.writef(fp, '\t\t && ') ; emit_ctorCall(ctx, fp, pro, '__%s_%s_%s_ctor' % (ctx.name, p, e['name'])) ; cb.utils.printf(fp, '')

		cb.utils.printf(fp, '\t;')
		cb.utils.printf(fp, '')

	cb.utils.printf(fp, '\tif(result == false)')
	cb.utils.printf(fp, '\t{')
	cb.utils.writef(fp, '\t\t') ; emit_dtorCall(ctx, fp, pro, '%s_%s_finalize' % (ctx.name, p)) ; cb.utils.printf(fp, ';')
	cb.utils.printf(fp, '\t}')
	cb.utils.printf(fp, '')

	#####################################################################

	cb.utils.printf(fp, '\treturn result;')

	cb.utils.printf(fp, '}')
	cb.utils.printf(fp, '')

#############################################################################

def emit_impProfileDtor(ctx, fp, p):
	pro = cb.utils.int_getProfile(ctx, p)
	IMP_PROFILES = ctx.imp_profiles[p]

	#####################################################################
	# PROFILE DTORS							    #
	#####################################################################

	i = 0

	for dtor in IMP_PROFILES['dtors']:

		for code in dtor:
			emit_dtorPrototype(ctx, fp, False, pro, '__%s_%s_dtor%d' % (ctx.name, p, i))
			cb.utils.printf(fp, '{')
			for t in code['txts']: cb.utils.printf(fp, '%s' % t)
			cb.utils.printf(fp, '}')
			cb.utils.printf(fp, '')

			emit_separator(ctx, fp)

			i += 1

	#####################################################################
	# EXTENSION DTORS						    #
	#####################################################################

	extDtorNr = 0

	for e in reversed(ctx.int_pub_extensions):

		if ctx.imp_profiles[p]['extensions'].has_key(e['name']) != False:

			emit_impExtensionXtor(ctx, fp, False, p, e['name'])

			emit_separator(ctx, fp)

			extDtorNr += 1

	#####################################################################
	# PROFILE DTOR							    #
	#####################################################################

	emit_dtorPrototype(ctx, fp, False, pro, '%s_%s_finalize' % (ctx.name, p))
	cb.utils.printf(fp, '{')

	cb.utils.printf(fp, '\tbool result = true;')
	cb.utils.printf(fp, '')

	#################################
	# EXTENSION DTORS		#
	#################################

	if extDtorNr > 0:

		for e in reversed(ctx.int_pub_extensions):

			if ctx.imp_profiles[p]['extensions'].has_key(e['name']) != False:

				cb.utils.writef(fp, '\tif(') ; emit_dtorCall(ctx, fp, pro, '__%s_%s_%s_dtor' % (ctx.name, p, e['name'])) ; cb.utils.printf(fp, ' == false) {')
				cb.utils.printf(fp, '\t\tresult = false;')
				cb.utils.printf(fp, '\t}')

		cb.utils.printf(fp, '')

	#################################
	# PROFILE DTORS			#
	#################################

	i = 0

	for ctor in IMP_PROFILES['dtors']:

		for code in ctor:

			if len(code['condition']) == 0:
				cb.utils.printf(fp, '\tif(1)')
				cb.utils.printf(fp, '\t{')
				cb.utils.writef(fp, '\t\tif(') ; emit_dtorCall(ctx, fp, pro, '__%s_%s_dtor%d' % (ctx.name, p, i)) ; cb.utils.printf(fp, ' == false) {')
				cb.utils.printf(fp, '\t\t\tresult = false;')
				cb.utils.printf(fp, '\t\t}')
				cb.utils.printf(fp, '\t\tgoto __next;')
				cb.utils.printf(fp, '\t}')
				cb.utils.printf(fp, '')
			else:
				cb.utils.printf(fp, '\tif(%s)' % code['condition'])
				cb.utils.printf(fp, '\t{')
				cb.utils.writef(fp, '\t\tif(') ; emit_dtorCall(ctx, fp, pro, '__%s_%s_dtor%d' % (ctx.name, p, i)) ; cb.utils.printf(fp, ' == false) {')
				cb.utils.printf(fp, '\t\t\tresult = false;')
				cb.utils.printf(fp, '\t\t}')
				cb.utils.printf(fp, '\t\tgoto __next;')
				cb.utils.printf(fp, '\t}')
				cb.utils.printf(fp, '')

			i += 1

	if i == 0:
		cb.utils.printf(fp, '\tresult = true;')
		cb.utils.printf(fp, '')
	else:
		cb.utils.printf(fp, '\tresult = false;')
		cb.utils.printf(fp, '')
		cb.utils.printf(fp, '__next:')

	#####################################################################

	cb.utils.printf(fp, '\tif(__%s_dtor(self) == false) {' % ctx.name)
	cb.utils.printf(fp, '\t\tresult = false;')
	cb.utils.printf(fp, '\t}')
	cb.utils.printf(fp, '')

	#####################################################################

	cb.utils.printf(fp, '\treturn result;')

	cb.utils.printf(fp, '}')
	cb.utils.printf(fp, '')

#############################################################################

def emit_impExtensionXtor(ctx, fp, isCtor, p, e):
	pro = cb.utils.int_getProfile(ctx, p)
	ext = ctx.imp_profiles[p]['extensions'][e]

	if isCtor != False:
		emit_xtorPrototype = emit_ctorPrototype
		emit_xtorCall = emit_ctorCall
		XTORS = ext['ctors']
		yuio = 'ctor'
	else:
		emit_xtorPrototype = emit_dtorPrototype
		emit_xtorCall = emit_dtorCall
		XTORS = ext['dtors']
		yuio = 'dtor'

	#####################################################################
	# EXTENSION XTORS						    #
	#####################################################################

	i = 0

	for xtor in XTORS:

		for code in xtor:
			emit_xtorPrototype(ctx, fp, False, pro, '__%s_%s_%s_%s%d' % (ctx.name, p, e, yuio, i))
			cb.utils.printf(fp, '{')
			for t in code['txts']: cb.utils.printf(fp, '%s' % t)
			cb.utils.printf(fp, '}')
			cb.utils.printf(fp, '')

			emit_separator(ctx, fp)

			i += 1

	#####################################################################
	# EXTENSION CTOR						    #
	#####################################################################

	emit_xtorPrototype(ctx, fp, False, pro, '__%s_%s_%s_%s' % (ctx.name, p, e, yuio))
	cb.utils.printf(fp, '{')

	cb.utils.printf(fp, '\tbool result;')
	cb.utils.printf(fp, '')

	#################################
	# EXTENSION CTORS		#
	#################################

	i = 0

	for ctor in XTORS:

		for code in ctor:

			if len(code['condition']) == 0:
				cb.utils.printf(fp, '\tif(1)')
				cb.utils.printf(fp, '\t{')
				cb.utils.writef(fp, '\t\tresult = ') ; emit_xtorCall(ctx, fp, pro, '__%s_%s_%s_%s%d' % (ctx.name, p, e, yuio, i)) ; cb.utils.printf(fp, ';')
				cb.utils.printf(fp, '\t\tgoto __next;')
				cb.utils.printf(fp, '\t}')
				cb.utils.printf(fp, '')
			else:
				cb.utils.printf(fp, '\tif(%s)' % code['condition'])
				cb.utils.printf(fp, '\t{')
				cb.utils.writef(fp, '\t\tresult = ') ; emit_xtorCall(ctx, fp, pro, '__%s_%s_%s_%s%d' % (ctx.name, p, e, yuio, i)) ; cb.utils.printf(fp, ';')
				cb.utils.printf(fp, '\t\tgoto __next;')
				cb.utils.printf(fp, '\t}')
				cb.utils.printf(fp, '')

			i += 1

	if i == 0:
		cb.utils.printf(fp, '\tresult = true;')
		cb.utils.printf(fp, '')
	else:
		cb.utils.printf(fp, '\tresult = false;')
		cb.utils.printf(fp, '')
		cb.utils.printf(fp, '__next:')

	#################################
	# EXTENSION METHODS		#
	#################################

	if isCtor != False:
		#################################
		# INITIALIZE			#
		#################################

		for m in ext['methods']:
			#################################
			# UNCONDITIONAL CODES		#
			#################################

			j = 0

			for (i, c) in enumerate(ext['methods'][m]):

				condition = c['condition']

				if len(condition) == 0:

					if j == 0:
						cb.utils.printf(fp, '\t/**/ if(1)')
					else:
						cb.utils.printf(fp, '\t/**/ if(1)')

					cb.utils.printf(fp, '\t{')
					cb.utils.printf(fp, '\t\tself->%s.%s = __%s_%s_%s%d;' % (e, m, p, e, m, i))
					cb.utils.printf(fp, '\t}')

					j += 1

			#################################
			# CONDITIONAL CODES		#
			#################################

			j = 0

			for (i, c) in enumerate(ext['methods'][m]):

				condition = c['condition']

				if len(condition) != 0:

					if j == 0:
						cb.utils.printf(fp, '\t/**/ if(%s)' % condition)
					else:
						cb.utils.printf(fp, '\telse if(%s)' % condition)

					cb.utils.printf(fp, '\t{')
					cb.utils.printf(fp, '\t\tself->%s.%s = __%s_%s_%s%d;' % (e, m, p, e, m, i))
					cb.utils.printf(fp, '\t}')

					j += 1

	else:
		#################################
		# FINALIZE			#
		#################################

		for m in ext['methods']:
			cb.utils.printf(fp, '\tself->%s.%s = NULL;' % (e, m))

	cb.utils.printf(fp, '')

	#####################################################################

	cb.utils.printf(fp, '\treturn result;')

	cb.utils.printf(fp, '}')
	cb.utils.printf(fp, '')

#############################################################################


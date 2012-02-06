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
	'char',
	'short',
	'int',
	'long',
	'float',
	'double',
]

#############################################################################

QUALIFIERS = [
	'const',
	'register',
	'volatile',
	'struct',
	'enum',
]

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

def emit_intPubProlog(ctx, fp):
	INT_ASSET = ctx['int_asset']

	cb.utils.printf(fp, '/* Authors : %s' % INT_ASSET['authors'])
	cb.utils.printf(fp, ' * Emails  : %s' % INT_ASSET['emails'])
	cb.utils.printf(fp, ' *')
	cb.utils.printf(fp, ' * Version : %d.%d (%s)' % (ctx['major'], ctx['minor'], INT_ASSET['date']))
	cb.utils.printf(fp, ' *')
	cb.utils.printf(fp, ' * %s' % INT_ASSET['description'])	
	cb.utils.printf(fp, ' */')
	cb.utils.printf(fp, '')

	emit_separator(ctx, fp)

	cb.utils.printf(fp, '#ifndef __%s_H' % ctx['name'].upper())
	cb.utils.printf(fp, '#define __%s_H' % ctx['name'].upper())
	cb.utils.printf(fp, '')

	emit_separator(ctx, fp)

	cb.utils.printf(fp, '#include <stddef.h>')
	cb.utils.printf(fp, '#include <stdint.h>')
	cb.utils.printf(fp, '#include <stdbool.h>')
	cb.utils.printf(fp, '')

#############################################################################

def emit_intPrivProlog(ctx, fp):
	INT_ASSET = ctx['int_asset']

	cb.utils.printf(fp, '/* Authors : %s' % INT_ASSET['authors'])
	cb.utils.printf(fp, ' * Emails  : %s' % INT_ASSET['emails'])
	cb.utils.printf(fp, ' *')
	cb.utils.printf(fp, ' * Version : %d.%d (%s)' % (ctx['major'], ctx['minor'], INT_ASSET['date']))
	cb.utils.printf(fp, ' *')
	cb.utils.printf(fp, ' * %s' % INT_ASSET['description'])	
	cb.utils.printf(fp, ' */')
	cb.utils.printf(fp, '')

	emit_separator(ctx, fp)

	cb.utils.printf(fp, '#ifndef __%s_INTERNAL_H' % ctx['name'].upper())
	cb.utils.printf(fp, '#define __%s_INTERNAL_H' % ctx['name'].upper())
	cb.utils.printf(fp, '')

	emit_separator(ctx, fp)

	cb.utils.printf(fp, '#include "%s.h"' % ctx['name'])
	cb.utils.printf(fp, '')

#############################################################################

def emit_impProlog(ctx, fp):
	INT_ASSET = ctx['int_asset']

	cb.utils.printf(fp, '/* Authors : %s' % INT_ASSET['authors'])
	cb.utils.printf(fp, ' * Emails  : %s' % INT_ASSET['emails'])
	cb.utils.printf(fp, ' *')
	cb.utils.printf(fp, ' * Version : %d.%d (%s)' % (ctx['major'], ctx['minor'], INT_ASSET['date']))
	cb.utils.printf(fp, ' *')
	cb.utils.printf(fp, ' * %s' % INT_ASSET['description'])	
	cb.utils.printf(fp, ' */')
	cb.utils.printf(fp, '')

	emit_separator(ctx, fp)

	cb.utils.printf(fp, '#include "%s_internal.h"' % ctx['name'])
	cb.utils.printf(fp, '')

	if len(ctx['imp_extras']) > 0:
		emit_separator(ctx, fp)

		emit_extras(ctx, fp, ctx['imp_extras'])

#############################################################################

def emit_impProfileProlog(ctx, fp, p):
	INT_ASSET = ctx['int_asset']
	IMP_PROFILES = ctx['imp_profiles'][p]

	cb.utils.printf(fp, '/* Authors : %s' % INT_ASSET['authors'])
	cb.utils.printf(fp, ' * Emails  : %s' % INT_ASSET['emails'])
	cb.utils.printf(fp, ' *')
	cb.utils.printf(fp, ' * Version : %d.%d (%s)' % (ctx['major'], ctx['minor'], INT_ASSET['date']))
	cb.utils.printf(fp, ' *')
	cb.utils.printf(fp, ' * %s' % INT_ASSET['description'])	
	cb.utils.printf(fp, ' */')
	cb.utils.printf(fp, '')

	emit_separator(ctx, fp)

	cb.utils.printf(fp, '#include <stdlib.h>')
	cb.utils.printf(fp, '')
	cb.utils.printf(fp, '#include "%s_internal.h"' % ctx['name'])
	cb.utils.printf(fp, '')

	if len(IMP_PROFILES['extras']) > 0:
		emit_separator(ctx, fp)

		emit_extras(ctx, fp, IMP_PROFILES['extras'])

#############################################################################
# EPILOGS								    #
#############################################################################

def emit_intPubEpilog(ctx, fp):
	cb.utils.printf(fp, '#endif /* __%s_H */' % ctx['name'].upper())

	cb.utils.printf(fp, '')
	emit_separator(ctx, fp)

#############################################################################

def emit_intPrivEpilog(ctx, fp):
	cb.utils.printf(fp, '#endif /* __%s_INTERNAL_H */' % ctx['name'].upper())

	cb.utils.printf(fp, '')
	emit_separator(ctx, fp)

#############################################################################

def emit_impEpilog(ctx, fp):
	pass

#############################################################################
# UTILS
#############################################################################

def emit_pointerPrototype(ctx, fp, m, prefix = '', suffix = ''):

	proto = '%s (* %s%s%s)(struct %s_s *self' % (m['type'], prefix, m['name'], suffix, ctx['name'])

	for p in m['params']:
		proto += ', %s %s' % (p['type'], p['name'])

	cb.utils.printf(fp, proto + ');')

#############################################################################

def emit_functionPrototype(ctx, fp, m, prefix = '', suffix = ''):

	proto = '%s %s%s%s(%s_t *self' % (m['type'], prefix, m['name'], suffix, ctx['name'])

	for p in m['params']:
		proto += ', %s %s' % (p['type'], p['name'])

	cb.utils.printf(fp, proto + ')')

#############################################################################
# PUBLIC INTERFACE							    #
#############################################################################

def emit_impPubTypes(ctx, fp):
	INT_TYPES = ctx['int_types']

	for t in INT_TYPES:

		#############################################################

		if t['class'] == 'base':
			cb.utils.printf(fp, 'typedef %s %s;' % (t['from'], t['name']))
			cb.utils.printf(fp, '')

		#############################################################

		if t['class'] == 'enum':
			cb.utils.printf(fp, 'typedef enum %s' % t['name'])
			cb.utils.printf(fp, '{')

			for v in t['values']:
				cb.utils.printf(fp, '\t%s = 0x%X,' % (v['name'], cb.utils.getCnt(ctx)))

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

def emit_impPubDefinitions(ctx, fp):
	name = ctx['name']
	NAME = ctx['name'].upper()

	#####################################################################
	# PROFILES							    #
	#####################################################################

	emit_comment(ctx, fp, 'PROFILE ENUMS')

	cb.utils.printf(fp, 'typedef enum %s_profiles_e' % name)
	cb.utils.printf(fp, '{')

	for p in ctx['int_profiles']:
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

	for e in ctx['int_extensions']:
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

	for e in ctx['int_extensions']:

		for m in e['methods']:
			cb.utils.printf(fp, '\t%s_METHOD_%s_%s = 0x%X,' % (NAME, e['name'].upper(), m['name'].upper(), cb.utils.getCnt(ctx)))

	cb.utils.printf(fp, '')
	cb.utils.printf(fp, '} %s_methods_t;' % name)

	cb.utils.printf(fp, '')

	#####################################################################
	# STRUCTURE							    #
	#####################################################################

	emit_comment(ctx, fp, 'STRUCTURE')

	cb.utils.printf(fp, 'typedef struct %s_s' % ctx['name'])
	cb.utils.printf(fp, '{')

	for e in ctx['int_extensions']:

		cb.utils.printf(fp, '\tstruct {')

		for m in e['methods']:

			cb.utils.writef(fp, '\t\t'),
			emit_pointerPrototype(ctx, fp, m, '', '')

		cb.utils.printf(fp, '')
		cb.utils.printf(fp, '\t\tvoid *user;')
		cb.utils.printf(fp, '')
		cb.utils.printf(fp, '\t} *%s;\n' % e['name'])		

	cb.utils.printf(fp, '\tvoid *user;')
	cb.utils.printf(fp, '')
	cb.utils.printf(fp, '} %s_t;' % ctx['name'])

	cb.utils.printf(fp, '')

#############################################################################

def emit_impPubMethods(ctx, fp):
	name = ctx['name']

	cb.utils.printf(fp, 'int %s_getMajor(void);' % name)
	cb.utils.printf(fp, 'int %s_getMinor(void);' % name)
	cb.utils.printf(fp, '')
	cb.utils.printf(fp, 'bool %s_initialize(struct %s_s *, %s_profiles_t);' % (name, name, name))
	cb.utils.printf(fp, 'bool %s_finalize(struct %s_s *, %s_profiles_t);' % (name, name, name))
	cb.utils.printf(fp, '')
	cb.utils.printf(fp, 'bool %s_checkExt(struct %s_s *, %s_extensions_t);' % (name, name, name))
	cb.utils.printf(fp, 'const char *%s_getExtName(struct %s_s *, %s_extensions_t);' % (name, name, name))
	cb.utils.printf(fp, 'const char *%s_getExtDesc(struct %s_s *, %s_extensions_t);' % (name, name, name))
	cb.utils.printf(fp, '')
	cb.utils.printf(fp, 'bool %s_checkMet(struct %s_s *, %s_methods_t);' % (name, name, name))
	cb.utils.printf(fp, 'const char *%s_getMetName(struct %s_s *, %s_methods_t);' % (name, name, name))
	cb.utils.printf(fp, 'const char *%s_getMetDesc(struct %s_s *, %s_methods_t);' % (name, name, name))
	cb.utils.printf(fp, '')

#############################################################################
# PRIVATE INTERFACE							    #
#############################################################################

def emit_impPrivConstraints(ctx, fp):
	INT_CONSTRAINTS = ctx['int_constraints']

	for c in INT_CONSTRAINTS:
		cb.utils.printf(fp, 'typedef enum %s_s' % c['name'])
		cb.utils.printf(fp, '{')

		for k in c['keys']:
			cb.utils.printf(fp, '\t%s,' % k['name'].upper())

		cb.utils.printf(fp, '')
		cb.utils.printf(fp, '} %s_t;' % c['name'])
		cb.utils.printf(fp, '')

#############################################################################

def emit_impPrivMethods(ctx, fp):

	for c in ctx['int_constraints']:
		cb.utils.printf(fp, 'extern enum %s_s %s;' % (c['name'], c['name'].upper()))

	cb.utils.printf(fp, '')

	emit_separator(ctx, fp)

	cb.utils.printf(fp, 'bool __%s_ctor(struct %s_s *);' % (ctx['name'], ctx['name']))
	cb.utils.printf(fp, 'bool __%s_dtor(struct %s_s *);' % (ctx['name'], ctx['name']))

	cb.utils.printf(fp, '')

	for p in ctx['int_profiles']:
		cb.utils.printf(fp, 'bool %s_%s_ctor(struct %s_s *);' % (ctx['name'], p['name'], ctx['name']))
		cb.utils.printf(fp, 'bool %s_%s_dtor(struct %s_s *);' % (ctx['name'], p['name'], ctx['name']))

		cb.utils.printf(fp, '')

#############################################################################
# IMPLEMENTATION							    #
#############################################################################

def emit_extras(ctx, fp, EXTRAS):

	for e in EXTRAS:

		for c in e:

			for t in c['txts']:
				cb.utils.printf(fp, t)

	cb.utils.printf(fp, '')

#############################################################################
# GLOBAL IMPLEMENTATION							    #
#############################################################################

def emit_impConstraints(ctx, fp):

	for constraint in ctx['int_constraints']:
		cb.utils.printf(fp, '%s_t %s = (%s_t) -1;' % (constraint['name'], constraint['name'].upper(), constraint['name']))

	cb.utils.printf(fp, '')

#############################################################################

def emit_impCtor(ctx, fp):

	i = 0

	for ctor in ctx['imp_ctors']:

		for code in ctor:

			for txt in code['txts']:

				cb.utils.printf(fp, 'static bool __%s_ctor%d(%s_t *self)' % (ctx['name'], i, ctx['name']))
				cb.utils.printf(fp, '{')
				cb.utils.printf(fp, '%s' % txt)
				cb.utils.printf(fp, '}')
				cb.utils.printf(fp, '')
				emit_separator(ctx, fp)

				i += 1

	##

	i = 0

	cb.utils.printf(fp, 'static bool __%s_ctor(%s_t *self)' % (ctx['name'], ctx['name']))
	cb.utils.printf(fp, '{')
	cb.utils.printf(fp, '\tbool result = true;')
	cb.utils.printf(fp, '')

	for ctor in ctx['imp_ctors']:

		for code in ctor:

			if len(code['condition']) > 0:
				cb.utils.printf(fp, '\tif(%s)' % code['condition'])

			cb.utils.printf(fp, '\t{')

			for txt in code['txts']:
				cb.utils.printf(fp, '\t\tresult = __%s_ctor%d(self);' % (ctx['name'], i))
				i += 1

			cb.utils.printf(fp, '\t\tgoto __next;')
			cb.utils.printf(fp, '\t}')
			cb.utils.printf(fp, '')

	if i > 0:
		cb.utils.printf(fp, '\tresult = false;')
		cb.utils.printf(fp, '')
		cb.utils.printf(fp, '__next:')

	cb.utils.printf(fp, '\treturn result;')
	cb.utils.printf(fp, '}')

	cb.utils.printf(fp, '')

#############################################################################

def emit_impDtor(ctx, fp):

	i = 0

	for dtor in ctx['imp_dtors']:

		for code in dtor:

			for txt in code['txts']:

				cb.utils.printf(fp, 'static bool __%s_dtor%d(%s_t *self)' % (ctx['name'], i, ctx['name']))
				cb.utils.printf(fp, '{')
				cb.utils.printf(fp, '%s' % txt)
				cb.utils.printf(fp, '}')
				cb.utils.printf(fp, '')
				emit_separator(ctx, fp)

				i += 1

	##

	i = 0

	cb.utils.printf(fp, 'static bool __%s_dtor(%s_t *self)' % (ctx['name'], ctx['name']))
	cb.utils.printf(fp, '{')
	cb.utils.printf(fp, '\tbool result = true;')
	cb.utils.printf(fp, '')

	for dtor in ctx['imp_dtors']:

		for code in dtor:

			if len(code['condition']) != 0:
				cb.utils.printf(fp, '\tif(%s)' % code['condition'])

			cb.utils.printf(fp, '\t{')

			for txt in code['txts']:
				cb.utils.printf(fp, '\t\tresult = __%s_dtor%d(self);' % (ctx['name'], i))
				i += 1

			cb.utils.printf(fp, '\t\tgoto __next;')
			cb.utils.printf(fp, '\t}')
			cb.utils.printf(fp, '')

	if i > 0:
		cb.utils.printf(fp, '\tresult = false;')
		cb.utils.printf(fp, '')
		cb.utils.printf(fp, '__next:')

	cb.utils.printf(fp, '\treturn result;')
	cb.utils.printf(fp, '}')

	cb.utils.printf(fp, '')

#############################################################################

def emit_impMethods(ctx, fp):

	name = ctx['name']

	#####################################################################

	cb.utils.printf(fp, 'int %s_getMajor(void)' % name)
	cb.utils.printf(fp, '{')
	cb.utils.printf(fp, '\treturn %d;' % ctx['major'])
	cb.utils.printf(fp, '}')
	cb.utils.printf(fp, '')

	#####################################################################

	emit_separator(ctx, fp)

	#####################################################################

	cb.utils.printf(fp, 'int %s_getMinor(void)' % name)
	cb.utils.printf(fp, '{')
	cb.utils.printf(fp, '\treturn %d;' % ctx['minor'])
	cb.utils.printf(fp, '}')
	cb.utils.printf(fp, '')

	#####################################################################

	emit_separator(ctx, fp)

	#####################################################################

	cb.utils.printf(fp, 'bool %s_initialize(%s_t *interface, %s_profiles_t profile)' % (name, name, name))
	cb.utils.printf(fp, '{')
	cb.utils.printf(fp, '\tbool result;')
	cb.utils.printf(fp, '')

	cb.utils.printf(fp, '\tswitch(profile)')
	cb.utils.printf(fp, '\t{')

	for p in ctx['int_profiles']:
		cb.utils.printf(fp, '\t\tcase %s_PROFILE_%s:' % (name.upper(), p['name'].upper()))
		cb.utils.printf(fp, '\t\t\tresult = %s_%s_ctor(interface);' % (name, p['name']))
		cb.utils.printf(fp, '\t\t\tbreak;')
		cb.utils.printf(fp, '')

	cb.utils.printf(fp, '\t\tdefault:')
	cb.utils.printf(fp, '\t\t\tresult = false;')
	cb.utils.printf(fp, '\t\t\tbreak;')

	cb.utils.printf(fp, '\t}')

	cb.utils.printf(fp, '')
	cb.utils.printf(fp, '\treturn result;')
	cb.utils.printf(fp, '}')
	cb.utils.printf(fp, '')

	#####################################################################

	emit_separator(ctx, fp)

	#####################################################################

	cb.utils.printf(fp, 'bool %s_checkExt(%s_t *interface, %s_extensions_t extension)' % (name, name, name))
	cb.utils.printf(fp, '{')
	cb.utils.printf(fp, '\tbool result;')
	cb.utils.printf(fp, '')

	cb.utils.printf(fp, '\tswitch(extension)')
	cb.utils.printf(fp, '\t{')

	for e in ctx['int_extensions']:
		cb.utils.printf(fp, '\t\tcase %s_EXTENSION_%s:' % (name.upper(), e['name'].upper()))
		cb.utils.printf(fp, '\t\t\tresult = interface->%s != NULL;' % e['name'])
		cb.utils.printf(fp, '\t\t\tbreak;')
		cb.utils.printf(fp, '')

	cb.utils.printf(fp, '\t\tdefault:')
	cb.utils.printf(fp, '\t\t\tresult = false;')
	cb.utils.printf(fp, '\t\t\tbreak;')

	cb.utils.printf(fp, '\t}')		

	cb.utils.printf(fp, '')
	cb.utils.printf(fp, '\treturn result;')
	cb.utils.printf(fp, '}')
	cb.utils.printf(fp, '')

	#####################################################################

	emit_separator(ctx, fp)

	#####################################################################

	cb.utils.printf(fp, 'bool %s_checkMet(%s_t *interface, %s_methods_t method)' % (name, name, name))
	cb.utils.printf(fp, '{')
	cb.utils.printf(fp, '\tbool result;')
	cb.utils.printf(fp, '')

	cb.utils.printf(fp, '\tswitch(method)')
	cb.utils.printf(fp, '\t{')

	for e in ctx['int_extensions']:

		for m in e['methods']:
			cb.utils.printf(fp, '\t\tcase %s_METHOD_%s_%s:' % (name.upper(), e['name'].upper(), m['name'].upper()))
			cb.utils.printf(fp, '\t\t\tresult = interface->%s->%s != NULL;' % (e['name'], m['name']))
			cb.utils.printf(fp, '\t\t\tbreak;')
			cb.utils.printf(fp, '')

	cb.utils.printf(fp, '\t\tdefault:')
	cb.utils.printf(fp, '\t\t\tresult = false;')
	cb.utils.printf(fp, '\t\t\tbreak;')

	cb.utils.printf(fp, '\t}')		

	cb.utils.printf(fp, '')
	cb.utils.printf(fp, '\treturn result;')
	cb.utils.printf(fp, '}')
	cb.utils.printf(fp, '')

#############################################################################
# PROFILE IMPLEMENTATION						    #
#############################################################################

# A RELIRE #
# A RELIRE #
# A RELIRE #
# A RELIRE #
# A RELIRE #
# A RELIRE #
# A RELIRE #
# A RELIRE #
# A RELIRE #
# A RELIRE #
# A RELIRE #
# A RELIRE #
# A RELIRE #
# A RELIRE #
# A RELIRE #
# A RELIRE #
# A RELIRE #
# A RELIRE #
# A RELIRE #
# A RELIRE #
# A RELIRE #
# A RELIRE #
# A RELIRE #
# A RELIRE #

def emit_impProfileMethods(ctx, fp, p):
	IMP_PROFILES = ctx['imp_profiles'][p]
	IMP_EXTENSIONS = IMP_PROFILES['extensions']

	for e in IMP_EXTENSIONS:
        	IMP_METHODS = IMP_EXTENSIONS[e]['methods']

		ext = cb.utils.int_getExtension(ctx, e)

		for m in IMP_METHODS:
                	i = 0

			met = cb.utils.int_getMethod(ext, m)

                        for c in IMP_METHODS[m]:
				prefix = '__%s_' % e
				suffix = '%d' % i

				##

				if len(c['txts']) >= 1:
					emit_functionPrototype(ctx, fp, met, prefix, suffix)
	  				cb.utils.printf(fp, '{')

					cb.utils.printf(fp, c['txts'][0])

	 				cb.utils.printf(fp, '}')

					cb.utils.printf(fp, '')
					emit_separator(ctx, fp)

				i += 1

#############################################################################

def emit_impProfileCtor(ctx, fp, p):
	IMP_PROFILES = ctx['imp_profiles'][p]
	INT_EXTENSIONS = ctx['int_extensions']

	##

	i = 0

	for ctor in IMP_PROFILES['ctors']:

		for code in ctor:

			for txt in code['txts']:

				cb.utils.printf(fp, 'bool __%s_%s_ctor%d(%s_t *self)' % (ctx['name'], p, i, ctx['name']))
				cb.utils.printf(fp, '{')
				cb.utils.printf(fp, '%s' % txt)
				cb.utils.printf(fp, '}')
				cb.utils.printf(fp, '')
				emit_separator(ctx, fp)

				i += 1

	##

	for e in IMP_PROFILES['extensions']:
		emit_impExtensionCtor(ctx, fp, p, e)

	##

	cb.utils.printf(fp, 'bool __%s_%s_ctor(%s_t *self)' % (ctx['name'], p, ctx['name']))
	cb.utils.printf(fp, '{')

	##

	cb.utils.printf(fp, '\tif(__%s_ctor(self) == false)' % ctx['name'])
	cb.utils.printf(fp, '\t{')
	cb.utils.printf(fp, '\t\treturn false;')
	cb.utils.printf(fp, '\t}')
	cb.utils.printf(fp, '')

	##

	cb.utils.printf(fp, '\tbool result = true;')

	i = 0

	for ctor in IMP_PROFILES['ctors']:

		for code in ctor:

			cb.utils.printf(fp, '')

			if len(code['condition']) == 0:
				cb.utils.printf(fp, '\t{')
				for txt in code['txts']:
					cb.utils.printf(fp, '\t\tresult = result && __%s_%s_ctor%d(self);' % (ctx['name'], p, i))
					i += 1
				cb.utils.printf(fp, '\t\tgoto __next1;')
				cb.utils.printf(fp, '\t}')

			else:
				cb.utils.printf(fp, '\tif(%s)' % code['condition'])
				cb.utils.printf(fp, '\t{')
				for txt in code['txts']:
					cb.utils.printf(fp, '\t\tresult = result && __%s_%s_ctor%d(self);' % (ctx['name'], p, i))
					i += 1
				cb.utils.printf(fp, '\t\tgoto __next1;')
				cb.utils.printf(fp, '\t}')

	cb.utils.printf(fp, '')

	if i > 0:
		cb.utils.printf(fp, '\tresult = false;')
		cb.utils.printf(fp, '')
		cb.utils.printf(fp, '__next1:')

	##

	i = 0

	if len(IMP_PROFILES['extensions']) > 0:

		cb.utils.printf(fp, '\tif(result != false)')
		cb.utils.printf(fp, '\t{')

		for e in INT_EXTENSIONS:

			if IMP_PROFILES['extensions'].has_key(e['name']) != False:

				cb.utils.printf(fp, '\t\tif((result = __%s_%s_%s_ctor(self)) == false)' % (ctx['name'], p, e['name']))
				cb.utils.printf(fp, '\t\t{')
				cb.utils.printf(fp, '\t\t\tgoto __next2;')
				cb.utils.printf(fp, '\t\t}')

				i += 1

		cb.utils.printf(fp, '\t}')
		cb.utils.printf(fp, '')

	if i > 0:
		cb.utils.printf(fp, '__next2:')

	##

	cb.utils.printf(fp, '\tif(result == false)')
	cb.utils.printf(fp, '\t{')
	cb.utils.printf(fp, '\t\t%s_%s_dtor(self);' % (ctx['name'], p))
	cb.utils.printf(fp, '\t}')
	cb.utils.printf(fp, '')

	##

	cb.utils.printf(fp, '\treturn result;')

	cb.utils.printf(fp, '}')
	cb.utils.printf(fp, '')

	emit_separator(ctx, fp)

#############################################################################

def emit_impProfileDtor(ctx, fp, p):
	IMP_PROFILES = ctx['imp_profiles'][p]
	INT_EXTENSIONS = ctx['int_extensions']

	##

	i = 0

	for dtor in IMP_PROFILES['dtors']:

		for code in dtor:

			for txt in code['txts']:

				cb.utils.printf(fp, 'bool __%s_%s_dtor%d(%s_t *self)' % (ctx['name'], p, i, ctx['name']))
				cb.utils.printf(fp, '{')
				cb.utils.printf(fp, '%s' % txt)
				cb.utils.printf(fp, '}')
				cb.utils.printf(fp, '')
				emit_separator(ctx, fp)

				i += 1

	##

	for e in reversed(INT_EXTENSIONS):
		emit_impExtensionDtor(ctx, fp, p, e['name'])

	##

	cb.utils.printf(fp, 'bool __%s_%s_dtor(%s_t *self)' % (ctx['name'], p, ctx['name']))
	cb.utils.printf(fp, '{')

	##

	cb.utils.printf(fp, '\tbool result = true;')
	cb.utils.printf(fp, '')

	for e in reversed(INT_EXTENSIONS):

		if IMP_PROFILES['extensions'].has_key(e['name']) != False:

			if IMP_PROFILES['extensions'].has_key(e['name']) != False:

				cb.utils.printf(fp, '\tresult = result && __%s_%s_%s_dtor(self);' % (ctx['name'], p, e['name']))

	##

	i = 0

	for dtor in IMP_PROFILES['dtors']:

		for code in dtor:

			cb.utils.printf(fp, '')

			if len(code['condition']) == 0:
				cb.utils.printf(fp, '\t{')
				for txt in code['txts']:
					cb.utils.printf(fp, '\t\tresult = result && __%s_%s_dtor%d(self);' % (ctx['name'], p, i))
					i += 1
				cb.utils.printf(fp, '\t\tgoto __next1;')
				cb.utils.printf(fp, '\t}')

			else:
				cb.utils.printf(fp, '\tif(%s)' % code['condition'])
				cb.utils.printf(fp, '\t{')
				for txt in code['txts']:
					cb.utils.printf(fp, '\t\tresult = result && __%s_%s_dtor%d(self);' % (ctx['name'], p, i))
					i += 1
				cb.utils.printf(fp, '\t\tgoto __next1;')
				cb.utils.printf(fp, '\t}')

	cb.utils.printf(fp, '')

	if i > 0:
			cb.utils.printf(fp, '__next1:')

	##

	cb.utils.printf(fp, '\treturn result && __%s_dtor(self);' % ctx['name'])
	cb.utils.printf(fp, '}')
	cb.utils.printf(fp, '')

	emit_separator(ctx, fp)

#############################################################################
# PROFILE IMPLEMENTATION						    #
#############################################################################

def emit_impExtensionCtor(ctx, fp, p, e):
	IMP_PROFILES = ctx['imp_profiles'][p]

	if IMP_PROFILES['extensions'].has_key(e) == False:
		return

	IMP_EXTENSIONS = IMP_PROFILES['extensions'][e]

	i = 0

	for ctor in IMP_EXTENSIONS['ctors']:

		for code in ctor:

			for txt in code['txts']:

				cb.utils.printf(fp, 'bool __%s_%s_%s_ctor%d(%s_t *self)' % (ctx['name'], p, e, i, ctx['name']))
				cb.utils.printf(fp, '{')
				cb.utils.printf(fp, '%s' % txt)
				cb.utils.printf(fp, '}')
				cb.utils.printf(fp, '')
				emit_separator(ctx, fp)

				i += 1

	##

	cb.utils.printf(fp, 'bool __%s_%s_%s_ctor(%s_t *self)' % (ctx['name'], p, e, ctx['name']))
	cb.utils.printf(fp, '{')
	cb.utils.printf(fp, '\tbool result = true;')

	i = 0

	for ctor in IMP_EXTENSIONS['ctors']:

		for code in ctor:

			cb.utils.printf(fp, '')

			if len(code['condition']) == 0:
				cb.utils.printf(fp, '\t{')
				for txt in code['txts']:
					cb.utils.printf(fp, '\t\tresult = __%s_%s_%s_ctor%d(self);' % (ctx['name'], p, e, i))
					i += 1
				cb.utils.printf(fp, '\t\tgoto __next;')
				cb.utils.printf(fp, '\t}')

			else:
				cb.utils.printf(fp, '\tif(%s)' % code['condition'])
				cb.utils.printf(fp, '\t{')
				for txt in code['txts']:
					cb.utils.printf(fp, '\t\tresult = __%s_%s_%s_ctor%d(self);' % (ctx['name'], p, e, i))
					i += 1
				cb.utils.printf(fp, '\t\tgoto __next;')
				cb.utils.printf(fp, '\t}')


	cb.utils.printf(fp, '')

	if i > 0:
		cb.utils.printf(fp, '\tresult = false;')
		cb.utils.printf(fp, '')
		cb.utils.printf(fp, '__next:')

	##

	IMP_METHODS = IMP_EXTENSIONS['methods']

	cb.utils.printf(fp, '')
	cb.utils.printf(fp, '\tself->%s = malloc(sizeof(self->%s[0]));' % (e, e))

	for m in IMP_METHODS:
		cb.utils.printf(fp, '')
		cb.utils.printf(fp, '\t/* %s */' % m)

		#############################################################
		# UNCONDITIONAL ASSIGNATION				    #
		#############################################################

		for (i, c) in enumerate(IMP_METHODS[m]):

			condition = c['condition'].strip()

			if len(condition) == 0 and len(c['txts']) > 0:
				cb.utils.printf(fp, '\t{')
				cb.utils.printf(fp, '\t\tself->%s->%s = __%s_%s%d;' % (e, m, e, m, i))
				cb.utils.printf(fp, '\t}')

		#############################################################
		# CONDITIONAL ASSIGNATION				    #
		#############################################################

		cnt = 0

		for (i, c) in enumerate(IMP_METHODS[m]):

			condition = c['condition'].strip()

			if len(condition) >= 1 and len(c['txts']) > 0:
				if cnt == 0:
					cb.utils.printf(fp, '\t/**/ if(%s)' % condition)
				else:
					cb.utils.printf(fp, '\telse if(%s)' % condition)

				cb.utils.printf(fp, '\t{')
				cb.utils.printf(fp, '\t\tself->%s->%s = __%s_%s%d;' % (e, m, e, m, i))
				cb.utils.printf(fp, '\t}')

				cnt += 1

		#############################################################

	##

	cb.utils.printf(fp, '\treturn result;')
	cb.utils.printf(fp, '}')
	cb.utils.printf(fp, '')

	emit_separator(ctx, fp)

#############################################################################

def emit_impExtensionDtor(ctx, fp, p, e):
	IMP_PROFILES = ctx['imp_profiles'][p]

	if IMP_PROFILES['extensions'].has_key(e) == False:
		return

	IMP_EXTENSIONS = IMP_PROFILES['extensions'][e]

	i = 0

	for dtor in IMP_EXTENSIONS['dtors']:

		for code in dtor:

			for txt in code['txts']:

				cb.utils.printf(fp, 'bool __%s_%s_%s_dtor%d(%s_t *self)' % (ctx['name'], p, e, i, ctx['name']))
				cb.utils.printf(fp, '{')
				cb.utils.printf(fp, '%s' % txt)
				cb.utils.printf(fp, '}')
				cb.utils.printf(fp, '')
				emit_separator(ctx, fp)

				i += 1

	##

	cb.utils.printf(fp, 'bool __%s_%s_%s_dtor(%s_t *self)' % (ctx['name'], p, e, ctx['name']))
	cb.utils.printf(fp, '{')

	##

	IMP_METHODS = IMP_EXTENSIONS['methods']

	cb.utils.printf(fp, '\tself->%s = realloc(self->%s, sizeof(self->%s[0]));' % (e, e, e))
	cb.utils.printf(fp, '')

	##

	cb.utils.printf(fp, '\tbool result = true;')

	i = 0

	for dtor in IMP_EXTENSIONS['dtors']:

		for code in dtor:

			cb.utils.printf(fp, '')

			if len(code['condition']) == 0:
				cb.utils.printf(fp, '\t{')
				for txt in code['txts']:
					cb.utils.printf(fp, '\t\tresult = __%s_%s_%s_dtor%d(self);' % (ctx['name'], p, e, i))
					i += 1
				cb.utils.printf(fp, '\t\tgoto __next;')
				cb.utils.printf(fp, '\t}')

			else:
				cb.utils.printf(fp, '\tif(%s)' % code['condition'])
				cb.utils.printf(fp, '\t{')
				for txt in code['txts']:
					cb.utils.printf(fp, '\t\tresult = __%s_%s_%s_dtor%d(self);' % (ctx['name'], p, e, i))
					i += 1
				cb.utils.printf(fp, '\t\tgoto __next;')
				cb.utils.printf(fp, '\t}')

	cb.utils.printf(fp, '')

	if i > 0:
		cb.utils.printf(fp, '\tresult = false;')
		cb.utils.printf(fp, '')
		cb.utils.printf(fp, '__next:')

	cb.utils.printf(fp, '\treturn result;')
	cb.utils.printf(fp, '}')
	cb.utils.printf(fp, '')

	emit_separator(ctx, fp)

#############################################################################


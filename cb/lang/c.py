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

	proto = '%s (* %s%s%s)(' % (m['type'], prefix, m['name'], suffix)

	if len(m['params']) > 0:
		for p in m['params']:
			proto += '%s %s,' % (p['type'], p['name'])
	else:
		proto += 'void,'

	cb.utils.printf(fp, proto[: -1] + ');')

#############################################################################

def emit_functionPrototype(ctx, fp, m, prefix = '', suffix = ''):

	proto = '%s %s%s%s(' % (m['type'], prefix, m['name'], suffix)

	if len(m['params']) > 0:
		for p in m['params']:
			proto += '%s %s,' % (p['type'], p['name'])
	else:
		proto += 'void,'

	cb.utils.printf(fp, proto[: -1] + ')')

#############################################################################

def emit_functionPrototypeCheck(ctx, fp, m, prefix = '', suffix = ''):

	proto = 'bool %s%s%s(' % (prefix, m['name'], suffix)

	if len(m['params']) > 0:
		for p in m['params']:
			proto += '%s %s,' % (p['type'], p['name'])
	else:
		proto += 'void,'

	cb.utils.printf(fp, proto[: -1] + ')')

#############################################################################

def emit_functionPrototypeBest(ctx, fp, m, prefix = '', suffix = ''):

	proto = 'bool %s%s%s(' % (prefix, m['name'], suffix)

	if len(m['params']) > 0:
		for p in m['params']:
			proto += '%s *%s,' % (p['type'], p['name'])
	else:
		proto += 'void,'

	cb.utils.printf(fp, proto[: -1] + ')')

#############################################################################
# PUBLIC INTERFACE							    #
#############################################################################

def emit_impPubTypes(ctx, fp, t):
	cb.utils.printf(fp, 'typedef %s %s;' % (t[0], t[1]['from']))
	cb.utils.printf(fp, '')

#############################################################################

def emit_impPubEnums(ctx, fp, t):
	cb.utils.printf(fp, 'typedef enum %s' % t[0])
	cb.utils.printf(fp, '{')

	for u in t[1]:
		for v in t[1][u]:
			cb.utils.printf(fp, '\t%s = 0x%X,' % (v['name'], cb.utils.getCnt(ctx)))

	cb.utils.printf(fp, '')
	cb.utils.printf(fp, '} %s;' % t[0])
	cb.utils.printf(fp, '')

#############################################################################

def emit_impPubStructs(ctx, fp, t):
	cb.utils.printf(fp, 'typedef struct %s' % t[0])
	cb.utils.printf(fp, '{')

	for u in t[1]:
		for v in t[1][u]:
			cb.utils.printf(fp, '\t%s %s;' % (v['type'], v['name']))

	cb.utils.printf(fp, '')
	cb.utils.printf(fp, '} %s;' % t[0])
	cb.utils.printf(fp, '')

#############################################################################

def emit_impPubDefinitions(ctx, fp):
	name = ctx['name']
	NAME = ctx['name'].upper()

	#####################################################################
	# PROFILES							    #
	#####################################################################

	emit_comment(ctx, fp, 'PROFILES')

	cb.utils.printf(fp, 'typedef enum %s_profiles_e' % name)
	cb.utils.printf(fp, '{')

	for p in ctx['int_profiles']:
		cb.utils.printf(fp, '\t%s_%s = 0x%X,' % (NAME, p.upper(), cb.utils.getCnt(ctx)))

	cb.utils.printf(fp, '')
	cb.utils.printf(fp, '} %s_profiles_t;' % name)

	cb.utils.printf(fp, '')

	#####################################################################
	# EXTENTIONS							    #
	#####################################################################

	emit_comment(ctx, fp, 'EXTENTIONS')

	cb.utils.printf(fp, 'typedef enum %s_extentions_e' % name)
	cb.utils.printf(fp, '{')

	for e in ctx['int_extensions']:
		cb.utils.printf(fp, '\t%s_%s = 0x%X,' % (NAME, e['name'].upper(), cb.utils.getCnt(ctx)))

	cb.utils.printf(fp, '')
	cb.utils.printf(fp, '} %s_extentions_t;' % name)

	cb.utils.printf(fp, '')

	#####################################################################
	# METHODS							    #
	#####################################################################

	emit_comment(ctx, fp, 'METHODS')

	cb.utils.printf(fp, 'typedef enum %s_methods_e' % name)
	cb.utils.printf(fp, '{')

	for e in ctx['int_extensions']:

		for m in e['methods']:
			cb.utils.printf(fp, '\t%s_%s_%s = 0x%X,' % (NAME, e['name'].upper(), m['name'].upper(), cb.utils.getCnt(ctx)))

	cb.utils.printf(fp, '')
	cb.utils.printf(fp, '} %s_methods_t;' % name)

	cb.utils.printf(fp, '')

#############################################################################

def emit_impPubExtensionStructs(ctx, fp):
	cb.utils.printf(fp, 'typedef struct %s_s' % ctx['name'])
	cb.utils.printf(fp, '{')

	for e in ctx['int_extensions']:

		cb.utils.printf(fp, '\tstruct {')

		for m in e['methods']:

			cb.utils.writef(fp, '\t\t'),
			emit_pointerPrototype(ctx, fp, m, '', '')
			cb.utils.writef(fp, '\t\t'),
			emit_pointerPrototype(ctx, fp, m, '', '_check')
			cb.utils.writef(fp, '\t\t'),
			emit_pointerPrototype(ctx, fp, m, '', '_best')
			cb.utils.printf(fp, '')

		cb.utils.printf(fp, '\t} %s;\n' % e['name'])		

	cb.utils.printf(fp, '} %s_t;' % ctx['name'])

	cb.utils.printf(fp, '')

#############################################################################

def emit_impPubExtensionProfiles(ctx, fp):

	for e in ctx['int_profiles']:

		cb.utils.printf(fp, 'extern %s_t %s_%s;' % (ctx['name'], ctx['name'], e))

	cb.utils.printf(fp, '')

#############################################################################

def emit_impPubMethodPrototypes(ctx, fp):
	name = ctx['name']

	emit_comment(ctx, fp, 'LOW LEVEL METHODS')

	cb.utils.printf(fp, 'bool %s_initialize(void);' % name)
	cb.utils.printf(fp, 'bool %s_finalize(void);' % name)
	cb.utils.printf(fp, '')
	cb.utils.printf(fp, 'int %s_getMajor(void);' % name)
	cb.utils.printf(fp, 'int %s_getMinor(void);' % name)
	cb.utils.printf(fp, '')
	cb.utils.printf(fp, 'int %s_getProNr(void);' % name)
	cb.utils.printf(fp, 'const char *%s_getProName(int);' % name)
	cb.utils.printf(fp, 'const char *%s_getProDesc(int);' % name)
	cb.utils.printf(fp, '')
	cb.utils.printf(fp, 'int %s_getExtNr(int);' % name)
	cb.utils.printf(fp, 'const char *%s_getExtName(int, int);' % name)
	cb.utils.printf(fp, 'const char *%s_getExtDesc(int, int);' % name)
	cb.utils.printf(fp, '')
	cb.utils.printf(fp, 'int %s_getMetNr(int, int);' % name)
	cb.utils.printf(fp, 'const char *%s_getMetName(int, int, int);' % name)
	cb.utils.printf(fp, 'const char *%s_getMetDesc(int, int, int);' % name)

	cb.utils.printf(fp, '')

	emit_comment(ctx, fp, 'HIGH LEVEL METHODS')

	cb.utils.printf(fp, '%s_t *%s_getInterface(%s_profiles_t);' % (name, name, name))
	cb.utils.printf(fp, '')
	cb.utils.printf(fp, 'bool %s_checkExt(%s_profiles_t, %s_extentions_t);' % (name, name, name))
	cb.utils.printf(fp, 'const char *%s_getExtName(%s_profiles_t, %s_extentions_t);' % (name, name, name))
	cb.utils.printf(fp, 'const char *%s_getExtDesc(%s_profiles_t, %s_extentions_t);' % (name, name, name))
	cb.utils.printf(fp, '')
	cb.utils.printf(fp, 'bool %s_checkMet(%s_profiles_t, %s_methods_t);' % (name, name, name))
	cb.utils.printf(fp, 'const char *%s_getMetName(%s_profiles_t, %s_methods_t);' % (name, name, name))
	cb.utils.printf(fp, 'const char *%s_getMetDesc(%s_profiles_t, %s_methods_t);' % (name, name, name))

	cb.utils.printf(fp, '')

#############################################################################
# PRIVATE INTERFACE							    #
#############################################################################

def emit_impPrivConstraints(ctx, fp):
	INT_CONSTRAINTS = ctx['int_constraints']

	for c in INT_CONSTRAINTS:
		cb.utils.printf(fp, 'typedef enum %s_s' % c)
		cb.utils.printf(fp, '{')

		for key in INT_CONSTRAINTS[c]['keys']:
			cb.utils.printf(fp, '\t%s,' % key.upper())

		cb.utils.printf(fp, '')
		cb.utils.printf(fp, '} %s_t;' % c)
		cb.utils.printf(fp, '')

#############################################################################

def emit_impPrivMethodPrototypes(ctx, fp):

	for c in ctx['int_constraints']:
		cb.utils.printf(fp, 'extern enum %s_s %s;' % (c, c.upper()))

	cb.utils.printf(fp, '')

	emit_separator(ctx, fp)

	cb.utils.printf(fp, 'bool __%s_ctor(void);' % ctx['name'])
	cb.utils.printf(fp, 'bool __%s_dtor(void);' % ctx['name'])

	cb.utils.printf(fp, '')

#############################################################################
# IMPLEMENTATION							    #
#############################################################################

def emit_Xtor(ctx, fp, Xtors, cnt):

	#####################################################################
	# UNCONDITIONAL XTORS						    #
	#####################################################################

	for Xtor in Xtors:

		for code in Xtor:
			condition = code['condition'].strip()

			if len(condition) == 0:

				cb.utils.printf(fp, '\t{')

				for text in code['txts']:
					cb.utils.printf(fp, text)

				cb.utils.printf(fp, '\t}')

	#####################################################################
	# CONDITIONAL XTORS						    #
	#####################################################################

	for Xtor in Xtors:

		for code in Xtor:
			condition = code['condition'].strip()

			if len(condition) >= 1:

				if cnt == 0:
					cb.utils.printf(fp, '\t/**/ if(%s)' % condition)
				else:
					cb.utils.printf(fp, '\telse if(%s)' % condition)

				cb.utils.printf(fp, '\t{')

				for text in code['txts']:
					cb.utils.printf(fp, text)

				cb.utils.printf(fp, '\t}')

				cnt += 1

#############################################################################
# GLOBAL IMPLEMENTATION							    #
#############################################################################

def emit_impConstraints(ctx, fp):

	for constraint in ctx['int_constraints']:
		cb.utils.printf(fp, '%s_t %s = (%s_t) -1;' % (constraint, constraint.upper(), constraint))

	cb.utils.printf(fp, '')

#############################################################################

def emit_impCtor(ctx, fp):
	cb.utils.printf(fp, 'bool __%s_ctor(void)' % ctx['name'])
	cb.utils.printf(fp, '{')
	cb.utils.printf(fp, '\tbool result = true;')
	cb.utils.printf(fp, '')
	emit_Xtor(ctx, fp, ctx['imp_ctors'], 0)
	cb.utils.printf(fp, '')
	cb.utils.printf(fp, '\treturn result;')
	cb.utils.printf(fp, '}')

	cb.utils.printf(fp, '')

#############################################################################

def emit_impDtor(ctx, fp):
	cb.utils.printf(fp, 'bool __%s_dtor(void)' % ctx['name'])
	cb.utils.printf(fp, '{')
	cb.utils.printf(fp, '\tbool result = true;')
	cb.utils.printf(fp, '')
	emit_Xtor(ctx, fp, ctx['imp_dtors'], 0)
	cb.utils.printf(fp, '')
	cb.utils.printf(fp, '\treturn result;')
	cb.utils.printf(fp, '}')

	cb.utils.printf(fp, '')

#############################################################################

def emit_impHighLevelMethods(ctx, fp):
	pass

#############################################################################
# PROFILE IMPLEMENTATION						    #
#############################################################################

def emit_impProfileStruct(ctx, fp, p):
	cb.utils.printf(fp, '%s_t %s_%s = {};' % (ctx['name'], ctx['name'], p))

	cb.utils.printf(fp, '')

#############################################################################

def emit_impProfileMethods(ctx, fp, p):
	IMP_PROFILES = ctx['imp_profiles'][p]
	IMP_EXTENSIONS = IMP_PROFILES['extensions']

	for e in IMP_EXTENSIONS:
        	IMP_METHODS = IMP_EXTENSIONS[e]['methods']

		ext = cb.utils.getExtension(ctx, e)

		for m in IMP_METHODS:
                	i = 0

			met = cb.utils.getMethod(ext, m)

                        for c in IMP_METHODS[m]:
				prefix = '__%s_' % e

				suffix1 = '%d' % i
				suffix2 = '%d_check' % i
                		suffix3 = '%d_best' % i

				##

				if len(c['txts']) >= 1:
					emit_functionPrototype(ctx, fp, met, prefix, suffix1)
	  				cb.utils.printf(fp, '{')

					cb.utils.printf(fp, c['txts'][0])

	 				cb.utils.printf(fp, '}')

					cb.utils.printf(fp, '')
					emit_separator(ctx, fp)

					##

					emit_functionPrototypeCheck(ctx, fp, met, prefix, suffix2)
					cb.utils.printf(fp, '{')

					if len(c['txts']) >= 2:
						cb.utils.printf(fp, c['txts'][1])
					else:
						cb.utils.printf(fp, '\treturn true;')

					cb.utils.printf(fp, '}')

					cb.utils.printf(fp, '')
					emit_separator(ctx, fp)

					##

					emit_functionPrototypeBest(ctx, fp, met, prefix, suffix3)
					cb.utils.printf(fp, '{')

					if len(c['txts']) >= 3:
						cb.utils.printf(fp, c['txts'][2])
					else:
						cb.utils.printf(fp, '\treturn false;')

					cb.utils.printf(fp, '}')

					cb.utils.printf(fp, '')
					emit_separator(ctx, fp)

				i += 1

#############################################################################

def emit_impProfileCtor(ctx, fp, p):
	IMP_PROFILES = ctx['imp_profiles'][p]
	IMP_EXTENSIONS = IMP_PROFILES['extensions']

	cb.utils.printf(fp, 'bool %s_%s_ctor(void)' % (ctx['name'], p))
	cb.utils.printf(fp, '{')
	cb.utils.printf(fp, '\tif(__%s_ctor(void) == false)' % ctx['name'])
	cb.utils.printf(fp, '\t{')
	cb.utils.printf(fp, '\t\treturn false;')
	cb.utils.printf(fp, '\t}')
	cb.utils.printf(fp, '')
	cb.utils.printf(fp, '\tbool result = true;')
	cb.utils.printf(fp, '')

	emit_Xtor(ctx, fp, IMP_PROFILES['ctors'], 0)

	for e in IMP_EXTENSIONS:
		cb.utils.printf(fp, '')
		cb.utils.printf(fp, '\t/* %s */' % e)
		emit_Xtor(ctx, fp, IMP_EXTENSIONS[e]['ctors'], 99)

	for e in IMP_EXTENSIONS:
		IMP_METHODS = IMP_EXTENSIONS[e]['methods']

		for m in IMP_METHODS:
			cb.utils.printf(fp, '')
			cb.utils.printf(fp, '\t/* %s::%s */' % (e, m))

			#####################################################
			# UNCONDITIONAL ASSIGNATION			    #
			#####################################################

			for (i, c) in enumerate(IMP_METHODS[m]):

				condition = c['condition'].strip()

				if len(condition) == 0 and len(c['txts']) > 0:
					cb.utils.printf(fp, '\t{')
					cb.utils.printf(fp, '\t\t%s_%s.%s.%s = __%s%d;' % (ctx['name'], p, e, m, m, i))
					cb.utils.printf(fp, '\t\t%s_%s.%s.%s_check = __%s%d_check;' % (ctx['name'], p, e, m, m, i))
					cb.utils.printf(fp, '\t\t%s_%s.%s.%s_best = __%s%d;' % (ctx['name'], p, e, m, m, i))
					cb.utils.printf(fp, '\t}')

			#####################################################
			# CONDITIONAL ASSIGNATION			    #
			#####################################################

			cnt = 0

			for (i, c) in enumerate(IMP_METHODS[m]):

				condition = c['condition'].strip()

				if len(condition) >= 1 and len(c['txts']) > 0:
					if cnt == 0:
						cb.utils.printf(fp, '\t/**/ if(%s)' % condition)
					else:
						cb.utils.printf(fp, '\telse if(%s)' % condition)

					cb.utils.printf(fp, '\t{')
					cb.utils.printf(fp, '\t\t%s_%s.%s.%s = __%s_%s%d;' % (ctx['name'], p, e, m, e, m, i))
					cb.utils.printf(fp, '\t\t%s_%s.%s.%s_check = __%s_%s%d_check;' % (ctx['name'], p, e, m, e, m, i))
					cb.utils.printf(fp, '\t\t%s_%s.%s.%s_best = __%s_%s%d_best;' % (ctx['name'], p, e, m, e, m, i))
					cb.utils.printf(fp, '\t}')

					cnt += 1

			#####################################################

	cb.utils.printf(fp, '')
	cb.utils.printf(fp, '\treturn result;')
	cb.utils.printf(fp, '}')

	cb.utils.printf(fp, '')

#############################################################################

def emit_impProfileDtor(ctx, fp, p):
	IMP_PROFILES = ctx['imp_profiles'][p]
	IMP_EXTENSIONS = IMP_PROFILES['extensions']

	cb.utils.printf(fp, 'bool %s_%s_dtor(void)' % (ctx['name'], p))
	cb.utils.printf(fp, '{')
	cb.utils.printf(fp, '\tif(__%s_dtor(void) == false)' % ctx['name'])
	cb.utils.printf(fp, '\t{')
	cb.utils.printf(fp, '\t\treturn false;')
	cb.utils.printf(fp, '\t}')
	cb.utils.printf(fp, '')
	cb.utils.printf(fp, '\tbool result = true;')
	cb.utils.printf(fp, '')

	emit_Xtor(ctx, fp, IMP_PROFILES['dtors'], 0)

	for e in IMP_EXTENSIONS:
		cb.utils.printf(fp, '')
		cb.utils.printf(fp, '\t/* %s */' % e)
		emit_Xtor(ctx, fp, IMP_EXTENSIONS[e]['dtors'], 99)

	for e in IMP_EXTENSIONS:
		IMP_METHODS = IMP_EXTENSIONS[e]['methods']

		for m in IMP_METHODS:
			cb.utils.printf(fp, '')
			cb.utils.printf(fp, '\t/* %s::%s */' % (e, m))

			#####################################################
			# UNCONDITIONAL ASSIGNATION			    #
			#####################################################

			for (i, c) in enumerate(IMP_METHODS[m]):

				condition = c['condition'].strip()

				if len(condition) == 0 and len(c['txts']) > 0:
					cb.utils.printf(fp, '\t{')
					cb.utils.printf(fp, '\t\t%s_%s.%s.%s = NULL;' % (ctx['name'], p, e, m))
					cb.utils.printf(fp, '\t\t%s_%s.%s.%s_check = NULL;' % (ctx['name'], p, e, m))
					cb.utils.printf(fp, '\t\t%s_%s.%s.%s_best = NULL;' % (ctx['name'], p, e, m))
					cb.utils.printf(fp, '\t}')

			#####################################################
			# CONDITIONAL ASSIGNATION			    #
			#####################################################

			cnt = 0

			for (i, c) in enumerate(IMP_METHODS[m]):

				condition = c['condition'].strip()

				if len(condition) >= 1 and len(c['txts']) > 0:
					if cnt == 0:
						cb.utils.printf(fp, '\t/**/ if(%s)' % condition)
					else:
						cb.utils.printf(fp, '\telse if(%s)' % condition)

					cb.utils.printf(fp, '\t{')
					cb.utils.printf(fp, '\t\t%s_%s.%s.%s = NULL;' % (ctx['name'], p, e, m))
					cb.utils.printf(fp, '\t\t%s_%s.%s.%s_check = NULL;' % (ctx['name'], p, e, m))
					cb.utils.printf(fp, '\t\t%s_%s.%s.%s_best = NULL;' % (ctx['name'], p, e, m))
					cb.utils.printf(fp, '\t}')

					cnt += 1

			#####################################################

	cb.utils.printf(fp, '')
	cb.utils.printf(fp, '\treturn result;')
	cb.utils.printf(fp, '}')

	cb.utils.printf(fp, '')

#############################################################################


#!/usr/bin/env python

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

import os, sys, xml.dom.minidom

import cb.utils
import cb.parse
import cb.check
import cb.emit

#############################################################################
# CODE-BUILDER								    #
#############################################################################

def fixRelPath(path, prefix):

	if os.path.isabs(path) == False:
		path = prefix + os.sep + path

	return path

#############################################################################

def codebuilder_load_xml(ctx, fileName):
	#####################################################################

	if ctx.verbose:
		print('Loading \'%s\'...' % fileName)

	try:
		doc = xml.dom.minidom.parse(fileName)

	except:
		cb.utils.fatal(ctx, 'XML error in file `%s`, %s !' % (fileName, sys.exc_info()[1]))

	#####################################################################

	includes = doc.getElementsByTagName('include')

	if len(includes) > 0:

		dirName = fixRelPath(os.path.dirname(fileName), '.')

		for include in includes:

			fileName = fixRelPath(include.getAttribute('url'), dirName)

			#####################################################
			#####################################################

			subdoc = codebuilder_load_xml(ctx, fileName)

			for node in subdoc.documentElement.childNodes:
				include.parentNode.appendChild(node.cloneNode(1))

			#####################################################
			#####################################################

	return doc

#############################################################################

class codebuilder(cb.utils.context):
	#####################################################################

	def __init__(self):
		cb.utils.context.__init__(self)

	#####################################################################

	def parse(self, fileName):
		doc = codebuilder_load_xml(self, fileName)

		cb.parse.parseInterfacePublic(self,
			doc.getElementsByTagName('interface_public')
		)

		cb.parse.parseInterfacePrivate(self,
			doc.getElementsByTagName('interface_private')
		)

		cb.parse.parseImplementation(self,
			doc.getElementsByTagName('implementation')
		)

	#####################################################################

	def check(self):
		cb.check.checkInterfacePublic(self)
		cb.check.checkInterfacePrivate(self)
		cb.check.checkImplementation(self)

		cb.utils.status(self)

		if self.error != 0:
			cb.utils.fatal(self, 'Abort !')

	#####################################################################

	def emit(self):
		cb.emit.interfacePublic(self)
		cb.emit.interfacePrivate(self)
		cb.emit.implementation(self)

#############################################################################

def entry_point(argv):
	#####################################################################

	ctx = codebuilder()

	#####################################################################

	flag = 0

	args = []

	for arg in argv[1:]:

		arg = arg.strip()

		if   flag == 1:
			ctx.language = arg
			flag = 0

		elif flag == 2:
			ctx.profiles = arg
			flag = 0

		else:
			if   arg == '--authors':
				print('Jerome ODIER, Christophe SMEKENS')
				return 0

			elif arg == '--version':
				print('codebuilder-1.0')
				return 0

			elif arg == '-v' or arg == '--verbose':
				ctx.verbose = True

			elif arg == '-l' or arg == '--language':
				flag = 1

			elif arg == '-p' or arg == '--profiles':
				flag = 2

			else:
				if arg[0] != '-':
					args.append(arg)
				else:
					print('Usage: %s [options] [filename]' % argv[0])
					print('')
					print('Options:')
					print('  -h, --help          show this help message and exit')
					print('  --authors           show authors')
					print('  --version           show version')
					print('  -v --verbose        set this program verbose')
					print('')
					print('  -l --language LANG  ')
					print('  -p --profiles LIST  ')

					return 1

	#####################################################################

	try:
		module = 'cb.lang.%s' % ctx.language

		##################
		__import__(module)
		##################

		ctx.lang = sys.modules[module]

	except ImportError, e:
		cb.utils.fatal(ctx, 'Could not load \'%s\' !' % module)

	#####################################################################

	ctx.primitives = ctx.lang.PRIMITIVES
	ctx.qualifiers = ctx.lang.QUALIFIERS

	#####################################################################

	list = [
		'CodeBuilder.xml',
	]

	if   len(args) == 0:
		fileName = os.path.normcase(list[0])
	elif len(args) == 1:
		fileName = os.path.normcase(args[0])
	else:
		cb.utils.fatal(ctx, 'Syntax error !')

	#####################################################################

	ctx.parse(fileName)

	ctx.check()

	ctx.emit()

#############################################################################

if __name__ == '__main__':
	sys.exit(entry_point(sys.argv))

#############################################################################


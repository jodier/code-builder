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

def codebuilder_load_xml(ctx, fileName):
	#####################################################################

	if ctx.verbose:
		print('Loading \'%s\'...' % fileName)

	#####################################################################

	try:
		doc = xml.dom.minidom.parse(fileName)

		includes = doc.getElementsByTagName('include')

		if len(includes) > 0:

			dirName = os.path.dirname(fileName)

			if len(dirName) == 0:
				dirName = '.'

			for include in includes:

				url = include.getStripedAttribute('url')

				if url[0] != os.sep:
					url = dirName + os.sep + url

				#############################################

				subdoc = codebuilder_load_xml(ctx, url)

				for node in subdoc.documentElement.childNodes:
					include.parentNode.appendChild(node.cloneNode(1))

				#############################################

	except:
		cb.utils.fatal(ctx, 'XML error in file `%s`, %s !' % (fileName, sys.exc_info()[1]))

	return doc

#############################################################################
import cb.lang.c
#############################################################################

class codebuilder:
	#####################################################################

	def __init__(self):
		self.lang = None

		#############################################################
		# INTERFACE						    #
		#############################################################

		self.name = 'noname'

		self.major = 0
		self.minor = 0

		self.int_asset = {}
		self.int_types = []
		self.int_profiles = []
		self.int_extensions = []
		self.int_constraints = []

		#############################################################
		# IMPLEMENTATION					    #
		#############################################################

		self.imp_extras = []
		self.imp_ctors = []
		self.imp_dtors = []
		self.imp_profiles = {}

		#############################################################

		self.verbose = False

		self.intext = ''
		self.impext = ''

		self.language = 'c'
		self.profiles = '*'

		self.debug = 0
		self.ooops = 0
		self.error = 0

		self.cnt = 0x10000

	#####################################################################

	def parse(self, fileName):
		doc = codebuilder_load_xml(self, fileName)

		cb.parse.parseInterface(self,
			doc.getElementsByTagName('interface')
		)

		cb.parse.parseImplementation(self,
			doc.getElementsByTagName('implementation')
		)

	#####################################################################

	def check(self):
		cb.check.interface(self)
		cb.check.implementation(self)

		cb.utils.status(self)

	#####################################################################

	def emit(self):
		cb.emit.interface(self)
		cb.emit.implementation(self)
		pass

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

		elif flag == 2:
			ctx.profiles = arg

		elif flag == 3:
			ctx.intext = arg

		elif flag == 4:
			ctx.impext = arg

		else:
			flag = 0

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

			elif arg == '--intext':
				flag = 3

			elif arg == '--impext':
				flag = 4

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
					print('')
					print('  --intext EXT        ')
					print('  --impext EXT        ')

					return 1

	#####################################################################

	ctx.lang = cb.lang.c

	#####################################################################

	if len(ctx.intext) == 0:
		ctx.intext = ctx.lang.INT_EXT

	if len(ctx.impext) == 0:
		ctx.impext = ctx.lang.IMP_EXT

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

	#####################################################################

	ctx.check()

	if ctx.error == 0:

		ctx.emit()

	#####################################################################

	return 0

#############################################################################

def target(*args):
	return entry_point, None
    
if __name__ == '__main__':
	entry_point(sys.argv)

#############################################################################


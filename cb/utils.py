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

import os, sys, glob

#############################################################################
# PATHS									    #
#############################################################################

def buildPaths(pwd, s):
	s = os.path.normpath(s)

	if not s[0] in ['\\', '/']:
		s = os.path.join(pwd, s)

	return [os.path.normpath(f).replace('\\', '/') for f in glob.iglob(s)]

#############################################################################
# TREES									    #
#############################################################################

def myprint(s, shift):

	for i in xrange(shift):
		sys.stdout.write(' ')

	print(s)

#############################################################################

def displayTree(T, level = 0):

		if   type(T).__name__ == 'list':

			for item in enumerate(T):

				myprint('idx: %d' % item[0], level)

				displayTree(item[1], level + 4)

		elif type(T).__name__ == 'dict':

			for item in T.iteritems():

				myprint('key: %s' % item[0], level)

				displayTree(item[1], level + 4)

		else:
			myprint(T, level)

#############################################################################

def getExtension(ctx, name):
	INT_EXTENSIONS = ctx['int_extensions']

	for e in INT_EXTENSIONS:

		if e['name'] == name:
			return e

	return None

#############################################################################

def getMethod(ext, name):
	INT_METHODS = ext['methods']

	for m in INT_METHODS:

		if m['name'] == name:
			return m

	return None

#############################################################################
# MESSAGES								    #
#############################################################################

def debug(ctx, msg):
	print('[Debug] %s' % msg)
	ctx['debug'] += 1

#############################################################################

def ooops(ctx, msg):
	print('[Ooops] %s' % msg)
	ctx['ooops'] += 1

#############################################################################

def error(ctx, msg):
	print('[Error] %s' % msg)
	ctx['error'] += 1

#############################################################################

def fatal(ctx, msg):
	print('[Fatal] %s' % msg)
	sys.exit(1)

#############################################################################

def status(ctx):
	if ctx['debug'] > 0\
	   or		   \
	   ctx['ooops'] > 0\
	   or		   \
	   ctx['error'] > 0:

		print('')

		if ctx['debug'] > 0:
			print('There are %d \'debug\' messages !' % ctx['debug'])

		if ctx['ooops'] > 0:
			print('There are %d \'ooops\' messages !' % ctx['ooops'])

		if ctx['error'] > 0:
			print('There are %d \'error\' messages !' % ctx['error'])

#############################################################################

def getCnt(ctx):
	ctx['cnt'] += 1

	return ctx['cnt']

#############################################################################


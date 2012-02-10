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

import os, re, sys

#############################################################################

try:
	import xml.dom.minidom

except ImportError, e:
	cb.utils.fatal(e)

#############################################################################
# XML									    #
#############################################################################

def getStripedAttribute(self, name):
	return self.getAttribute(name).strip()

xml.dom.minidom.Element.getStripedAttribute = \
					getStripedAttribute

#############################################################################

def getStripedLAttribute(self, name):
	return self.getAttribute(name).strip().lower()

xml.dom.minidom.Element.getStripedLAttribute = \
					getStripedLAttribute

#############################################################################

def getStripedUAttribute(self, name):
	return self.getAttribute(name).strip().upper()

xml.dom.minidom.Element.getStripedUAttribute = \
					getStripedUAttribute

#############################################################################
# PROFILES								    #
#############################################################################

def selectedProfiles(ctx):
	L = None

	if not ctx['options'].profiles is None:
		L = re.split('\W+', ctx['options'].profiles)

	return L

#############################################################################
# TREES									    #
#############################################################################

def myprint(s, shift):

	for i in xrange(shift):
		sys.stdout.write(' ')

	print(s)

#############################################################################

def displayTree(T, level = 0):
	#####################################################################
	# LISTS								    #
	#####################################################################

	if   type(T).__name__ == 'list':

		for item in enumerate(T):

			myprint('idx: %d' % item[0], level)

			displayTree(item[1], level + 4)

	#####################################################################
	# DICTS								    #
	#####################################################################

	elif type(T).__name__ == 'dict':

		for item in T.iteritems():

			myprint('key: %s' % item[0], level)

			displayTree(item[1], level + 4)

	#####################################################################
	# LEAFS								    #
	#####################################################################

	else:
		myprint(T, level)

#############################################################################

def int_getProfile(ctx, name):
	INT_PROFILES = ctx['int_profiles']

	for p in INT_PROFILES:

		if p['name'] == name:
			return p

	return None

#############################################################################

def int_getExtension(ctx, name):
	INT_EXTENSIONS = ctx['int_extensions']

	for e in INT_EXTENSIONS:

		if e['name'] == name:
			return e

	return None

#############################################################################

def int_getMethod(ext, name):
	INT_METHODS = ext['methods']

	for m in INT_METHODS:

		if m['name'] == name:
			return m

	return None

#############################################################################
# TYPES									    #
#############################################################################

def extractTypes(ctx, s):
	L = []

	for word in re.split('\W+', s):

		if len(word) > 0 and not word in ctx['lang'].QUALIFIERS:

			if word[0] < '0'\
			   or		\
			   word[0] > '9':
				L.append(word)

	return L

#############################################################################
# IO									    #
#############################################################################

def writef(fp, s):
	fp.write(s)

#############################################################################

def printf(fp, s):
	fp.write(s + '\n')

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
# COUNTER								    #
#############################################################################

def getCnt(ctx):
	ctx['cnt'] += 1

	return ctx['cnt']

#############################################################################


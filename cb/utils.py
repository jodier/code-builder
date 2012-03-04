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

import os, re, sys, xml.dom.minidom

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

def getTEXTs(self):
	L = []

	for node in self.childNodes:

		if node.nodeType == 3:
			L.append(node.nodeValue.lstrip('\r\n').rstrip(' \t\r\n'))

	return L

xml.dom.minidom.Element.getTEXTs = \
				getTEXTs

#############################################################################

def getCDATAs(self):
	L = []

	for node in self.childNodes:

		if node.nodeType == 4:
			L.append(node.nodeValue.lstrip('\r\n').rstrip(' \t\r\n'))

	return L

xml.dom.minidom.Element.getCDATAs = \
				getCDATAs

#############################################################################
# PROFILES								    #
#############################################################################

class context:
	#####################################################################

	def __init__(self, name = 'noname', major = 0, minor = 0, verbose = False, primitives = '', qualifiers = '', language = 'c', profiles = '*'):

		self.lang = None

		#############################################################
		# PUBLIC INTERFACE					    #
		#############################################################

		self.name = name

		self.major = major
		self.minor = minor

		self.int_pub_asset = {}
		self.int_pub_prologs = []
		self.int_pub_epilogs = []
		self.int_pub_types = []
		self.int_pub_profiles = []
		self.int_pub_extensions = []

		#############################################################
		# PRIVATE INTERFACE					    #
		#############################################################

		self.int_priv_prologs = []
		self.int_priv_epilogs = []
		self.int_priv_types = []
		self.int_priv_constraints = []

		#############################################################
		# IMPLEMENTATION					    #
		#############################################################

		self.imp_extras = []
		self.imp_ctors = []
		self.imp_dtors = []
		self.imp_profiles = {}

		#############################################################
		# OTHER							    #
		#############################################################

		self.verbose = verbose

		self.primitives = primitives
		self.qualifiers = qualifiers

		self.language = language
		self.profiles = profiles

		self.debug = 0
		self.ooops = 0
		self.error = 0

		self.cnt = 0x10000

#############################################################################
# PROFILES								    #
#############################################################################

def selectedProfiles(ctx):
	L = None

	if ctx.profiles != '*':
		L = re.split('\W+', ctx.profiles)

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
	INT_PROFILES = ctx.int_pub_profiles

	for p_node in INT_PROFILES:

		if p_node['name'] == name:
			return p_node

	return None

#############################################################################

def int_getExtension(ctx, name):
	INT_EXTENSIONS = ctx.int_pub_extensions

	for e_node in INT_EXTENSIONS:

		if e_node['name'] == name:
			return e_node

	return None

#############################################################################

def int_getMethod(ext, name):
	INT_METHODS = ext['methods']

	for m_node in INT_METHODS:

		if m_node['name'] == name:
			return m_node

	return None

#############################################################################
# TYPES									    #
#############################################################################

def extractTypes(ctx, s):
	L = []

	for word in re.split('\W+', re.sub('\[[^\]]*\]', '', s)):

		if len(word) > 0 and not word in ctx.qualifiers:

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
	ctx.debug += 1

#############################################################################

def ooops(ctx, msg):
	print('[Ooops] %s' % msg)
	ctx.ooops += 1

#############################################################################

def error(ctx, msg):
	print('[Error] %s' % msg)
	ctx.error += 1

#############################################################################

def fatal(ctx, msg):
	print('[Fatal] %s' % msg)
	sys.exit(1)

#############################################################################

def status(ctx):
	if ctx.debug > 0\
	   or		\
	   ctx.ooops > 0\
	   or		\
	   ctx.error > 0:

		print('')

		if ctx.debug > 0:
			print('There are %d \'debug\' messages !' % ctx.debug)

		if ctx.ooops > 0:
			print('There are %d \'ooops\' messages !' % ctx.ooops)

		if ctx.error > 0:
			print('There are %d \'error\' messages !' % ctx.error)

#############################################################################
# COUNTER								    #
#############################################################################

def getCnt(ctx):
	result = ctx.cnt
	ctx.cnt += 1
	return result

#############################################################################


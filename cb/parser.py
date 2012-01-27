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

try:
	import xml.dom.minidom

except ImportError, e:
	cb.utils.fatal(e)

#############################################################################
# UTILS									    #
#############################################################################

def __getTEXTs(self):
	L = []

	for textensionNode in self.childNodes:
		if textensionNode.nodeType == 3:
			L.append(textensionNode.nodeValue)

	return L

#############################################################################

xml.dom.minidom.Element.getTEXTs = __getTEXTs

#############################################################################

def __getCDATAs(self):
	L = []

	for textensionNode in self.childNodes:
		if textensionNode.nodeType == 4:
			L.append(textensionNode.nodeValue)

	return L

#############################################################################

xml.dom.minidom.Element.getCDATAs = __getCDATAs

#############################################################################
# PARSERS								    #
#############################################################################

def parseInterface(ctx, interfaces):
	#####################################################################

	if len(interfaces) != 1:
		if len(interfaces) > 1:
			cb.utils.error('Only one interface allowed !')

		return

	interface = interfaces[0]

	#####################################################################

	date = ''
	authors = ''
	emails = ''
	description = ''

	#####################################################################

	for node in interface.childNodes:

		#############################################################
		# ASSET							    #
		#############################################################

		if node.nodeName == 'asset':

			for assetNode in node.childNodes:

				if assetNode.nodeName == 'date':
					date = assetNode.getTEXTs()[0]
				if assetNode.nodeName == 'authors':
					authors = assetNode.getTEXTs()[0]
				if assetNode.nodeName == 'emails':
					emails = assetNode.getTEXTs()[0]
				if assetNode.nodeName == 'description':
					description = assetNode.getTEXTs()[0]

		#############################################################
		# TYPES							    #
		#############################################################

		if node.nodeName == 'types':

			TYPE = {}
			ENUM = {}
			STRUCT = {}

			for typeNode in node.childNodes:

				#############################################
				# TYPE					    #
				#############################################

				if typeNode.nodeName == 'type':

					dic = {
						'from': typeNode.getAttribute('from')
					}

					TYPE[typeNode.getAttribute('name')] = dic

				#############################################
				# ENUM					    #
				#############################################

				if typeNode.nodeName == 'enum':

					VALUES = []

					for valueNode in typeNode.childNodes:

						#############################
						# VALUE			    #
						#############################

						if valueNode.nodeName == 'value':

							dic = {
								'name': valueNode.getAttribute('name'),
								'init': valueNode.getAttribute('init'),
							}

							VALUES.append(dic)

					dic = {
						'values': VALUES
					}

					ENUM[typeNode.getAttribute('name')] = dic


				#############################################
				# STRUCT				    #
				#############################################

				if typeNode.nodeName == 'struct':

					FIELDS = []

					for fieldNode in typeNode.childNodes:

						#############################
						# FIELD			    #
						#############################

						if fieldNode.nodeName == 'field':

							dic = {
								'name': fieldNode.getAttribute('name'),
								'type': fieldNode.getAttribute('type'),
							}

							FIELDS.append(dic)

					dic = {
						'fields': FIELDS
					}

					STRUCT[typeNode.getAttribute('name')] = dic

			#####################################################

			ctx['int_types']['types'] = TYPE
			ctx['int_types']['enums'] = ENUM
			ctx['int_types']['structs'] = STRUCT

		#############################################################
		# PROFILES						    #
		#############################################################

		if node.nodeName == 'profiles':

			for profileNode in node.childNodes:

				#############################################

				if profileNode.nodeName == 'profile':

					dic = {
					}

					ctx['int_profiles'][profileNode.getAttribute('name')] = dic

		#############################################################
		# EXTENSIONS						    #
		#############################################################

		if node.nodeName == 'extensions':

			for extensionNode in node.childNodes:

				#############################################
				# EXTENSION				    #
				#############################################

				if extensionNode.nodeName == 'extension':

					METHODS = []

					for methodNode in extensionNode.childNodes:

						#############################
						# METHOD		    #
						#############################

						if methodNode.nodeName == 'method':

							PARAMS = []

							for paramNode in methodNode.childNodes:

								#############
								# PARAM	    #
								#############

								if paramNode.nodeName == 'param':

									dic = {
										'name': paramNode.getAttribute('name'),
										'type': paramNode.getAttribute('type'),
									}

									PARAMS.append(dic)

							dic = {
								'name': methodNode.getAttribute('name'),
								'type': methodNode.getAttribute('type'),
								'params': PARAMS
							}

							METHODS.append(dic)

					dic = {
						'name': extensionNode.getAttribute('name'),
					#	'type': extensionNode.getAttribute('type'),
						'methods': METHODS
					}

					ctx['int_extensions'].append(dic)

		#############################################################
		# CONSTRAINTS						    #
		#############################################################

		if node.nodeName == 'constraints':

			for constraintNode in node.childNodes:

				#############################################
				# CONSTRAINT				    #
				#############################################

				if constraintNode.nodeName == 'constraint':

					KEYS = {}

					for keyNode in constraintNode.childNodes:

						#############################
						# KEY			    #
						#############################

						if keyNode.nodeName == 'key':

							dic = {
							}

							KEYS[keyNode.getAttribute('name')] = dic

					dic = {
						'keys': KEYS
					}

					ctx['int_constraints'][constraintNode.getAttribute('name')] = dic

	#####################################################################

	ctx['int_name'] = interface.getAttribute('name')
	ctx['int_major'] = int(interface.getAttribute('major'))
	ctx['int_minor'] = int(interface.getAttribute('minor'))

	#####################################################################

	ctx['int_asset']['date'] = date
	ctx['int_asset']['authors'] = authors
	ctx['int_asset']['emails'] = emails
	ctx['int_asset']['description'] = description

	#####################################################################

	if ctx['options'].verbose:
		displayInterface(ctx)

#############################################################################

def parseCode(node):
	#####################################################################

	CODES = []

	#####################################################################

	for codeNode in node.childNodes:

		#############################################################
		# CODE							    #
		#############################################################

		if codeNode.nodeName == 'code':

			dic = {
				'condition': codeNode.getAttribute('condition'),
				'txts': codeNode.getCDATAs()
			}

			CODES.append(dic)

	return CODES

#############################################################################

def parseImplementation(ctx, implementations):
	#####################################################################

	if len(implementations) != 1:
		if len(implementations) > 1:
			cb.utils.error('Only one implementation allowed !')

		return

	implementation = implementations[0]

	#####################################################################

	for node in implementation.childNodes:

		#############################################################
		# EXTRA							    #
		#############################################################

		if node.nodeName == 'extra':
			ctx['imp_extras'].append(parseCode(node))

		#############################################################
		# INIT							    #
		#############################################################

		if node.nodeName == 'init':
			ctx['imp_inits'].append(parseCode(node))

		#############################################################
		# PROFILES						    #
		#############################################################

		if node.nodeName == 'profiles':

			for profileNode in node.childNodes:

				#############################################
				# PROFILE				    #
				#############################################

				if profileNode.nodeName == 'profile':

					EXTRAS1 = []
					INITS1 = []
					EXTENSIONS = {}

					for itemNode1 in profileNode.childNodes:

						#############################
						# EXTRA			    #
						#############################

						if itemNode1.nodeName == 'extra':
							EXTRAS1.append(parseCode(itemNode1))

						#############################
						# INIT			    #
						#############################

						if itemNode1.nodeName == 'init':
							INITS1.append(parseCode(itemNode1))

						#############################
						# EXTENSIONS		    #
						#############################

						if itemNode1.nodeName == 'extensions':

							for extensionNode in itemNode1.childNodes:

								#############
								# EXTENSION #
								#############

								if extensionNode.nodeName == 'extension':

									EXTRAS2 = []
									INITS2 = []
									METHODS = {}

									for itemNode2 in extensionNode.childNodes:

										#############
										# EXTRA	    #
										#############

										if itemNode2.nodeName == 'extra':
											EXTRAS2.append(parseCode(itemNode2))

										#############
										# INIT	    #
										#############

										if itemNode2.nodeName == 'init':
											INITS2.append(parseCode(itemNode2))

										#############
										# METHOD    #
										#############

										if itemNode2.nodeName == 'method':
											METHODS[itemNode2.getAttribute('name')] = parseCode(itemNode2)

									dic = {
										'extras': EXTRAS2,
										'inits': INITS2,
										'methods': METHODS,
									}

									EXTENSIONS[extensionNode.getAttribute('name')] = dic

					dic = {
						'extras': EXTRAS1,
						'inits': INITS1,
						'extensions': EXTENSIONS,
					}

					ctx['imp_profiles'][profileNode.getAttribute('name')] = dic

	#####################################################################

	if ctx['options'].verbose:
		displayImplementation(ctx)

#############################################################################

def displayInterface(ctx):
	print('-----------------------------------------------------------------------------')
	print('| ASSET                                                                     |')
	print('-----------------------------------------------------------------------------')
	cb.utils.displayTree(ctx['int_asset'])
	print('-----------------------------------------------------------------------------')
	print('| TYPES                                                                     |')
	print('-----------------------------------------------------------------------------')
	cb.utils.displayTree(ctx['int_types'])
	print('-----------------------------------------------------------------------------')
	print('| PROFILES                                                                  |')
	print('-----------------------------------------------------------------------------')
	cb.utils.displayTree(ctx['int_profiles'])
	print('-----------------------------------------------------------------------------')
	print('| CONSTRAINTS                                                               |')
	print('-----------------------------------------------------------------------------')
	cb.utils.displayTree(ctx['int_constraints'])
	print('-----------------------------------------------------------------------------')
	print('| EXTENSIONS                                                                |')
	print('-----------------------------------------------------------------------------')
	cb.utils.displayTree(ctx['int_extensions'])
	print('-----------------------------------------------------------------------------')
	print('')


#############################################################################

def displayImplementation(ctx):
	print('-----------------------------------------------------------------------------')
	print('| EXTRAS                                                                    |')
	print('-----------------------------------------------------------------------------')
	cb.utils.displayTree(ctx['imp_extras'])
	print('-----------------------------------------------------------------------------')
	print('| INITS                                                                     |')
	print('-----------------------------------------------------------------------------')
	cb.utils.displayTree(ctx['imp_inits'])
	print('-----------------------------------------------------------------------------')
	print('| PROFILES                                                                  |')
	print('-----------------------------------------------------------------------------')
	cb.utils.displayTree(ctx['imp_profiles'])
	print('-----------------------------------------------------------------------------')
	print('')

#############################################################################


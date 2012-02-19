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

import cb.utils, xml.dom.minidom

#############################################################################
# UTILS									    #
#############################################################################

def __getTEXTs(self):
	L = []

	for node in self.childNodes:
		if node.nodeType == 3:
			L.append(node.nodeValue)

	return L

#############################################################################

xml.dom.minidom.Element.getTEXTs = __getTEXTs

#############################################################################

def __getCDATAs(self):
	L = []

	for node in self.childNodes:
		if node.nodeType == 4:
			L.append(node.nodeValue)

	return L

#############################################################################

xml.dom.minidom.Element.getCDATAs = __getCDATAs

#############################################################################
# PARSERS								    #
#############################################################################

def parseType(node):
	#####################################################################

	TYPES = []

	#####################################################################

	for typeNode in node.childNodes:

		#############################################
		# TYPE					    #
		#############################################

		if typeNode.nodeName == 'type':

			dic = {
				'class': 'base',
				'name': typeNode.getStripedAttribute('name'),
				'from': typeNode.getStripedAttribute('from'),
			}

			TYPES.append(dic)

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
						'name': valueNode.getStripedAttribute('name'),
						'init': valueNode.getStripedAttribute('init'),
					}

					VALUES.append(dic)

			dic = {
				'class': 'enum',
				'name': typeNode.getStripedAttribute('name'),
				'values': VALUES
			}

			TYPES.append(dic)

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
						'name': fieldNode.getStripedAttribute('name'),
						'type': fieldNode.getStripedAttribute('type'),
					}

					FIELDS.append(dic)

			dic = {
				'class': 'struct',
				'name': typeNode.getStripedAttribute('name'),
				'fields': FIELDS
			}

			TYPES.append(dic)

		#############################################
		# PRIMITIVE				    #
		#############################################

		if typeNode.nodeName == 'primitive':

			name = typeNode.\
				getStripedAttribute('name')

			if len(name) > 0:
				ctx.primitives.add(name)

		#############################################
		# QUALIFIER				    #
		#############################################

		if typeNode.nodeName == 'qualifier':

			name = typeNode.\
				getStripedAttribute('name')

			if len(name) > 0:
				ctx.qualifiers.add(name)

	return TYPES

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
				'condition': codeNode.getStripedAttribute('condition'),
				'txts': codeNode.getCDATAs()
			}

			CODES.append(dic)

	return CODES

#############################################################################

def parseInterfacePublic(ctx, interfaces):
	#####################################################################

	if len(interfaces) == 0:
		cb.utils.error(ctx, 'No public interface defined !')

		return

	if len(interfaces) != 1:
		cb.utils.error(ctx, 'Only one public interface allowed, \'%d\' found !' % len(interfaces))

		return

	interface = interfaces[0]

	#####################################################################

	SELECTED_PROFILES = cb.utils.selectedProfiles(ctx)

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
					date = assetNode.getTEXTs()[0].strip()
				if assetNode.nodeName == 'authors':
					authors = assetNode.getTEXTs()[0].strip()
				if assetNode.nodeName == 'emails':
					emails = assetNode.getTEXTs()[0].strip()
				if assetNode.nodeName == 'description':
					description = assetNode.getTEXTs()[0].strip()

		#############################################################
		# PROLOG						    #
		#############################################################

		if node.nodeName == 'prolog':
			ctx.int_pub_prologs.append(parseCode(node))

		#############################################################
		# EPILOG						    #
		#############################################################

		if node.nodeName == 'epilog':
			ctx.int_pub_epilogs.append(parseCode(node))

		#############################################################
		# TYPES							    #
		#############################################################

		if node.nodeName == 'types':
			ctx.int_pub_types.extend(parseType(node))

		#############################################################
		# PROFILES						    #
		#############################################################

		if node.nodeName == 'profiles':

			for profileNode in node.childNodes:

				#############################################

				if profileNode.nodeName == 'profile':

					dic = {
						'name': profileNode.getStripedAttribute('name')
					}

					if SELECTED_PROFILES is None\
					   or			    \
					   profileNode.getStripedAttribute('name') in SELECTED_PROFILES:

						ctx.int_pub_profiles.append(dic)

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
										'name': paramNode.getStripedAttribute('name'),
										'type': paramNode.getStripedAttribute('type'),
									}

									PARAMS.append(dic)

							dic = {
								'name': methodNode.getStripedAttribute('name'),
								'type': methodNode.getStripedAttribute('type'),
								'params': PARAMS
							}

							METHODS.append(dic)

					dic = {
						'name': extensionNode.getStripedAttribute('name'),
					#	'type': extensionNode.getStripedAttribute('type'),
						'methods': METHODS
					}

					ctx.int_pub_extensions.append(dic)

		#############################################################
		# CONSTRAINTS						    #
		#############################################################

		if node.nodeName == 'constraints':

			for constraintNode in node.childNodes:

				#############################################
				# CONSTRAINT				    #
				#############################################

				if constraintNode.nodeName == 'constraint':

					KEYS = []

					for keyNode in constraintNode.childNodes:

						#############################
						# KEY			    #
						#############################

						if keyNode.nodeName == 'key':

							dic = {
								'name': keyNode.getStripedAttribute('name')
							}

							KEYS.append(dic)

					dic = {
						'name': constraintNode.getStripedAttribute('name'),
						'keys': KEYS,
					}

					ctx.int_pub_constraints.append(dic)

	#####################################################################

	ctx.name = interface.getStripedAttribute('name')
	ctx.major = int(interface.getStripedAttribute('major'))
	ctx.minor = int(interface.getStripedAttribute('minor'))

	#####################################################################

	ctx.int_pub_asset['date'] = date
	ctx.int_pub_asset['authors'] = authors
	ctx.int_pub_asset['emails'] = emails
	ctx.int_pub_asset['description'] = description

	#####################################################################

	if ctx.verbose:
		displayInterfacePublic(ctx)

#############################################################################

def parseInterfacePrivate(ctx, interfaces):
	#####################################################################

	if len(interfaces) == 0:
		cb.utils.debug(ctx, 'No private interface defined !')

		return

	if len(interfaces) != 1:
		cb.utils.error(ctx, 'Only one private interface allowed, \'%d\' found !' % len(interfaces))

		return

	interface = interfaces[0]

	#####################################################################

	for node in interface.childNodes:

		#############################################################
		# PROLOG						    #
		#############################################################

		if node.nodeName == 'prolog':
			ctx.int_priv_prologs.append(parseCode(node))

		#############################################################
		# EPILOG						    #
		#############################################################

		if node.nodeName == 'epilog':
			ctx.int_priv_epilogs.append(parseCode(node))

		#############################################################
		# TYPES							    #
		#############################################################

		if node.nodeName == 'types':
			ctx.int_priv_types.extend(parseType(node))

	#####################################################################

	if ctx.verbose:
		displayInterfacePrivate(ctx)

#############################################################################

def parseImplementation(ctx, implementations):
	#####################################################################

	if len(implementations) == 0:
		cb.utils.error(ctx, 'No implementation defined !')

		return

	if len(implementations) != 1:
		cb.utils.error(ctx, 'Only one implementation allowed, \'%d\' found !' % len(implementations))

		return

	implementation = implementations[0]

	#####################################################################

	SELECTED_PROFILES = cb.utils.selectedProfiles(ctx)

	#####################################################################

	for node in implementation.childNodes:

		#############################################################
		# EXTRA							    #
		#############################################################

		if node.nodeName == 'extra':
			ctx.imp_extras.append(parseCode(node))

		#############################################################
		# CTOR							    #
		#############################################################

		if node.nodeName == 'ctor':
			ctx.imp_ctors.append(parseCode(node))

		#############################################################
		# DTOR							    #
		#############################################################

		if node.nodeName == 'dtor':
			ctx.imp_dtors.append(parseCode(node))

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
					CTORS1 = []
					DTORS1 = []
					EXTENSIONS = {}

					for itemNode1 in profileNode.childNodes:

						#############################
						# EXTRA			    #
						#############################

						if itemNode1.nodeName == 'extra':
							EXTRAS1.append(parseCode(itemNode1))

						#############################
						# CTOR			    #
						#############################

						if itemNode1.nodeName == 'ctor':
							CTORS1.append(parseCode(itemNode1))

						#############################
						# DTOR			    #
						#############################

						if itemNode1.nodeName == 'dtor':
							DTORS1.append(parseCode(itemNode1))

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
									CTORS2 = []
									DTORS2 = []
									METHODS = {}

									for itemNode2 in extensionNode.childNodes:

										#############
										# EXTRA	    #
										#############

										if itemNode2.nodeName == 'extra':
											EXTRAS2.append(parseCode(itemNode2))

										#############
										# CTOR	    #
										#############

										if itemNode2.nodeName == 'ctor':
											CTORS2.append(parseCode(itemNode2))

										#############
										# DTOR	    #
										#############

										if itemNode2.nodeName == 'dtor':
											DTORS2.append(parseCode(itemNode2))

										#############
										# METHOD    #
										#############

										if itemNode2.nodeName == 'method':
											METHODS[itemNode2.getStripedAttribute('name')] = parseCode(itemNode2)

									dic = {
										'extras': EXTRAS2,
										'ctors': CTORS2,
										'dtors': DTORS2,
										'methods': METHODS,
									}

									EXTENSIONS[extensionNode.getStripedAttribute('name')] = dic

					dic = {
						'extras': EXTRAS1,
						'ctors': CTORS1,
						'dtors': DTORS1,
						'extensions': EXTENSIONS,
					}

					if SELECTED_PROFILES is None\
					   or			    \
					   profileNode.getStripedAttribute('name') in SELECTED_PROFILES:

						ctx.imp_profiles[profileNode.getStripedAttribute('name')] = dic

	#####################################################################

	if ctx.verbose:
		displayImplementation(ctx)

#############################################################################

def displayInterfacePublic(ctx):
	print('-----------------------------------------------------------------------------')
	print('| ASSET                                                                     |')
	print('-----------------------------------------------------------------------------')
	cb.utils.displayTree(ctx.int_pub_asset)
	print('-----------------------------------------------------------------------------')
	print('| PROLOGS                                                                   |')
	print('-----------------------------------------------------------------------------')
	cb.utils.displayTree(ctx.int_pub_prologs)
	print('-----------------------------------------------------------------------------')
	print('| EPILOGS                                                                   |')
	print('-----------------------------------------------------------------------------')
	cb.utils.displayTree(ctx.int_pub_epilogs)
	print('-----------------------------------------------------------------------------')
	print('| TYPES                                                                     |')
	print('-----------------------------------------------------------------------------')
	cb.utils.displayTree(ctx.int_pub_types)
	print('-----------------------------------------------------------------------------')
	print('| PROFILES                                                                  |')
	print('-----------------------------------------------------------------------------')
	cb.utils.displayTree(ctx.int_pub_profiles)
	print('-----------------------------------------------------------------------------')
	print('| CONSTRAINTS                                                               |')
	print('-----------------------------------------------------------------------------')
	cb.utils.displayTree(ctx.int_pub_constraints)
	print('-----------------------------------------------------------------------------')
	print('| EXTENSIONS                                                                |')
	print('-----------------------------------------------------------------------------')
	cb.utils.displayTree(ctx.int_pub_extensions)
	print('-----------------------------------------------------------------------------')
	print('')

#############################################################################

def displayInterfacePrivate(ctx):
	print('-----------------------------------------------------------------------------')
	print('| PROLOGS                                                                   |')
	print('-----------------------------------------------------------------------------')
	cb.utils.displayTree(ctx.int_priv_prologs)
	print('-----------------------------------------------------------------------------')
	print('| EPILOGS                                                                   |')
	print('-----------------------------------------------------------------------------')
	cb.utils.displayTree(ctx.int_priv_epilogs)
	print('-----------------------------------------------------------------------------')
	print('| TYPES                                                                     |')
	print('-----------------------------------------------------------------------------')
	cb.utils.displayTree(ctx.int_priv_types)
	print('-----------------------------------------------------------------------------')
	print('')

#############################################################################

def displayImplementation(ctx):
	print('-----------------------------------------------------------------------------')
	print('| EXTRAS                                                                    |')
	print('-----------------------------------------------------------------------------')
	cb.utils.displayTree(ctx.imp_extras)
	print('-----------------------------------------------------------------------------')
	print('| CTORS                                                                     |')
	print('-----------------------------------------------------------------------------')
	cb.utils.displayTree(ctx.imp_ctors)
	print('-----------------------------------------------------------------------------')
	print('| DTORS                                                                     |')
	print('-----------------------------------------------------------------------------')
	cb.utils.displayTree(ctx.imp_dtors)
	print('-----------------------------------------------------------------------------')
	print('| PROFILES                                                                  |')
	print('-----------------------------------------------------------------------------')
	cb.utils.displayTree(ctx.imp_profiles)
	print('-----------------------------------------------------------------------------')
	print('')

#############################################################################


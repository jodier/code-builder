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

def checkTypes(ctx, TYPES):
	#####################################################################
	# PASS ONE							    #
	#####################################################################

	for t_node in TYPES:

		if t_node['name'] in ctx.primitives:
			cb.utils.error(ctx, 'Duplicated type \'%s\' !' % t_node['name'])
		else:
			ctx.primitives.add(t_node['name'])

	#####################################################################
	# PASS TWO							    #
	#####################################################################

	for t_node in TYPES:
		#############################################################
		# BASE TYPE						    #
		#############################################################

		if t_node['class'] == 'base':

			for t_name in cb.utils.extractTypes(ctx, t_node['from']):

				if t_name in ctx.primitives:

					if t_name == t_node['name']:
						cb.utils.error(ctx, 'Recursif type \'%s\' !' % t_name)

				else:
					cb.utils.error(ctx, 'Undefined type \'%s\' !' % t_name)

		#############################################################
		# ENUM TYPE						    #
		#############################################################

		if t_node['class'] == 'enum':

			values = t_node['values']

			for i in xrange(0 + 0, len(values)):
				for j in xrange(i + 1, len(values)):

					if values[i]['name'] == values[j]['name']:
						cb.utils.error(ctx, 'Duplicated values \'%s\' for type \'%s\' !' % (values[i]['name'], t_node['name']))

		#############################################################
		# STRUCT TYPE						    #
		#############################################################

		if t_node['class'] == 'struct':

			fields = t_node['fields']

			for i in xrange(0 + 0, len(fields)):
				for j in xrange(i + 1, len(fields)):

					if fields[i]['name'] == fields[j]['name']:
						cb.utils.error(ctx, 'Duplicated fields \'%s\' for type \'%s\' !' % (fields[i]['name'], t_node['name']))

			##

			for f_node in fields:

				for t_name in cb.utils.extractTypes(ctx, f_node['type']):

					if t_name in ctx.primitives:

						if t_name == t_node['name']:
							cb.utils.debug(ctx, 'Recursif type \'%s\' !' % t_name)

					else:
						cb.utils.error(ctx, 'Undefined type \'%s\' !' % t_name)

#############################################################################

def checkInterfacePublic(ctx):
	#####################################################################
	# TYPES								    #
	#####################################################################

	checkTypes(ctx, ctx.int_pub_types)

	#####################################################################
	# EXTENSIONS							    #
	#####################################################################

	INT_EXTENSIONS = ctx.int_pub_extensions

	#####################################################################

	for e_node in INT_EXTENSIONS:

		for m_node in e_node['methods']:

			for p_node in m_node['params']:

				for t_name in cb.utils.extractTypes(ctx, p_node['type']):

					if not t_name in ctx.primitives:
						cb.utils.error(ctx, 'Undefined type \'%s\' !' % t_name)

			##

			params = m_node['params']

			for i in xrange(0 + 0, len(params)):
				for j in xrange(i + 1, len(params)):

					if params[i]['name'] == params[j]['name']:
						cb.utils.error(ctx, 'Duplicated param \'%s\' !' % params[i]['name'])

		methods = e_node['methods']

		for i in xrange(0 + 0, len(methods)):
			for j in xrange(i + 1, len(methods)):

				if methods[i]['name'] == methods[j]['name']:
					cb.utils.error(ctx, 'Duplicated method \'%s\' !' % methods[i]['name'])

	extensions = INT_EXTENSIONS

	for i in xrange(0 + 0, len(extensions)):
		for j in xrange(i + 1, len(extensions)):

			if extensions[i]['name'] == extensions[j]['name']:
				cb.utils.error(ctx, 'Duplicated extension \'%s\' !' % extensions[i]['name'])

	#####################################################################
	# PROFILES							    #
	#####################################################################

	INT_PROFILES = ctx.int_pub_profiles

	#####################################################################

	for p_node in INT_PROFILES:

		for cp_node in p_node['ctor_params']:

			for t_node in cb.utils.extractTypes(ctx, cp_node['type']):

				if not t_node in ctx.primitives:
					cb.utils.error(ctx, 'Undefined type \'%s\' !' % t_node)

		##

		for dp_node in p_node['dtor_params']:

			for t_node in cb.utils.extractTypes(ctx, dp_node['type']):

				if not t_node in ctx.primitives:
					cb.utils.error(ctx, 'Undefined type \'%s\' !' % t_node)

		##

		ctor_params = p_node['ctor_params']

		for i in xrange(0 + 0, len(ctor_params)):
			for j in xrange(i + 1, len(ctor_params)):

				if ctor_params[i]['name'] == ctor_params[j]['name']:
					cb.utils.error(ctx, 'Duplicated ctor_param \'%s\' !' % ctor_params[i]['name'])

		##

		dtor_params = p_node['dtor_params']

		for i in xrange(0 + 0, len(dtor_params)):
			for j in xrange(i + 1, len(dtor_params)):

				if dtor_params[i]['name'] == dtor_params[j]['name']:
					cb.utils.error(ctx, 'Duplicated dtor_param \'%s\' !' % dtor_params[i]['name'])

#############################################################################

def checkInterfacePrivate(ctx):
	#####################################################################
	# TYPES								    #
	#####################################################################

	checkTypes(ctx, ctx.int_priv_types)

#############################################################################

def checkExtraXtor(ctx, EXTRAS, CTORS, DTORS):
	#####################################################################
	# EXTRAS							    #
	#####################################################################

	if len(EXTRAS) > 1:
		cb.utils.error(ctx, 'Only one extra allowed !')

	for e_node in EXTRAS:
		for c_node in e_node:

			if len(c_node['txts']) == 0:
				cb.utils.error(ctx, 'At least one CDATA node needed for extra !')

			if len(c_node['condition'].strip()) > 0:
				cb.utils.ooops(ctx, 'Only unconditional extra allowed !')

	#####################################################################
	# CTORS								    #
	#####################################################################

	if len(CTORS) > 1:
		cb.utils.error(ctx, 'Only one ctor allowed !')

	for x_node in CTORS:
		for c_node in x_node:

			if len(c_node['txts']) == 0:
				cb.utils.error(ctx, 'At least one CDATA node needed for ctor !')

	#####################################################################
	# DTORS								    #
	#####################################################################

	if len(DTORS) > 1:
		cb.utils.error(ctx, 'Only one dtor allowed !')

	for x_node in DTORS:
		for c_node in x_node:

			if len(c_node['txts']) == 0:
				cb.utils.error(ctx, 'At least one CDATA node needed for dtor !')

#############################################################################

def checkCodes(ctx, CODES):
	#####################################################################
	# CODES								    #
	#####################################################################

	for c_node in CODES:

		if len(c_node['txts']) == 0:
			cb.utils.error(ctx, 'Only one CDATA allowed for method !')

#############################################################################

def checkImplementation(ctx):
	#####################################################################
	# PROFILES							    #
	#####################################################################

	IMP_PROFILES = ctx.imp_profiles

	#####################################################################

	for p_name in IMP_PROFILES:

		PRO = cb.utils.int_getProfile(ctx, p_name)
		if PRO is None:
			cb.utils.error(ctx, 'Undefined profile \'%s\' !' % p_name)

		else:
			#####################################################
			# EXTENSIONS					    #
			#####################################################

			IMP_EXTENSIONS = IMP_PROFILES[p_name]['extensions']

			#####################################################

			for e_name in IMP_EXTENSIONS:

				EXT = cb.utils.int_getExtension(ctx, e_name)
				if EXT is None:
					cb.utils.error(ctx, 'Undefined extension \'%s\' !' % e_name)

				else:
					#####################################
					# METHODS			    #
					#####################################

					IMP_METHODS = IMP_EXTENSIONS[e_name]['methods']

					#####################################

					for m_name in IMP_METHODS:

						MET = cb.utils.int_getMethod(EXT, m_name)
						if MET is None:
							cb.utils.error(ctx, 'Undefined method \'%s\' !' % m_name)

						checkCodes(ctx,
							IMP_METHODS[m_name]
						)

				checkExtraXtor(ctx,
					IMP_EXTENSIONS[e_name]['extras'],
					IMP_EXTENSIONS[e_name]['ctors'],
					IMP_EXTENSIONS[e_name]['dtors']
				)

		checkExtraXtor(ctx,
			IMP_PROFILES[p_name]['extras'],
			IMP_PROFILES[p_name]['ctors'],
			IMP_PROFILES[p_name]['dtors']
		)

	#####################################################################

	checkExtraXtor(ctx,
		ctx.imp_extras,
		ctx.imp_ctors,
		ctx.imp_dtors
	)

#############################################################################


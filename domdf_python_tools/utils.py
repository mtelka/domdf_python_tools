#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  utils.py
"""
General Functions
"""
#
#  Copyright © 2018-2020 Dominic Davis-Foster <dominic@davis-foster.co.uk>
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU Lesser General Public License as published by
#  the Free Software Foundation; either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU Lesser General Public License for more details.
#
#  You should have received a copy of the GNU Lesser General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#
#

import sys
from collections.abc import Sequence
from domdf_python_tools.doctools import is_documented_by

pyversion = int(sys.version[0])  # Python Version


def as_text(value):
	"""
	Convert the given value to a string
	
	:param value: value to convert to a string
	:type value: any
	
	:rtype: str
	"""
	
	if value is None:
		return ""
	
	return str(value)


def str2tuple(input_string, sep=","):
	"""
	Convert a comma-separated string of integers into a tuple

	:param input_string: The string to be converted into a tuple
	:type input_string: str
	:param sep: The separator in the string, default ","
	:type sep: str

	:rtype: tuple
	"""
	
	return tuple(int(x) for x in input_string.split(sep))


def tuple2str(input_tuple, sep=","):
	"""
	Convert a tuple into a comma-separated string

	:param input_tuple: The tuple to be joined into a string
	:type input_tuple: tuple
	:param sep: The separator in the string, default ","
	:type sep: str

	:rtype: str
	"""
	
	return sep.join([str(x) for x in input_tuple])


def chunks(l, n):
	"""
	Yield successive n-sized chunks from l.

	:param l: The objects to yield chunks from
	:type l: Sequence
	:param n: The size of the chunks
	:type n: int
	"""
	
	for i in range(0, len(l), n):
		yield l[i:i + n]


def check_dependencies(dependencies, prt=True):
	"""
	
	:param dependencies:
	:param prt:
	
	:return:
	"""
	
	from pkgutil import iter_modules
	
	modules = set(x[1] for x in iter_modules())
	
	missing_modules = []
	for requirement in dependencies:
		if requirement not in modules:
			missing_modules.append(requirement)
	
	if prt:
		if len(missing_modules) == 0:
			print("All modules installed")
		else:
			print("The following modules are missing.")
			print(missing_modules)
			print("Please check the documentation.")
		print("")
	
	else:
		return missing_modules


def list2str(the_list, sep=","):
	"""
	Convert a list to a comma separated string
	
	:param the_list: The list to convert to a string
	:type the_list: list, tuple
	:param sep: Separator to use for the string, default ","
	:type sep: str
	
	:return: Comma separated string
	:rtype: str
	"""
	
	return sep.join([str(x) for x in the_list])


list2string = list2str


def split_len(string, n):
	"""
	Split a string every x characters
	
	:param string: The string to split
	:type string: str
	:param n:
	:type n: int
	
	:return: The split string
	:rtype: list
	"""
	
	return [string[i:i + n] for i in range(0, len(string), n)]


splitLen = split_len


def permutations(data, n=2):
	"""
	Return permutations containing `n` items from `data` without any reverse duplicates.
	If ``n`` is equal to or greater than the length of the data an empty list of returned
	
	:type data: list or string
	:type n: int
	
	:rtype: [tuple]
	"""
	
	import itertools
	
	if n == 0:
		raise ValueError("`n` cannot be 0")
	
	perms = []
	for i in itertools.permutations(data, n):
		"""from https://stackoverflow.com/questions/10201977/how-to-reverse-tuples-in-python"""
		if i[::-1] not in perms:
			perms.append(i)
	return perms


class bdict(dict):
	"""
	Returns a new dictionary initialized from an optional positional argument
		and a possibly empty set of keyword arguments.
	
	Each key:value pair is entered into the dictionary in both directions,
		so you can perform lookups with either the key or the value.
	
	If no positional argument is given, an empty dictionary is created.
	If a positional argument is given and it is a mapping object, a dictionary
		is created with the same key-value pairs as the mapping object.
	Otherwise, the positional argument must be an iterable object.
		Each item in the iterable must itself be an iterable with exactly two
		objects. The first object of each item becomes a key in the new
		dictionary, and the second object the corresponding value.
	
	If keyword arguments are given, the keyword arguments and their values are
	added to the dictionary created from the positional argument.
	
	If an attempt is made to add a key or value that already exists in the
		dictionary a ValueError will be raised
	
	Keys or values of "None", "True" and "False" will be stored internally as
		"_None" "_True" and "_False" respectively
	
	Based on https://stackoverflow.com/a/1063393 by https://stackoverflow.com/users/9493/brian
	"""
	
	def __init__(self, seq=None, **kwargs):
		super().__init__(self)
		if seq:
			for key, value in dict(seq).items():
				self.__setitem__(key, value)
		else:
			for key, value in kwargs.items():
				self.__setitem__(key, value)
	
	def __setitem__(self, key, val):
		if key in self or val in self:
			if key in self and self[key] != val:
				raise ValueError(f"The key '{key}' is already present in the dictionary")
			if val in self and self[val] != key:
				raise ValueError(f"The key '{val}' is already present in the dictionary")
		
		if key is None:
			key = "_None"
		if val is None:
			val = "_None"
		
		if isinstance(key, bool):
			if key:
				key = "_True"
			else:
				key = "_False"
		
		if isinstance(val, bool):
			if val:
				val = "_True"
			else:
				val = "_False"
		
		dict.__setitem__(self, key, val)
		dict.__setitem__(self, val, key)
	
	def __delitem__(self, key):
		dict.__delitem__(self, self[key])
		dict.__delitem__(self, key)
	
	def __getitem__(self, key):
		if key is None:
			key = "_None"
		
		if isinstance(key, bool):
			if key:
				key = "_True"
			else:
				key = "_False"
		
		val = dict.__getitem__(self, key)
		
		if val == "_None":
			return None
		elif val == "_True":
			return True
		elif val == "_False":
			return False
		else:
			return val
	
	def __contains__(self, key):
		if key is None:
			key = "_None"
		
		if isinstance(key, bool):
			if key:
				key = "_True"
			else:
				key = "_False"
		
		return dict.__contains__(self, key)


def cmp(x, y):
	"""
	Implementation of cmp for Python 3
	
	Compare the two objects x and y and return an integer according to the outcome.
	The return value is negative if x < y, zero if x == y and strictly positive if x > y.

	:rtype: int
	"""
	
	# TODO: see how this compares to version in functools
	
	return int((x > y) - (x < y))

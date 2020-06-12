#!/usr/bin/env python
# cython: language_level=3
# -*- coding: utf-8 -*-
#
#  utils.py
"""
General utility functions
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

# stdlib
import sys
from typing import Any, Generator, Iterable, List, Sequence, Tuple, Union

pyversion = int(sys.version[0])  # Python Version


def as_text(value: Any) -> str:
	"""
	Convert the given value to a string. ``None`` is converted to ``''``.

	:param value: Value to convert to a string

	:rtype: str
	"""

	if value is None:
		return ""

	return str(value)


def check_dependencies(dependencies: Iterable[str], prt: bool = True) -> List[str]:
	"""
	Check whether one or more dependencies are available to be imported.

	:param dependencies: The list of dependencies to check the availability of.
	:param prt: Whether the status should be printed to the terminal. Default ``True``.
	:type prt: bool, optional

	:return: A list of any missing modules
	:rtype: list
	"""

	# stdlib
	from pkgutil import iter_modules

	modules = {x[1] for x in iter_modules()}
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

	return missing_modules


def chunks(l: Sequence[Any], n: int) -> Generator[Any, None, None]:
	"""
	Yield successive n-sized chunks from l.

	:param l: The objects to yield chunks from
	:type l: ~collections.abc.Sequence
	:param n: The size of the chunks
	:type n: int
	"""

	for i in range(0, len(l), n):
		yield l[i:i + n]


def cmp(x, y) -> int:
	"""
	Implementation of cmp for Python 3.

	Compare the two objects x and y and return an integer according to the outcome.

	The return value is negative if x < y, zero if x == y and strictly positive if x > y.

	:rtype: int
	"""

	return int((x > y) - (x < y))


def list2str(the_list: Iterable[Any], sep: str = ",") -> str:
	"""
	Convert an iterable, such as a list, to a comma separated string.

	:param the_list: The iterable to convert to a string
	:type the_list: ~collections.abc.Iterable
	:param sep: Separator to use for the string. Default `,`
	:type sep: str

	:return: Comma separated string
	:rtype: str
	"""

	return sep.join([str(x) for x in the_list])


tuple2str = list2string = list2str


def permutations(data: Iterable[Any], n: int = 2) -> List[Tuple[Any, ...]]:
	"""
	Return permutations containing ``n`` items from ``data`` without any reverse duplicates.

	If ``n`` is equal to or greater than the length of the data an empty list of returned.

	:param data:
	:type data: ~collections.abc.Iterable
	:param n:
	:type n: int
	"""

	# stdlib
	import itertools

	if n == 0:
		raise ValueError("`n` cannot be 0")

	perms = []
	for i in itertools.permutations(data, n):
		if i[::-1] not in perms:
			perms.append(i)

	return perms


def printr(obj: Any, *args, **kwargs) -> None:
	"""
	Print the repr() of an object.
	"""

	print(repr(obj), *args, **kwargs)


def printt(obj: Any, *args, **kwargs) -> None:
	"""
	Print the type of an object.
	"""

	print(type(obj), *args, **kwargs)


def stderr_writer(*args, **kwargs):
	"""
	Write to stderr, flushing stdout beforehand and stderr afterwards.
	"""

	sys.stdout.flush()
	kwargs["file"] = sys.stderr
	print(*args, **kwargs)
	sys.stderr.flush()


printe = stderr_writer


def split_len(string: str, n: int) -> List[str]:
	"""
	Split a string every ``n`` characters.

	:param string: The string to split
	:type string: str
	:param n: The number of characters to split after
	:type n: int

	:return: The split string
	"""

	return [string[i:i + n] for i in range(0, len(string), n)]


splitLen = split_len


def str2tuple(input_string: str, sep: str = ",") -> Tuple[int, ...]:
	"""
	Convert a comma-separated string of integers into a tuple.

	.. important::

		The input string must represent a comma-separated series of integers.

	TODO: Allow custom types, not just ``int`` (making ``int`` the default)

	:param input_string: The string to be converted into a tuple
	:type input_string: str
	:param sep: The separator in the string. Default `,`
	:type sep: str
	"""

	return tuple(int(x) for x in input_string.split(sep))


def strtobool(val: Union[str, bool]) -> bool:
	"""
	Convert a string representation of truth to ``True`` or ``False``.

	If val is an integer then its boolean representation is returned. If val is a boolean it is returned as-is.

	True values are 'y', 'yes', 't', 'true', 'on', and '1'; false values
	are 'n', 'no', 'f', 'false', 'off', and '0'.  Raises ValueError if
	'val' is anything else.

	Based on distutils
	"""

	if isinstance(val, int):
		return bool(val)

	val = val.lower()
	if val in ('y', 'yes', 't', 'true', 'on', '1'):
		return True
	elif val in ('n', 'no', 'f', 'false', 'off', '0'):
		return False
	else:
		raise ValueError(f"invalid truth value {val!r}")


def enquote_value(value: Any) -> Union[str, bool, float]:
	"""
	Adds quotes to the given value, suitable for use in a templating system such as Jinja2.

	floats, integerss, booleans, None, and the strings "True", "False" and "None" are returned as-is.

	:param value: The value to enquote
	"""

	if value in {"True", "False", "None", True, False, None}:
		return value
	elif isinstance(value, (int, float)):
		return value
	else:
		return f"'{value}'"

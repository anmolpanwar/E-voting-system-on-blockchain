# Copyright (C) 2008-2009 John Millikin <jmillikin@gmail.com>
# 
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""JSON parser/serializer for Python.

The main implementation of this module is accessed through calls to
``read()`` and ``write()``. See their documentation for details.

"""
__author__ = "John Millikin <jmillikin@gmail.com>"
__version__ = (1, 6, 1)
__license__ = "GPL"

__all__ = [
	'loads', 'dumps', 'read', 'write',
	'ReadError', 'WriteError', 'UnknownSerializerError',
]

import codecs
from decimal import Decimal
import re
import sys
import abc
import collections

# Constants {{{
KEYWORDS = (('null', None), ('true', True), ('false', False))
try:
	INFINITY = float ('inf')
except ValueError:
	INFINITY = 1e300000
try:
	NAN = float ('nan')
except ValueError:
	NAN = INFINITY/INFINITY
	
UNICODE_BOMS = [
	(codecs.BOM_UTF32_BE, 'utf-32-be'),
	(codecs.BOM_UTF32_LE, 'utf-32-le'),
	(codecs.BOM_UTF16_BE, 'utf-16-be'),
	(codecs.BOM_UTF16_LE, 'utf-16-le'),
	(codecs.BOM_UTF8, 'utf-8'),
]
UTF_HEADERS = [
	((0, 0, 0, 1), 'utf-32-be'),
	((1, 0, 0, 0), 'utf-32-le'),
	((0, 1, 0, 1), 'utf-16-be'),
	((1, 0, 1, 0), 'utf-16-le'),
]

NUMBER_SPLITTER = re.compile (
	'^(?P<minus>-)?(?P<int>0|[1-9][0-9]*)' # Basic integer portion
	'(?:\\.(?P<frac>[0-9]+))?'             # Fractional portion
	'(?P<exp>[eE][-+]?[0-9]+)?$',          # Exponent
)

READ_ESCAPES = {
	'\\': '\\',
	'"': '"',
	'/': '/',
	'b': '\b',
	'f': '\f',
	'n': '\n',
	'r': '\r',
	't': '\t',
}

WRITE_ESCAPES = {
	# Escaping the solidus is a security measure intended for
	# protecting users from broken browser parsing, if the consumer
	# is stupid enough to parse JSON by including it directly into
	# a <script> tag.
	# 
	# See: http://t3.dotgnu.info/blog/insecurity/quotes-dont-help.html
	'/': '\\/',
	'"': '\\"',
	'\t': '\\t',
	'\b': '\\b',
	'\n': '\\n',
	'\r': '\\r',
	'\f': '\\f',
	'\\': '\\\\'
}

for __char_ord in range (0, 0x20):
	WRITE_ESCAPES.setdefault (chr (__char_ord), '\\u%04x' % __char_ord)
	
ALLOWED_WHITESPACE = '\u0020\u0009\u000A\u000D'
# }}}

# Exception classes {{{
class ReadError (ValueError):
	"""Exception raised if there is an error parsing a JSON expression."""
	pass
	
class WriteError (ValueError):
	"""Exception raised if there is an error generating a JSON expression."""
	pass
	
class UnknownSerializerError (WriteError):
	"""Exception raised if there is no known way to convert a
	value to a JSON expression.
	
	"""
	pass
# }}}

# Parser {{{
def unicode_autodetect_encoding (bytestring):
	"""Intelligently convert a byte string to Unicode.
	
	Assumes the encoding used is one of the UTF-* variants. If the
	input is already in unicode, this is a noop.
	
	"""
	if isinstance (bytestring, str):
		return bytestring
		
	# Check for UTF byte order marks in the bytestring
	for bom, encoding in UNICODE_BOMS:
		if bytestring.startswith (bom):
			return bytestring[len(bom):].decode (encoding)
			
	# Autodetect UTF-* encodings using the algorithm in the RFC
	# Don't use inline if..else for Python 2.4
	header = tuple ((1 if b else 0) for b in bytestring[:4])
	for utf_header, encoding in UTF_HEADERS:
		if header == utf_header:
			return bytestring.decode (encoding)
			
	# Default to UTF-8
	return bytestring.decode ('utf-8')
	
class ParseErrorHelper:
	"""Small class to provide a collection of error-formatting routines
	shared between the Python and C implementation.
	
	"""
	def next_char_ord (self, text, offset):
		value = ord (text[offset])
		if (0xD800 <= value <= 0xDBFF) and len (text) >= 2:
			upper = value
			lower = ord (text[offset + 1])
			upper -= 0xD800
			lower -= 0xDC00
			value = ((upper << 10) + lower) + 0x10000
			
		if value > 0xffff:
			return "U+%08X" % value
		return "U+%04X" % value
		
	def generic (self, text, offset, message):
		line = text.count ('\n', 0, offset) + 1
		if line == 1:
			column = offset + 1
		else:
			column = offset - text.rindex ('\n', 0, offset)
			
		template = ("JSON parsing error at line %d, column %d"
		            " (position %d): %s")
		error = template % (line, column, offset, message)
		raise ReadError (error)
		
	def unexpected (self, text, offset, looking_for):
		char_ord = self.next_char_ord (text, offset)
		if looking_for is None:
			desc = "Unexpected %s." % (char_ord,)
		else:
			desc = "Unexpected %s while looking for %s." % (char_ord, looking_for)
		self.generic (text, offset, desc)
		
	def extra_data (self, text, offset):
		self.generic (text, offset, "Extra data after JSON expression.")
		
	def no_expression (self, text, offset):
		self.generic (text, offset, "No expression found.")
		
	def unknown_escape (self, text, offset, escape):
		self.generic (text, offset, "Unknown escape code: \\%s." % escape)
		
	def unterminated_unicode (self, text, offset):
		self.generic (text, offset, "Unterminated unicode escape.")
		
	def unterminated_string (self, text, offset):
		self.generic (text, offset, "Unterminated string.")
		
	def reserved_code_point (self, text, offset, ord):
		self.generic (text, offset, "U+%04X is a reserved code point." % ord)
		
	def missing_surrogate (self, text, offset):
		self.generic (text, offset, "Missing surrogate pair half.")
		
	def invalid_number (self, text, offset):
		self.generic (text, offset, "Invalid number.")
		
class Parser:
	def __init__ (self, text, use_float, error_helper):
		self.text = text
		self.index = 0
		self.use_float = use_float
		self.raise_ = error_helper
		
	def parse (self):
		value = self.parse_raw (True)
		self.skip_whitespace ()
		if self.index != len (self.text):
			self.raise_.extra_data (self.text, self.index)
		return value
		
	def parse_raw (self, root = False):
		self.skip_whitespace ()
		if self.index == len (self.text):
			self.raise_.no_expression (self.text, 0)
		c = self.text[self.index]
		if c == '{':
			return self.read_object ()
		if c == '[':
			return self.read_array ()
		if root:
			self.raise_unexpected ()
		if c == '"':
			return self.read_string ()
		if c in 'tfn':
			return self.read_keyword ()
		if c in '-0123456789':
			return self.read_number ()
		self.raise_unexpected ()
		
	def read_object (self):
		retval = {}
		start = self.index
		skip = lambda: self.skip_whitespace (start, "Unterminated object.")
		c = lambda: self.text[self.index]
		
		self.skip ('{', "object start")
		skip ()
		if c () == '}':
			self.skip ('}', "object end")
			return retval
		while True:
			skip ()
			if c () != '"':
				self.raise_unexpected ("property name")
			key = self.parse_raw ()
			skip ()
			self.skip (':', "colon")
			skip ()
			value = self.parse_raw ()
			retval[key] = value
			skip ()
			if c () == '}':
				self.skip ('}', "object end")
				return retval
			self.skip (',', "comma")
			
	def read_array (self):
		retval = []
		start = self.index
		skip = lambda: self.skip_whitespace (start, "Unterminated array.")
		c = lambda: self.text[self.index]
		
		self.skip ('[', "array start")
		skip ()
		if c () == ']':
			self.skip (']', "array end")
			return retval
		while True:
			skip ()
			value = self.parse_raw ()
			retval.append (value)
			skip ()
			if c () == ']':
				self.skip (']', "array end")
				return retval
			self.skip (',', "comma")
			
		
	def read_string (self):
		text_len = len (self.text)
		start = self.index
		escaped = False
		chunks = []
		
		self.skip ('"', "string start")
		while True:
			while not escaped:
				if self.index >= text_len:
					self.raise_.unterminated_string (self.text, start)
					
				c = self.text[self.index]
				if c == '\\':
					escaped = True
				elif c == '"':
					self.skip ('"', "string end")
					return ''.join (chunks)
				elif ord (c) < 0x20:
					self.raise_unexpected ()
				else:
					chunks.append (c)
				self.index += 1
				
			escaped = False
			if self.index >= text_len:
				self.raise_.unterminated_string (self.text, start)
				
			c = self.text[self.index]
			if c == 'u':
				unescaped = self.read_unicode_escape ()
				chunks.append (unescaped)
			elif c in READ_ESCAPES:
				chunks.append (READ_ESCAPES[c])
			else:
				self.raise_.unknown_escape (self.text, self.index - 1, c)
			self.index += 1
			
	def read_unicode_escape (self):
		"""Read a JSON-style Unicode escape.
		
		Unicode escapes may take one of two forms:
		
		* \\uUUUU, where UUUU is a series of four hexadecimal digits that
		indicate a code point in the Basic Multi-lingual Plane.
		
		* \\uUUUU\\uUUUU, where the two points encode a UTF-16 surrogate pair.
		  In builds of Python without wide character support, these are
		  returned as a surrogate pair.
		
		"""
		first_hex_str = self.text[self.index+1:self.index+5]
		if len (first_hex_str) < 4 or '"' in first_hex_str:
			self.raise_.unterminated_unicode (self.text, self.index - 1)
		first_hex = int (first_hex_str, 16)
		
		# Some code points are reserved for indicating surrogate pairs
		if 0xDC00 <= first_hex <= 0xDFFF:
			self.raise_.reserved_code_point (self.text, self.index - 1, first_hex)
			
		# Check if it's a UTF-16 surrogate pair
		if not (0xD800 <= first_hex <= 0xDBFF):
			self.index += 4
			return chr (first_hex)
			
		second_hex_str = self.text[self.index+5:self.index+11]
		if (not (len (second_hex_str) >= 6
			and second_hex_str.startswith ('\\u'))
		    or '"' in second_hex_str):
			self.raise_.missing_surrogate (self.text, self.index + 5)
			
		second_hex = int (second_hex_str[2:], 16)
		if sys.maxunicode <= 65535:
			retval = chr (first_hex) + chr (second_hex)
		else:
			# Convert to 10-bit halves of the 20-bit character
			first_hex -= 0xD800
			second_hex -= 0xDC00
			
			# Merge into 20-bit character
			retval = chr ((first_hex << 10) + second_hex + 0x10000)
		self.index += 10
		return retval
		
	def read_keyword (self):
		for text, value in KEYWORDS:
			end = self.index + len (text)
			if self.text[self.index:end] == text:
				self.index = end
				return value
		self.raise_unexpected ()
		
	def read_number (self):
		allowed = '0123456789-+.eE'
		end = self.index
		try:
			while self.text[end] in allowed:
				end += 1
		except IndexError:
			pass
		match = NUMBER_SPLITTER.match (self.text[self.index:end])
		if not match:
			self.raise_.invalid_number (self.text, self.index)
			
		self.index = end
		int_part = int (match.group ('int'), 10)
		if match.group ('frac') or match.group ('exp'):
			if self.use_float:
				return float (match.group (0))
			return Decimal (match.group (0))
		if match.group ('minus'):
			return -int_part
		return int_part
		
	def skip (self, text, error):
		new_index = self.index + len (text)
		skipped = self.text[self.index:new_index]
		if skipped != text:
			self.raise_unexpected (error)
		self.index = new_index
		
	def skip_whitespace (self, start = None, err = None):
		text_len = len (self.text)
		ws = '\x09\x20\x0a\x0d'
		while self.index < text_len and self.text[self.index] in ws:
			self.index += 1
		if self.index >= text_len and (start is not None) and (err is not None):
			self.raise_.generic (self.text, start, err)
			
	def raise_unexpected (self, message = None):
		self.raise_.unexpected (self.text, self.index, message)
		
def read_impl (text, use_float, error_helper):
	parser = Parser (text, use_float, error_helper)
	return parser.parse ()
	
def read (bytestring, use_float = False):
	"""Parse a JSON expression into a Python value.
	
	If string is a byte string, it will be converted to Unicode
	before parsing (see unicode_autodetect_encoding).
	
	"""
	text = unicode_autodetect_encoding (bytestring)
	return read_impl (text, use_float, ParseErrorHelper ())
	
loads = read
# }}}

# Serializer {{{
class JSONAtom (metaclass = abc.ABCMeta):
	pass
	
JSONAtom.register (type (None))
JSONAtom.register (int)
JSONAtom.register (float)
JSONAtom.register (complex)
JSONAtom.register (Decimal)
JSONAtom.register (str)

class SerializerErrorHelper:
	def invalid_root (self):
		raise WriteError ("The outermost container must be an array or object.")
		
	def unknown_serializer (self, value):
		raise UnknownSerializerError ("No known serializer for object: %r" % (value,))
		
	def self_referential (self):
		raise WriteError ("Cannot serialize self-referential values.")
		
	def invalid_object_key (self):
		raise WriteError ("Only strings may be used as object keys.")
		
	def incomplete_surrogate (self):
		raise WriteError ("Cannot serialize incomplete surrogate pair.")
		
	def invalid_surrogate (self):
		raise WriteError ("Cannot serialize invalid surrogate pair.")
		
	def reserved_code_point (self, ord):
		raise WriteError ("Cannot serialize reserved code point U+%04X." % ord)
		
	def no_nan (self):
		raise WriteError ("Cannot serialize NaN.")
		
	def no_infinity (self):
		raise WriteError ("Cannot serialize Infinity.")
		
	def no_neg_infinity (self):
		raise WriteError ("Cannot serialize -Infinity.")
		
	def no_imaginary (self):
		raise WriteError ("Cannot serialize complex numbers with"
		                  " imaginary components.")
		
class Serializer (metaclass = abc.ABCMeta):
	def __init__ (self, sort_keys, indent, ascii_only,
	              coerce_keys, encoding, on_unknown,
	              error_helper):
		self.sort_keys = sort_keys
		self.indent = indent
		self.ascii_only = ascii_only
		self.coerce_keys = coerce_keys
		self.encoding = encoding
		self.on_unknown = on_unknown
		self.raise_ = error_helper
		
	@abc.abstractmethod
	def append (self, value):
		raise NotImplementedError
		
	@abc.abstractmethod
	def serialize (self, value):
		raise NotImplementedError
		
	def serialize_object (self, value, parent_ids, in_unknown_hook = False):
		if isinstance (value, collections.UserString):
			value = value.data
		if isinstance (value, JSONAtom):
			if not parent_ids:
				self.raise_.invalid_root ()
			self.serialize_atom (value)
		elif isinstance (value, collections.Mapping):
			self.serialize_mapping (value, parent_ids)
		elif isinstance (value, collections.Iterable):
			self.serialize_iterable (value, parent_ids)
		elif not in_unknown_hook:
			new_value = self.on_unknown (value,
				self.raise_.unknown_serializer)
			self.serialize_object (new_value, parent_ids, True)
		else:
			self.raise_.unknown_serializer (value)
			
	def get_separators (self, indent_level):
		if self.indent is None:
			return '', ''
		else:
			indent = '\n' + (self.indent * (indent_level + 1))
			post_indent = '\n' + (self.indent * indent_level)
			return indent, post_indent
			
	def serialize_mapping (self, value, parent_ids):
		v_id = id (value)
		if v_id in parent_ids:
			self.raise_.self_referential ()
			
		a = self.append
		first = True
		items = value.items ()
		if self.sort_keys:
			items = sorted (items)
			
		indent, post_indent = self.get_separators (len (parent_ids))
		
		a ('{')
		for key, item in items:
			if isinstance (key, collections.UserString):
				key = key.data
			if not isinstance (key, str):
				if self.coerce_keys:
					key = str (key)
				else:
					self.raise_.invalid_object_key ()
			if first:
				first = False
			else:
				a (',')
			a (indent)
			self.serialize_object (key, parent_ids + [v_id])
			if self.indent is None:
				a (':')
			else:
				a (': ')
			self.serialize_object (item, parent_ids + [v_id])
		a (post_indent)
		a ('}')
		
	def serialize_iterable (self, value, parent_ids):
		v_id = id (value)
		if v_id in parent_ids:
			self.raise_.self_referential ()
			
		a = self.append
		
		indent, post_indent = self.get_separators (len (parent_ids))
		
		a ('[')
		first = True
		for item in value:
			if first:
				first = False
			else:
				a (',')
			a (indent)
			self.serialize_object (item, parent_ids + [v_id])
		a (post_indent)
		a (']')
		
	def serialize_atom (self, value):
		for keyword, kw_value in KEYWORDS:
			if value is kw_value:
				return self.append (keyword)
				
		if isinstance (value, str):
			self.serialize_string (value)
		elif isinstance (value, int):
			self.append (str (value))
		elif isinstance (value, float):
			self.serialize_float (value)
		elif isinstance (value, complex):
			self.serialize_complex (value)
		elif isinstance (value, Decimal):
			self.serialize_decimal (value)
		else:
			self.raise_.unknown_serializer (value)
			
	def serialize_string (self, value):
		a = self.append
		stream = iter (value)
		a ('"')
		for char in stream:
			ochar = ord (char)
			if char in WRITE_ESCAPES:
				a (WRITE_ESCAPES[char])
			elif ochar > 0x7E:
				# Prevent invalid surrogate pairs from being
				# encoded.
				if 0xD800 <= ochar <= 0xDBFF:
					try:
						nextc = next (stream)
					except StopIteration:
						self.raise_.incomplete_surrogate ()
					onext = ord (nextc)
					if not (0xDC00 <= onext <= 0xDFFF):
						self.raise_.invalid_surrogate ()
					if self.ascii_only:
						a ('\\u%04x\\u%04x' % (ochar, onext))
					else:
						a (char)
						a (nextc)
				elif 0xDC00 <= ochar <= 0xDFFF:
					self.raise_.reserved_code_point (ochar)
				elif self.ascii_only:
					if ochar > 0xFFFF:
						unicode_value = ord (char)
						reduced = unicode_value - 0x10000
						second_half = (reduced & 0x3FF) # Lower 10 bits
						first_half = (reduced >> 10)
					
						first_half += 0xD800
						second_half += 0xDC00
					
						a ('\\u%04x\\u%04x'% (first_half, second_half))
					else:
						a ('\\u%04x' % ochar)
				else:
					a (char)
			else:
				a (char)
				
		a ('"')
		
	def serialize_float (self, value):
		if value != value:
			self.raise_.no_nan ()
		if value == INFINITY:
			self.raise_.no_infinity ()
		if value == -INFINITY:
			self.raise_.no_neg_infinity ()
		self.append (repr (value))
		
	def serialize_complex (self, value):
		if value.imag == 0.0:
			self.append (repr (value.real))
		else:
			self.raise_.no_imaginary ()
			
	def serialize_decimal (self, value):
		if value != value:
			self.raise_.no_nan ()
		s_value = str (value)
		if s_value == 'Infinity':
			self.raise_.no_infinity ()
		elif s_value == '-Infinity':
			self.raise_.no_neg_infinity ()
		self.append (s_value)
		
class StreamSerializer(Serializer):
	def __init__ (self, fp, *args, **kwargs):
		super (StreamSerializer, self).__init__ (*args, **kwargs)
		self.fp = fp
		
	def append (self, value):
		if self.encoding is not None:
			value = value.encode (self.encoding)
		self.fp.write (value)
		
	def serialize (self, value):
		self.serialize_object (value, [])
		
class BufferSerializer(Serializer):
	def __init__ (self, *args, **kwargs):
		super (BufferSerializer, self).__init__ (*args, **kwargs)
		self.chunks = []
		
	def append (self, value):
		self.chunks.append (value)
		
	def serialize (self, value):
		self.serialize_object (value, [])
		str_result = ''.join (self.chunks)
		if self.encoding is None:
			return str_result
		return str_result.encode (self.encoding)
		
def dump_impl (value, fp, sort_keys, indent, ascii_only,
               coerce_keys, encoding, on_unknown, error_helper):
	serializer = StreamSerializer (fp, sort_keys, indent, ascii_only,
	                               coerce_keys, encoding,
	                               on_unknown, error_helper)
	return serializer.serialize (value)
	
def dump (value, fp, sort_keys = False, indent = None, ascii_only = True,
          coerce_keys = False, encoding = 'utf-8', on_unknown = None):
	"""Serialize a Python value to a JSON-formatted byte string.
	
	Rather than being returned as a string, the output is written to
	a file-like object.
	
	"""
	return dump_impl (value, fp, sort_keys,
	                  validate_indent (indent), ascii_only,
	                  coerce_keys, encoding,
	                  validate_on_unknown (on_unknown),
	                  SerializerErrorHelper ())
	
def write_impl (value, sort_keys, indent, ascii_only,
                coerce_keys, encoding, on_unknown, error_helper):
	serializer = BufferSerializer (sort_keys, indent, ascii_only,
	                               coerce_keys, encoding,
	                               on_unknown, error_helper)
	return serializer.serialize (value)
	
def write (value, sort_keys = False, indent = None, ascii_only = True,
           coerce_keys = False, encoding = 'utf-8', on_unknown = None):
	"""Serialize a Python value to a JSON-formatted byte string.
	
	.. describe:: value
		
		The Python object to serialize.
		
	.. describe:: sort_keys
		
		Whether object keys should be kept sorted. Useful
		for tests, or other cases that check against a
		constant string value.
		
	.. describe:: indent
		
		A string to be used for indenting arrays and objects.
		If this is non-None, pretty-printing mode is activated.
		
	.. describe:: ascii_only
		
		Whether the output should consist of only ASCII
		characters. If this is True, any non-ASCII code points
		are escaped even if their inclusion would be legal.
	
	.. describe:: coerce_keys
		
		Whether to coerce invalid object keys to strings. If
		this is False, an exception will be raised when an
		invalid key is specified.
	
	.. describe:: encoding
		
		The output encoding to use. This must be the name of an
		encoding supported by Python's codec mechanism. If
		None, a Unicode string will be returned rather than an
		encoded bytestring.
		
		If a non-UTF encoding is specified, the resulting
		bytestring might not be readable by many JSON libraries,
		including jsonlib.
		
		The default encoding is UTF-8.
	.. describe:: on_unknown
		
		A callable to be used for converting objects of an
		unrecognized type into a JSON expression. If ``None``,
		unrecognized objects will raise an ``UnknownSerializerError``.
		
	"""
	return write_impl (value, sort_keys, validate_indent (indent), ascii_only,
	                   coerce_keys, encoding,
	                   validate_on_unknown (on_unknown),
	                   SerializerErrorHelper ())
	
dumps = write

def validate_indent (indent):
	if indent is not None:
		indent = str (indent)
	if not (indent is None or len (indent) == 0):
		if len (indent.strip (ALLOWED_WHITESPACE)) > 0:
			raise TypeError ("Only whitespace may be used for indentation.")
	return indent
	
def validate_on_unknown (f):
	def on_unknown (value, unknown):
		unknown (value)
	if f is None:
		return on_unknown
	if not isinstance (f, collections.Callable):
		raise TypeError ("The on_unknown object must be callable.")
	return f
# }}}

try:
	from _jsonlib import read_impl, write_impl, dump_impl
except ImportError:
	pass

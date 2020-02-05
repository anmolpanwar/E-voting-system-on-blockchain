########################################################################
# hashlib_additional Python library
# Copyright (c) 2019 Ryan Finnie
#
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
# CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
# TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
# SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
########################################################################

import struct
import codecs
import zlib
import copy
import random as _random


__version__ = '1.0.1'


class HASH:
    """
    A hash represents the object used to calculate a checksum of a
    string of information.
    """
    name = 'hash'
    digest_size = 0
    block_size = 0
    _checksum = b''

    def __init__(self, data=b'', **kwargs):
        self.update(data)

    def copy(self):
        """Return a copy of the hash object."""
        return copy.copy(self)

    def digest(self):
        """Return the digest value as a string of binary data."""
        return self._checksum

    def hexdigest(self):
        """Return the digest value as a string of hexadecimal digits."""
        return codecs.encode(self.digest(), 'hex_codec').decode('ascii')

    def update(self, data):
        """Update this hash object's state with the provided string."""
        pass


class crc32(HASH):
    name = 'crc32'
    digest_size = 4
    block_size = 1
    _checksum = 0

    def update(self, data):
        self._checksum = zlib.crc32(data, self._checksum)

    def digest(self):
        return struct.pack(b'>I', (self._checksum & 0xffffffff))


class bsd(HASH):
    name = 'bsd'
    digest_size = 2
    block_size = 1
    _checksum = 0

    def update(self, data):
        for ch in data:
            self._checksum = (self._checksum >> 1) + ((self._checksum & 1) << 15)
            self._checksum += ch
            self._checksum &= 0xffff

    def digest(self):
        return struct.pack(b'>H', self._checksum)


class twoping(HASH):
    """
    2ping checksum

    https://www.finnie.org/software/2ping/
    """
    name = 'twoping'
    digest_size = 2
    block_size = 2
    _held_data = b''
    _checksum = 0

    def update(self, data):
        data = self._held_data + data

        if (len(data) % 2) == 1:
            self._held_data = bytes([data[-1]])
            data = data[0:-1]
        else:
            self._held_data = b''

        for i in range(0, len(data), 2):
            self._checksum = self._checksum + (data[i] << 8) + data[i+1]
            self._checksum = ((self._checksum & 0xffff) + (self._checksum >> 16))

    def digest(self):
        checksum = self._checksum

        if self._held_data:
            checksum = checksum + (ord(self._held_data) << 8)
            checksum = ((checksum & 0xffff) + (checksum >> 16))

        checksum = ~checksum & 0xffff

        if checksum == 0:
            checksum = 0xffff

        return struct.pack(b'>H', checksum)


class udp(HASH):
    name = 'udp'
    digest_size = 2
    block_size = 2
    _held_data = b''
    _checksum = 0

    def _carry_around_add(self, a, b):
        c = a + b
        return (c & 0xffff) + (c >> 16)

    def update(self, data):
        data = self._held_data + data

        if (len(data) % 2) == 1:
            self._held_data = bytes([data[-1]])
            data = data[0:-1]
        else:
            self._held_data = b''

        for i in range(0, len(data), 2):
            self._checksum = self._carry_around_add(self._checksum, (data[i] + (data[i+1] << 8)))

    def digest(self):
        checksum = self._checksum

        if self._held_data:
            checksum = self._carry_around_add(checksum, ord(self._held_data))

        if checksum == 0:
            checksum = 0xffff

        return struct.pack(b'>H', checksum)


class adler32(HASH):
    name = 'adler32'
    digest_size = 4
    block_size = 1
    _checksum = 1

    def update(self, data):
        self._checksum = zlib.adler32(data, self._checksum)

    def digest(self):
        return struct.pack(b'>I', (self._checksum & 0xffffffff))


class random(HASH):
    """Dummy random hash"""
    name = 'random'
    digest_size = 16
    block_size = 1
    _checksum = b''

    def __init__(self, *args, digest_size=16):
        self.digest_size = digest_size
        super().__init__(*args)

    def update(self, data):
        if data or not self._checksum:
            self._checksum = bytes([_random.randint(0, 255) for x in range(self.digest_size)])


class null(HASH):
    """Dummy null hash"""
    name = 'null'
    digest_size = 16
    block_size = 1
    _checksum = b''

    def __init__(self, *args, digest_size=16):
        self.digest_size = digest_size
        self._checksum = bytes(digest_size)
        super().__init__(*args)


__algorithm_map = {}
for obj in copy.copy(vars()).values():
    if type(obj) == type(HASH) and issubclass(obj, HASH) and obj != HASH:
        __algorithm_map[obj.name] = obj

# For the moment, everything can be done using stdlib,
# so available and guaranteed are the same.
algorithms_available = set(__algorithm_map.keys())
algorithms_guaranteed = algorithms_available

__all__ = tuple(set(
    list(algorithms_available) + [
        'new', 'algorithms_available', 'algorithms_guaranteed',
    ],
))


def new(name, *args, **kwargs):
    if name not in algorithms_available:
        raise ValueError('unsupported hash type ' + name)
    return __algorithm_map[name](*args, **kwargs)


if __name__ == '__main__':
    for name in sorted(algorithms_available):
        h = new(name)
        empty_hex = h.hexdigest()
        h = new(name, b'foo')
        initial_hex = h.hexdigest()
        h.update(b'bar')
        update_hex = h.hexdigest()
        h = h.copy()
        h.update(b'baz')
        copy_hex = h.hexdigest()
        print('{}: empty {}, initial {}, update {}, copy {}'.format(
            name,
            empty_hex,
            initial_hex,
            update_hex,
            copy_hex,
        ))

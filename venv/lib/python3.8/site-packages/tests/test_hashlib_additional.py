#!/usr/bin/env python3

import unittest
import hashlib_additional


class BaseTest:
    name = ''
    empty_digest = b''
    foo_digest = b''
    foobar_digest = b''

    def test_empty(self):
        self.assertEqual(
            hashlib_additional.new(self.name).digest(),
            self.empty_digest,
        )

    def test_foo(self):
        self.assertEqual(
            hashlib_additional.new(self.name, b'foo').digest(),
            self.foo_digest,
        )

    def test_foobar(self):
        self.assertEqual(
            hashlib_additional.new(self.name, b'foobar').digest(),
            self.foobar_digest,
        )

    def test_same(self):
        digest = hashlib_additional.new(self.name, b'foobar')
        self.assertEqual(
            digest.digest(),
            digest.digest(),
        )

    def test_update(self):
        digest = hashlib_additional.new(self.name, b'foo')
        digest.update(b'bar')
        self.assertEqual(
            digest.digest(),
            self.foobar_digest,
        )

    def test_same_update_none(self):
        digest = hashlib_additional.new(self.name, b'foobar')
        old_result = digest.digest()
        digest.update(b'')
        self.assertEqual(
            digest.digest(),
            old_result,
        )

    def test_copy_new_changed(self):
        digest = hashlib_additional.new(self.name, b'foo')
        digest_copy = digest.copy()
        digest_copy.update(b'bar')
        self.assertEqual(
            digest_copy.digest(),
            self.foobar_digest,
        )

    def test_copy_old_unchanged(self):
        digest = hashlib_additional.new(self.name, b'foo')
        digest_copy = digest.copy()
        digest_copy.update(b'bar')
        digest_copy.digest()
        self.assertEqual(
            digest.digest(),
            self.foo_digest,
        )

    def test_direct(self):
        digest = getattr(hashlib_additional, self.name)()
        digest.update(b'foo')
        self.assertEqual(
            digest.digest(),
            self.foo_digest,
        )


class TestAdler32(unittest.TestCase, BaseTest):
    name = 'adler32'
    empty_digest = b'\x00\x00\x00\x01'
    foo_digest = b'\x02\x82\x01E'
    foobar_digest = b'\x08\xab\x02z'


class TestBsd(unittest.TestCase, BaseTest):
    name = 'bsd'
    empty_digest = b'\x00\x00'
    foo_digest = b'\x00\xc0'
    foobar_digest = b'\x00\xd3'


class TestCrc32(unittest.TestCase, BaseTest):
    name = 'crc32'
    empty_digest = b'\x00\x00\x00\x00'
    foo_digest = b'\x8cse!'
    foobar_digest = b'\x9e\xf6\x1f\x95'


class TestNull(unittest.TestCase, BaseTest):
    name = 'null'
    empty_digest = b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
    foo_digest = b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
    foobar_digest = b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'

    def test_variable_digest_size(self):
        digest = hashlib_additional.new(self.name, b'foo', digest_size=3)
        self.assertEqual(
            digest.digest(),
            b'\x00\x00\x00',
        )


class TestTwoping(unittest.TestCase, BaseTest):
    name = 'twoping'
    empty_digest = b'\xff\xff'
    foo_digest = b'*\x90'
    foobar_digest = b'\xc8\xbb'


class TestUdp(unittest.TestCase, BaseTest):
    name = 'udp'
    empty_digest = b'\xff\xff'
    foo_digest = b'o\xd5'
    foobar_digest = b'D7'


class TestRandom(unittest.TestCase):
    name = 'random'

    def test_empty(self):
        self.assertEqual(
            len(hashlib_additional.new(self.name).digest()),
            16,
        )

    def test_foo(self):
        self.assertEqual(
            len(hashlib_additional.new(self.name, b'foo').digest()),
            16,
        )

    def test_same(self):
        digest = hashlib_additional.new(self.name, b'foobar')
        self.assertEqual(
            digest.digest(),
            digest.digest(),
        )

    def test_variable_digest_size(self):
        digest = hashlib_additional.new(self.name, b'foo', digest_size=3)
        self.assertEqual(
            len(digest.digest()),
            3,
        )

    def test_direct(self):
        digest = hashlib_additional.random()
        digest.update(b'foo')
        self.assertEqual(
            len(digest.digest()),
            16,
        )

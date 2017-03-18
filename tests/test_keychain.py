# -*- coding: utf-8 -*-
import pytest
import tempfile
import os.path

from mokeychain.keychain import Keychain, create


class TestKeychain(object):

    _tempdir = '/tmp'

    def setup(self):
        self._tempdir = tempfile.mkdtemp('mokeychain')

    # def test_keychain_create_interactive(self):
    #     k = create(os.path.join(self._tempdir, 'test.keychain'))

    def test_keychain_create(self):
        k = create(os.path.join(self._tempdir, 'test.keychain'), 'password')


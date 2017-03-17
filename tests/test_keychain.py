# -*- coding: utf-8 -*-
import pytest
import tempfile

from mokeychain.keychain import Keychain, create

class TestKeychain(object):
    def setup(self):
        self._tempdir = tempfile.mkdtemp('mokeychain')

    def test_seckeychaincreate_nopassword(self):
        k = create(self._tempdir)
# -*- coding: utf-8 -*-
import pytest
import tempfile

from mokeychain.keychain import Keychain

class TestKeychain(object):
    def setup(self):
        self._tempdir = tempfile.mkdtemp('mokeychain')

# -*- coding: utf-8 -*-
import os
from Security import SecKeychainOpen, SecCopyErrorMessageString, SecKeychainLock, SecKeychainUnlock, SecKeychainGetPath, \
    SecKeychainGetStatus, kSecUnlockStateStatus, kSecReadPermStatus, kSecWritePermStatus, SecKeychainCopyDefault, \
    SecItemCopyMatching, kSecMatchSearchList, kSecReturnRef, kSecClass, kSecClassCertificate
from certificate import KeychainCertificate

class KeychainException(Exception):
    """KeychainException provides the message and code given from SecCopyErrorMessageString()"""

    def __init__(self, os_status):
        self.message = SecCopyErrorMessageString(os_status, None)


class Keychain(object):
    """Keychain represents a high level object view of a keychain.

    """

    def __init__(self, path):
        if not os.path.exists(path):
            raise RuntimeError('The path supplied does not exist: {}'.format(path))

        err, self._ref = SecKeychainOpen(path, None)
        if err is not None:
            raise KeychainException(err)

    @property
    def path(self):
        pathLen = 0
        err, pathLen, pathName = SecKeychainGetPath(self._ref, pathLen, None)
        return pathName

    @property
    def status(self):
        """The status property returns a tuple of:
        unlocked, readable, writable
        """
        err, status = SecKeychainGetStatus(self._ref, None)
        if err is not None:
            raise KeychainException(err)

        unlocked = (status | kSecUnlockStateStatus == kSecUnlockStateStatus)
        readable = (status | kSecReadPermStatus == kSecReadPermStatus)
        writable = (status | kSecWritePermStatus == kSecWritePermStatus)

        return unlocked, readable, writable

    @property
    def is_default(self):
        """Determine whether this keychain is the default"""
        err, ref = SecKeychainCopyDefault(None)
        return self._ref == ref  # TODO may not actually work without calling Sec* to compare

    def lock(self):
        """Lock this keychain"""
        err = SecKeychainLock(self._ref)
        if err is not None:
            raise KeychainException(err)

    def unlock(self, password=None):
        """Unlock the keychain. If the password is none the user may be prompted to enter a password."""
        if password is None:
            err = SecKeychainUnlock(self._ref, 0, None, False)
        else:
            err = SecKeychainUnlock(self._ref, len(password), password, True)

        if err is not None:
            raise KeychainException(err)

    # def items(self):
    #     query = {
    #         kSecMatchSearchList: [self._ref],
    #         kSecReturnRef: True
    #     }
    #     err, result = SecItemCopyMatching(query, None)

    def certificates(self, label=None, subject=None, serial_number=None):
        """Generate a list of certificate items in this keychain"""
        query = {
            kSecMatchSearchList: [self._ref],
            kSecClass: kSecClassCertificate,
            kSecReturnRef: True
        }
        err, result = SecItemCopyMatching(query, None)
        if err is not None:
            raise KeychainException(err)

        for cert_item_ref in result:
            yield KeychainCertificate(cert_item_ref)

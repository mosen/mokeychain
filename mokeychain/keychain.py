# -*- coding: utf-8 -*-
import os
import objc
import CoreFoundation
import sys
import Security

from Security import SecKeychainOpen, SecCopyErrorMessageString, SecKeychainLock, SecKeychainUnlock, SecKeychainGetPath, \
    SecKeychainGetStatus, kSecUnlockStateStatus, kSecReadPermStatus, kSecWritePermStatus, SecKeychainCopyDefault, \
    SecItemCopyMatching, kSecMatchSearchList, kSecReturnRef, kSecClass, kSecClassCertificate, SecKeychainSettings, \
    SecKeychainCopySettings, SecKeychainCreate

#from certificate import KeychainCertificate

class KeychainException(Exception):
    """KeychainException provides the message and code given from SecCopyErrorMessageString()"""

    def __init__(self, os_status):
        self.message = SecCopyErrorMessageString(os_status, None)

def create(path, password=None):
    """Create a new Keychain at a specified path.

    Args:
        path: The path where the keychain should be created.
        password: The password used to secure the keychain. This may be None if you want to prompt the user.
    Returns:
        An instance of Keychain
    """
    if password is None:
        err, ref = SecKeychainCreate(path, 0, None, True, None, None)

class Keychain(object):
    """Keychain represents a high level object view of a keychain.

    The purpose of the Keychain object is to wrap the CoreFoundation functions relating to a single keychain
    in a more accessible way.

    Attributes:
        _ref: SecKeychainRef object reference
    """

    def __init__(self, path=None, ref=None):
        if path is not None:
            if not os.path.exists(path):
                raise RuntimeError('The path supplied does not exist: {}'.format(path))

            err, self._ref = SecKeychainOpen(path, None)
            if err is not None:
                raise KeychainException(err)
        elif ref is not None:
            self._ref = ref
        else:
            raise TypeError('You did not specify either a path or SecKeychainRef object')


    @property
    def path(self):
        """Get the path of the keychain."""
        pathLen = 0
        err, pathLen, pathName = SecKeychainGetPath(self._ref, pathLen, None)
        return pathName

    @property
    def status(self):
        """Get the status of the keychain.

        This will allow you to query whether the Keychain is locked, readable and/or writable.

        Returns:
            A tuple of 3 Boolean values (unlocked, readable, writable)
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

    @property
    def settings(self):
        """Get keychain settings.

        Returns:
            A tuple of 4 keychain settings:
            version: Version of keychain
            lock_on_sleep:
            use_lock_interval: Whether the Keychain should be locked after a period of time.
            lock_interval: The duration before automatically locking the keychain"""

        settings = SecKeychainSettings()
        settings.version = 1
        
        err, settings = SecKeychainCopySettings(self._ref, settings)
        if err is not None:
            raise KeychainException(err)

        return settings.version, settings.lockOnSleep, settings.useLockInterval, settings.lockInterval


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

    # def certificates(self, label=None, subject=None, serial_number=None):
    #     """Generate a list of certificate items in this keychain"""
    #     query = {
    #         kSecMatchSearchList: [self._ref],
    #         kSecClass: kSecClassCertificate,
    #         kSecReturnRef: True
    #     }
    #     err, result = SecItemCopyMatching(query, None)
    #     if err is not None:
    #         raise KeychainException(err)
    #
    #     for cert_item_ref in result:
    #         yield KeychainCertificate(cert_item_ref)

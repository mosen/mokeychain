from Security import SecCertificateCopySerialNumber, SecCertificateCopyEmailAddresses, SecCertificateCopyData, \
    SecCertificateCopyPublicKey, SecCertificateCopyCommonName, SecCertificateCopySubjectSummary, SecKeyDecrypt, \
    SecCertificateCopyLongDescription


class Key(object):
    """Class representing an asymmetric key, see SecKeyRef"""
    def __init__(self, ref=None):
        if ref:
            self._ref = ref

    def decrypt(self, cipher_text, padding=None):
        """Decrypt a block of cipher text using this key."""
        err, plain_text, plain_text_len = SecKeyDecrypt(self._ref, padding, cipher_text, len(cipher_text), None, None)
        return plain_text

    def encrypt(self, plain_text, padding=None):
        pass

    def sign(self, data, padding=None):
        pass


class Certificate(object):

    def __init__(self, ref):
        self._ref = ref

    @property
    def serial_number(self):
        """Get the DER encoded serial number of this certificate item"""
        data, err = SecCertificateCopySerialNumber(self._ref, None)
        # TODO CFErrorRef get message
        if err is not None:
            raise Exception('Cant get serial number')

        return data

    @property
    def email_addresses(self):
        """Get a list of e-mail addresses in the certificate subject. May return None"""
        err, addresses = SecCertificateCopyEmailAddresses(self._ref, None)
        if err is not None:
            raise Exception('Cant get serial number')

        return addresses

    @property
    def data(self):
        """Get the Certificate Data (DER Encoded)"""
        data = SecCertificateCopyData(self._ref)
        
        return data

    @property
    def public_key(self):
        """Get the public key from this certificate"""
        err, key_ref = SecCertificateCopyPublicKey(self._ref, None)
        if err is not None:
            raise Exception('Cant get public key')

        return Key(ref=key_ref)

    @property
    def cn(self):
        """Get the Common Name from this certificate"""
        err, common_name = SecCertificateCopyCommonName(self._ref, None)
        if err is not None:
            raise Exception('Cant get common name')

        return common_name

    @property
    def summary(self):
        """Get a human readable summary of the certificate"""
        summary = SecCertificateCopySubjectSummary(self._ref)
        return summary

    @property
    def long_description(self):
        """Get a long description of the certificate"""
        long_description, err = SecCertificateCopyLongDescription(None, self._ref, None)
        return long_description

    def __str__(self):
        """Return the string representation as the summary"""
        return self.summary


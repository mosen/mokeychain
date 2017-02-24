from Security import SecCertificateCopySerialNumber, SecCertificateCopyEmailAddresses

class KeychainCertificate(object):

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


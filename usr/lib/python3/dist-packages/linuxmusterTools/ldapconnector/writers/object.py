import logging

from ..ldap_writer import LdapWriter
from ..urls.ldaprouter import router

class LMNObjectWriter:
    """
    Search per dn, may not be the best solution.
    """

    def __init__(self):
        self.lw = LdapWriter()
        self.lr = router

    def setattr(self, dn, **kwargs):
        """
        Middleware to check if the object exists.

        :param name: cn of the object
        :type name: basestring
        """

        details = self.lr.get(f'/dn/{dn}')

        if not details:
            logging.info(f"The object {dn} was not found in ldap.")
            raise Exception(f"The object {dn} was not found in ldap.")

        self.lw._setattr(details, **kwargs)

    def delattr(self, dn, **kwargs):
        """
        Middleware to check if the object exists.

        :param name: cn of the object
        :type name: basestring
        """

        details = self.lr.get(f'/dn/{dn}')

        if not details:
            logging.info(f"The object {dn} was not found in ldap.")
            raise Exception(f"The object {dn} was not found in ldap.")

        self.lw._delattr(details, **kwargs)

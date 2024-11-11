from dataclasses import dataclass, field
from .common import LMNParent


@dataclass
class LMNDevice(LMNParent):
    cn: str
    displayName: str
    distinguishedName: str
    dNSHostName: str
    memberOf: list
    name: str
    objectClass: list
    proxyAddresses: list
    sAMAccountName: str
    sAMAccountType: str
    servicePrincipalName: list
    sophomorixAdminClass: str
    sophomorixAdminFile: str
    sophomorixComment: str
    sophomorixComputerIP: str
    sophomorixComputerMAC: str
    sophomorixComputerRoom: str
    sophomorixCreationDate: str
    sophomorixDnsNodename: str
    sophomorixRole: str
    sophomorixSchoolname: str
    sophomorixSchoolPrefix: str
    sophomorixStatus: str
    dn:   str = field(init=False)

    def __post_init__(self):
        self.dn = self.distinguishedName
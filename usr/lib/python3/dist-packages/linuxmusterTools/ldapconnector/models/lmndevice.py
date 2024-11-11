from dataclasses import dataclass, field
from .common import LMNParent


@dataclass
class LMNDevice(LMNParent):
    cn: str
    displayName: str
    distinguishedName: str
    memberOf: list
    name: str
    objectClass: list
    proxyAddresses: list
    sAMAccountName: str
    sAMAccountType: str
    sophomorixAdminClass: str
    sophomorixAdminFile: str
    sophomorixComment: str
    sophomorixComputerIP: str
    sophomorixComputerMAC: str
    sophomorixComputerRoom: str
    sophomorixCreationDate: str
    sophomorixRole: str
    sophomorixSchoolname: str
    sophomorixSchoolPrefix: str
    sophomorixStatus: str
    dn:   str = field(init=False)

    def __post_init__(self):
        self.dn = self.distinguishedName
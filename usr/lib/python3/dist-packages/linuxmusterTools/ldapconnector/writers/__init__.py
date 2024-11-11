from .user import *
from .printer import *
from .managementgroup import *
from .project import *
from .device import *
from .schoolclass import *
from .object import *


DeviceWriter = LMNDeviceWriter()
MgmtGroupWriter = LMNMGMTGroupWriter()
ObjectWriter  = LMNObjectWriter()
PrinterWriter = LMNPrinterWriter()
ProjectWriter = LMNProjectWriter()
SchoolclassWriter = LMNSchoolclassWriter()
UserWriter  = LMNUserWriter()

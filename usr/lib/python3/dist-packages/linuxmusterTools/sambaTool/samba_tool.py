import os
import logging
from dataclasses import dataclass
from samba.auth import system_session
from samba.credentials import Credentials
from samba.param import LoadParm
from samba.samdb import SamDB
from samba.netcmd.gpo import get_gpo_info
import xml.etree.ElementTree as ElementTree


lp = LoadParm()
creds = Credentials()
creds.guess(lp)
gpos_infos = {}

SAMDB_PATH = '/var/lib/samba/private/sam.ldb'

class Drives:
    """
    Object to store data from Drives.xml
    """

    def __init__(self, policy_path):
        self.policy = policy_path.split('/')[-1]
        self.path = f'{policy_path}/User/Preferences/Drives/Drives.xml'
        self.usedLetters = []
        self.load()

    def load(self):
        """
        Parse the Drives.xml in the policy directory in order to get all shares
        properties.
        """

        self.drives = []
        self.drives_dict = {}

        try:
            self.tree = ElementTree.parse(self.path)
        except FileNotFoundError:
            return

        for drive in self.tree.findall('Drive'):
            drive_attr = {'properties': {}}
            drive_attr['disabled'] = bool(int(drive.attrib.get('disabled', '0')))
            for prop in drive.findall('Properties'):
                drive_attr['properties']['useLetter'] = bool(int(prop.get('useLetter', '0')))
                drive_attr['properties']['letter'] = prop.get('letter', '')
                drive_attr['properties']['label'] = prop.get('label', 'Unknown')
                drive_attr['properties']['path'] = prop.get('path', None)
                self.usedLetters.append(drive_attr['properties']['letter'])

            self.drives.append(drive_attr)
            if drive_attr['properties']['path'] is not None:
                drive_id = drive_attr['properties']['path'].split('\\')[-1]
                self.drives_dict[drive_id] = {
                    'userLetter': drive_attr['properties']['useLetter'],
                    'letter': drive_attr['properties']['letter'],
                    'disabled': drive_attr['disabled'],
                    'label': drive_attr['properties']['label'],
                }

    def save(self, content):
        """
        Save all configuration and properties from the drives and then reload
        the configuration.

        :param content: All drives configuration and properties
        :type content: dict
        """

        self.tree.write(f'{self.path}.bak', encoding='utf-8', xml_declaration=True)

        for drive in self.tree.findall('Drive'):
            for prop in drive.findall('Properties'):
                for newDrive in content:
                    if newDrive['properties']['label'] == prop.get('label', 'Unknown'):
                        prop.set('letter', newDrive['properties']['letter'])
                        prop.set('useLetter', str(int(newDrive['properties']['useLetter'])))
                        drive.set('disabled', str(int(newDrive['disabled'])))

        self.tree.write(self.path, encoding='utf-8', xml_declaration=True)
        self.load()

@dataclass
class GPO:
    dn: str
    drives: Drives
    gpo: str
    name: str
    path: str
    unix_path: str

class GPOManager:
    """
    Sample object to manage all GPOs informations.
    """

    def __init__(self):
        if os.path.isfile(SAMDB_PATH):
            try:
                samdb = SamDB(url=SAMDB_PATH, session_info=system_session(),credentials=creds, lp=lp)
                gpos_infos = get_gpo_info(samdb, None)
            except Exception:
                logging.error(f'Could not load {SAMDB_PATH}, is linuxmuster installed ?')
        else:
            logging.warning(f'{SAMDB_PATH} not found, is linuxmuster installed ?')
        
        self.gpos = {}
        
        for gpo in gpos_infos:
            gpo_id = gpo['name'][0].decode()
            name = gpo['displayName'][0].decode()
            path = gpo['gPCFileSysPath'][0].decode()
            unix_path = "/var/lib/samba/" + '/'.join(path.split('\\')[3:])
            drives = Drives(unix_path)
            self.gpos[name] = GPO(str(gpo.dn), drives, gpo_id, name, path, unix_path)

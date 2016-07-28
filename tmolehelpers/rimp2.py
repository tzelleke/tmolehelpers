import os.path
import re


class RIMP2(object):
    _re = {
        'SCF_energy': re.compile('^\s+[*]\s+SCF-energy\s+:\s+(\S+)\s+[*]$', re.MULTILINE),
        'MP2_energy': re.compile('^\s+[*]\s+MP2-energy\s+:\s+(\S+)\s+[*]$', re.MULTILINE),
        'total_energy': re.compile('^\s+[*]\s+total\s+:\s+(\S+)\s+[*]$', re.MULTILINE)
    }

    def __init__(self, directory, filename='rimp2.out'):
        self.directory = directory
        self.filename = filename
        self._parse()

    def _parse(self):
        with open(os.path.join(self.directory, self.filename)) as f:
            rimp2_out = f.read()
        for label, regex in RIMP2._re.items():
            match = regex.search(rimp2_out)
            self.__dict__[label] = float(match.group(1)) if match else None

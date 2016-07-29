import os.path
import re


class DSCF(object):
    _re = {
        'total_energy': re.compile('^\s+[|]\s+total energy\s+=\s+(\S+)\s+[|]$', re.MULTILINE)
    }

    def __init__(self, directory, filename='dscf.out'):
        self.directory = directory
        self.filename = filename
        self._parse()

    def _parse(self):
        with open(os.path.join(self.directory, self.filename)) as f:
            dscf_out = f.read()
        self._converged(dscf_out)
        for label, regex in DSCF._re.items():
            match = regex.search(dscf_out)
            self.__dict__[label] = float(match.group(1)) if match else None

    def _converged(self, output):
        self.converged = not bool(re.search('ATTENTION: dscf did not converge!'))

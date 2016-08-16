from .vib_spectrum_parser import VibSpectrumParser
from .tmole_file import TMoleFile


class Aoforce(TMoleFile):
    _parser = [
        (VibSpectrumParser, {'natoms': (lambda s: s.natoms)})
    ]

    def __init__(self, directory, filename='aoforce.out'):
        super().__init__(directory, filename)
        self.natoms = 24
        self._run_parsers()


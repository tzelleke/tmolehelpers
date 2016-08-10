from io import StringIO

import pandas as pd
from fortranformat import FortranRecordReader
from pyparsing import Word, nums, Literal, LineStart, LineEnd, OneOrMore

from .base_parser import BaseParser


class VibSpectrumParser(BaseParser):
    _anchors = {
        'MAIN': LineStart() + Word('-') + Literal('NORMAL MODES and VIBRATIONAL FREQUENCIES (cm**(-1))') + Word(
            '-') + LineEnd(),
        'MODE': LineStart() + Literal('mode') + OneOrMore(Word(nums)) + LineEnd(),
    }

    _parser = {
        'MODE': FortranRecordReader('(A20,6I9)'),
        'FREQUENCY': FortranRecordReader('(A20,6F9.2)'),
        'IR': FortranRecordReader('(A20,6A9)'),
    }

    def __init__(self, raw, natoms):
        self.raw = StringIO(raw)
        self.natoms = natoms
        self.nmodes = natoms * 3
        self._data = pd.DataFrame(columns=['MODE', 'FREQUENCY', 'IR'])
        self._parse(self._data)

    def _chunks(self, sequence, n):
        """Yield successive n-sized chunks from sequence."""
        for i in range(0, len(sequence), n):
            yield sequence[i:i + n]

    def _parse(self, df):
        NCOLS = 6
        self._scan_forward(VibSpectrumParser._anchors['MAIN'])
        data = {
            'MODE': [],
            'FREQUENCY': [],
            'IR': []
        }
        for chunk in self._chunks(range(self.nmodes), NCOLS):
            modes, frequencies, ir = self._parse_block(chunk)
            data['MODE'].extend(modes)
            data['FREQUENCY'].extend(frequencies)
            data['IR'].extend(ir)
        print(data['MODE'])
        print(data['FREQUENCY'])

    def _parse_block(self, mode_indices):
        self._scan_forward(VibSpectrumParser._anchors['MODE'], before_match=True)
        line = self._next_content_line()
        modes = self._parser['MODE'].read(line)
        line = self._next_content_line()
        frequencies = self._parser['FREQUENCY'].read(line)
        line = self._next_content_line(skip=1)
        ir = self._parser['IR'].read(line)
        ir = [_.strip() for _ in ir]
        return modes[1:], frequencies[1:], ir[1:]

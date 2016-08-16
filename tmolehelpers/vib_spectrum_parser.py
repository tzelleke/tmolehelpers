from collections import defaultdict
from functools import reduce
from operator import add

import pandas as pd
from pyparsing import Word, nums, Literal, LineStart, LineEnd, OneOrMore

from .base_parser import BaseParser
from .fortran_line_parser import FortranLineParser


class VibSpectrumParser(BaseParser):
    _anchors = {
        'MAIN': reduce(add, [LineStart(), Word('-'),
                             Literal('NORMAL MODES and VIBRATIONAL FREQUENCIES (cm**(-1))'),
                             Word('-'), LineEnd()]),
        'MODE': reduce(add, [LineStart(), Literal('mode'), OneOrMore(Word(nums)), LineEnd()])
    }

    _parser = {
        'MODE': FortranLineParser('(A20,6I9)', skip=0),
        'FREQUENCY': FortranLineParser('(A20,6F9.2)', skip=0),
        'IR': FortranLineParser('(A20,6A9)', skip=0, map_values={'YES': True, '-': False}),
    }

    def __init__(self, raw, natoms):
        super().__init__(raw)
        self.natoms = natoms
        self.nmodes = natoms * 3
        self._data = None
        self._parse()

    def _parse(self):
        NCOLS = 6
        self.raw.seek(0)
        self._scan_forward(VibSpectrumParser._anchors['MAIN'])
        datastore = defaultdict(list)
        for chunk in self._chunks(range(self.nmodes), NCOLS):
            self._parse_block(chunk, datastore)
        self._data = pd.DataFrame(datastore)

    def _parse_block(self, mode_indices, datastore):
        self._scan_forward(VibSpectrumParser._anchors['MODE'], before_match=True)
        line = self._next_content_line()
        datastore['MODE'] += self._parser['MODE'](line)
        line = self._next_content_line()
        datastore['FREQUENCY'] += self._parser['FREQUENCY'](line)
        line = self._next_content_line(skip=1)
        datastore['IR'] += self._parser['IR'](line)

from fortranformat import FortranRecordReader


class FortranLineParser(object):
    def __init__(self, pattern, name=None, after_read_hook=None):
        self._reader = FortranRecordReader(pattern)
        self.name = name
        self._after_read_hook = after_read_hook

    def __call__(self, line):
        data = self._reader.read(line)
        return self._after_read_hook(data)

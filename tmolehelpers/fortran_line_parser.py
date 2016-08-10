from fortranformat import FortranRecordReader


class FortranLineParser(object):
    def __init__(self, pattern, name=None,
                 skip=None, strip_whitespace=True, map_values=None,
                 after_read_hook=None):
        self._reader = FortranRecordReader(pattern)
        self.name = name
        self._skip = [skip] if isinstance(skip, int) else skip
        self._strip_whitespace = strip_whitespace
        self._map_values = map_values if isinstance(map_values, dict) else None
        self._after_read_hook = after_read_hook

    def __call__(self, line):
        data = self._reader.read(line)
        if self._skip:
            skip = self._skip
            data = [_ for i, _ in enumerate(data) if i not in skip]
        if self._strip_whitespace:
            data = [(_.strip() if isinstance(_, str) else _) for _ in data]
        if self._map_values:
            _map = self._map_values
            data = [(_map[_] if _ in _map else _) for _ in data]
        if self._after_read_hook:
            data = self._after_read_hook(data)
        return data

from io import StringIO
from os.path import join


class TMoleFile(object):
    _parser = []

    def __init__(self, directory, filename):
        self.directory = directory
        self.filename = filename
        with open(join(directory, filename)) as f:
            self.raw = StringIO(f.read())

    def _run_parsers(self):
        for Parser, kwargs in self.__class__._parser:
            key = Parser.__name__
            if key.endswith('Parser'):
                key = key[:-6]
            for argname in kwargs:
                if callable(kwargs[argname]):
                    kwargs[argname] = kwargs[argname](self)
            data = Parser(self.raw, **kwargs)._data
            self.__dict__[key] = data

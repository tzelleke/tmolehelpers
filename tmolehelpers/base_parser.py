from io import StringIO


class BaseParser(object):
    def __init__(self, raw):
        self.raw = StringIO(raw)

    def _scan_forward(self, anchor, before_match=False):
        loc = self.raw.tell()
        scanner = anchor.scanString(self.raw.read())
        match, start, end = next(scanner)
        scanner.close()
        if before_match:
            self.raw.seek(loc + start)
        else:
            self.raw.seek(loc + end)

    def _next_content_line(self, skip=0):
        while True:
            line = self.raw.readline()
            if line is '':
                raise RuntimeError('EOF reached')
            if line.strip() is not '':
                if skip > 0:
                    skip -= 1
                else:
                    return line

    def _chunks(self, sequence, n):
        """Yield successive n-sized chunks from sequence."""
        for i in range(0, len(sequence), n):
            yield sequence[i:i + n]

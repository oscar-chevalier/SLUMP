class Locus:    
    def __init__(self, filename: str, line: int, column: int):
        self.filename = filename
        self.line = line
        self.column = column

    def __repr__(self):
        return f'Locus({self.filename!r}, {self.line!r}, {self.column!r})'

    def __str__(self):
        return f'{self.filename}:{self.line}.{self.column}'

    def __eq__(self, other):
        if not isinstance(other, Locus):
            return False
        return self.filename == other.filename and self.line == other.line and self.column == other.column


class Extent:
    def __init__(self, begin: Locus, end: Locus):
        assert isinstance(begin, Locus), begin
        assert isinstance(end, Locus), end
        self.begin: Locus = begin
        self.end: Locus = end

    @classmethod
    def fromto(cls, begin: 'Extent', end: 'Extent') -> 'Extent':
        return Extent(begin.begin, end.end)

    @classmethod
    def create(cls, filename, firstline, firstcolumn, length):
        return Extent(Locus(filename, firstline, firstcolumn), Locus(filename, firstline, firstcolumn+length))

    def __repr__(self):
        return f'Extent({self.begin!r}, {self.end!r})'

    def __str__(self):
        if self.begin.filename == self.end.filename:
            if self.begin.line == self.end.line:
                return f'{self.begin.filename}:{self.begin.line}.{self.begin.column}-{self.end.column}'
            return f'{self.begin.filename}:{self.begin.line}.{self.begin.column}-{self.end.line}.{self.end.column}'
        return f'{self.begin.filename}:{self.begin.line}.{self.begin.column}-{self.end.filename}:{self.end.line}.{self.end.column}'

    def __eq__(self, other):
        if not isinstance(other, Extent):
            return False
        return self.begin == other.begin and self.end == other.end

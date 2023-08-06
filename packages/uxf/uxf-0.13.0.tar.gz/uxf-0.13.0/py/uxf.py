#!/usr/bin/env python3
# Copyright © 2022 Mark Summerfield. All rights reserved.
# License: GPLv3

'''
UXF is a plain text human readable optionally typed storage format. UXF may
serve as a convenient alternative to csv, ini, json, sqlite, toml, xml, or
yaml.

The uxf module can be used as an executable. To see the command line help run:

    python3 -m uxf -h

or

    path/to/uxf.py -h

The uxf module's public API provides the following free functions and
classes.

    load(filename_or_filelike): -> uxf_obj
    loads(uxf_text): -> uxf_obj

These functions read UXF data from a file, file-like, or string.
The returned uxf_obj is of type Uxf (see below).
See the function docs for additional options.

    dump(filename_or_filelike, data)
    dumps(data) -> uxf_text

These functions write UXF data to a file, file-like, or string.
The data can be a Uxf object or a single list, List, dict, Map, or Table.
dump() writes the data to the filename_or_filelike; dumps() writes the data
into a string that's then returned. See the function docs for additional
options.

    naturalize(s) -> object

This function takes a str and returns a bool or datetime.datetime or
datetime.date or int or float if any of these can be parsed, otherwise
returns the original string s. This is provided as a helper function (e.g.,
it is used by uxfconvert.py).

    canonicalize(name, prefix)

Given a name and an optional prefix, returns a name that is a valid table or
field name.

    is_scalar(x) -> bool

Returns True if x is None or a bool, int, float, datetime.date,
datetime.datetime, str, bytes, or bytearray; otherwise returns False.

    Error

This class is used to propagate errors (and warnings if warn_is_error is
True).

    Uxf

This class has a .data attribute which holds a Map, List, or Table, a
.custom str holding a (possibly empty) custom string, and a .ttypes holding
a (possibly empty) dict whose names are TType table names and whose values
are TTypes.

    List

This class is used to represent a UXF list. It is a collections.UserList
subclass that also has .comment and .vtype attributes.

    Map

This class is used to represent a UXF map. It is a collections.UserDict
subclass that also has .comment, .ktype, and .vtype attributes. It also has
a special append() method.

    Table

This class is used to store UXF Tables. A Table has a TType (see below) and
a records list which is a list of lists of scalars with each sublist having
the same number of items as the number of fields. It also has .comment and
.ttype attributes and a special append() method.

    TType

This class is used to store a Table's name and fields (see below).

    Field

This class is used to store a Table's fields. The .name must start with a
letter and be followed by 0-uxf.MAX_IDENTIFIER_LEN-1 letters, digits, or
underscores..vtype must be one of these strs: 'bool', 'int', 'real', 'date',
'datetime', 'str', 'bytes', or None (which means accept any valid type).

Note that the __version__ is the module version (i.e., the versio of this
implementation), while the VERSION is the maximum UXF version that this
module can read (and the UXF version that it writes).
'''

import collections
import datetime
import enum
import gzip
import io
import sys
from xml.sax.saxutils import escape, unescape

try:
    from dateutil.parser import isoparse
except ImportError:
    isoparse = None


__all__ = ('__version__', 'VERSION', 'load', 'loads', 'dump', 'dumps',
           'naturalize', 'canonicalize', 'is_scalar', 'Uxf', 'List',
           'Map', 'Table', 'TType', 'Field')
__version__ = '0.13.0' # uxf module version
VERSION = 1.0 # uxf file format version

UTF8 = 'utf-8'
MAX_IDENTIFIER_LEN = 60
_KEY_TYPES = {'int', 'date', 'datetime', 'str', 'bytes'}
_VALUE_TYPES = _KEY_TYPES | {'bool', 'real'}
_ANY_VALUE_TYPES = _VALUE_TYPES | {'list', 'map', 'table'}
_BOOL_FALSE = {'no', 'false'}
_BOOL_TRUE = {'yes', 'true'}
_CONSTANTS = _BOOL_FALSE | _BOOL_TRUE
_BAREWORDS = _ANY_VALUE_TYPES | _CONSTANTS
_MISSING = object()


class Uxf:

    def __init__(self, data, custom='', *, ttypes=None):
        self.data = data
        self.custom = custom
        self.ttypes = ttypes


    @property
    def data(self):
        return self._data


    @data.setter
    def data(self, data):
        if not isinstance(data, (list, dict, List, Map, Table)):
            raise Error('Uxf data must be a list, List, dict, Map, or '
                        f'Table, got {type(data)}')
        self._data = data


def load(filename_or_filelike, *, check=False, fixtypes=False,
         warn_is_error=False):
    '''
    Returns a 2-tuple, the first item of which is a Map, List, or Table
    containing all the UXF data read. The second item is the custom string
    (if any) from the file's header.

    filename_or_filelike is sys.stdin or a filename or an open readable file
    (text mode UTF-8 encoded, optionally gzipped).

    If warn_is_error is True warnings raise Error exceptions.
    '''
    filename = (filename_or_filelike
                if isinstance(filename_or_filelike, str) else '-')
    return _loads(_read_text(filename_or_filelike), check=check,
                  fixtypes=fixtypes, warn_is_error=warn_is_error,
                  filename=filename)


def loads(uxf_text, *, check=False, fixtypes=False, warn_is_error=False):
    '''
    Returns a 2-tuple, the first item of which is a Map, List, or Table
    containing all the UXF data read. The second item is the custom string
    (if any) from the file's header.

    uxf_text must be a string of UXF data.

    If warn_is_error is True warnings raise Error exceptions.
    '''
    return _loads(uxf_text, check=check, fixtypes=fixtypes,
                  warn_is_error=warn_is_error)


def _loads(uxf_text, *, check=False, fixtypes=False, warn_is_error=False,
           filename='-'):
    tokens, custom, text = _tokenize(uxf_text, warn_is_error=warn_is_error,
                                     filename=filename)
    data, ttypes = _parse(tokens, text=uxf_text, check=check,
                          fixtypes=fixtypes, warn_is_error=warn_is_error,
                          filename=filename)
    return Uxf(data, custom, ttypes=ttypes)


def _tokenize(uxf_text, *, warn_is_error=False, filename='-'):
    lexer = _Lexer(warn_is_error=warn_is_error, filename=filename)
    tokens = lexer.tokenize(uxf_text)
    return tokens, lexer.custom, uxf_text


def _read_text(filename_or_filelike):
    if not isinstance(filename_or_filelike, str):
        return filename_or_filelike.read()
    try:
        with gzip.open(filename_or_filelike, 'rt', encoding=UTF8) as file:
            return file.read()
    except gzip.BadGzipFile:
        with open(filename_or_filelike, 'rt', encoding=UTF8) as file:
            return file.read()


class _ErrorMixin:

    def warn(self, message):
        if self.warn_is_error:
            self.error(message)
        lino = self.text.count('\n', 0, self.pos) + 1
        print(f'Warning:{self._what}:{self.filename}:{lino}: {message}')


    def error(self, message):
        lino = self.text.count('\n', 0, self.pos) + 1
        raise Error(f'{self._what}:{self.filename}:{lino}: {message}')


class _Lexer(_ErrorMixin):

    def __init__(self, *, warn_is_error=False, filename='-'):
        self.warn_is_error = warn_is_error
        self._what = 'lexer'
        self.filename = filename


    def clear(self):
        self.pos = 0 # current
        self.custom = None
        self.in_ttype = False
        self.tokens = []


    def tokenize(self, text):
        self.clear()
        self.text = text
        self.scan_header()
        while not self.at_end():
            self.scan_next()
        self.add_token(_Kind.EOF)
        return self.tokens


    def scan_header(self):
        i = self.text.find('\n')
        if i == -1:
            self.error('missing UXF file header or empty file')
        self.pos = i
        parts = self.text[:i].split(None, 2)
        if len(parts) < 2:
            self.error('invalid UXF file header')
        if parts[0] != 'uxf':
            self.error('not a UXF file')
        try:
            version = float(parts[1])
            if version > VERSION:
                self.warn(f'version ({version}) > current ({VERSION})')
        except ValueError:
            self.warn('failed to read UXF file version number')
        if len(parts) > 2:
            self.custom = parts[2]


    def at_end(self):
        return self.pos >= len(self.text)


    def scan_next(self):
        c = self.getch()
        if c.isspace():
            pass
        elif c == '(':
            if self.peek() == ':':
                self.pos += 1
                self.read_bytes()
            else:
                self.check_in_ttype()
                self.add_token(_Kind.TABLE_BEGIN)
        elif c == ')':
            self.add_token(_Kind.TABLE_END)
        elif c == '[':
            self.check_in_ttype()
            self.add_token(_Kind.LIST_BEGIN)
        elif c == '=':
            self.add_token(_Kind.TTYPE_BEGIN)
            self.in_ttype = True
        elif c == ']':
            self.add_token(_Kind.LIST_END)
        elif c == '{':
            self.check_in_ttype()
            self.add_token(_Kind.MAP_BEGIN)
        elif c == '}':
            self.in_ttype = False
            self.add_token(_Kind.MAP_END)
        elif c == '?':
            self.add_token(_Kind.NULL)
        elif c == '#':
            if self.tokens and self.tokens[-1].kind in {
                    _Kind.LIST_BEGIN, _Kind.MAP_BEGIN, _Kind.TABLE_BEGIN}:
                if self.peek() != '<':
                    self.error('a str must follow the # comment '
                               f'introducer, got {c!r}')
                self.read_comment()
            else:
                self.error('comments may only occur at the start of Maps, '
                           'Lists, and Tables')
        elif c == '<':
            self.read_string()
        elif c == ':':
            self.read_field_vtype()
        elif c == '-' and self.peek().isdecimal():
            c = self.getch() # skip the - and get the first digit
            self.read_negative_number(c)
        elif c.isdecimal():
            self.read_positive_number_or_date(c)
        elif c.isalpha():
            self.read_name()
        else:
            self.error(f'invalid character encountered: {c!r}')


    def check_in_ttype(self):
        if self.in_ttype:
            self.in_ttype = False
            self.add_token(_Kind.TTYPE_END)


    def read_comment(self):
        self.pos += 1 # skip the leading <
        value = self.match_to('>', error_text='unterminated string or name')
        self.add_token(_Kind.COMMENT, unescape(value))


    def read_string(self):
        value = self.match_to('>', error_text='unterminated string')
        self.add_token(_Kind.STR, unescape(value))


    def read_bytes(self):
        value = self.match_to(':)', error_text='unterminated bytes')
        try:
            self.add_token(_Kind.BYTES, bytes.fromhex(value))
        except ValueError as err:
            self.error(f'expected bytes, got {value!r}: {err}')


    def read_negative_number(self, c):
        is_real = False
        start = self.pos - 1
        while not self.at_end() and (c in '.eE' or c.isdecimal()):
            if c in '.eE':
                is_real = True
            c = self.text[self.pos]
            self.pos += 1
        convert = float if is_real else int
        text = self.text[start:self.pos]
        try:
            value = convert(text)
            self.add_token(_Kind.REAL if is_real else _Kind.INT,
                           -value)
        except ValueError as err:
            self.error(f'invalid number: {text}: {err}')


    def read_positive_number_or_date(self, c):
        is_real = is_datetime = False
        hyphens = 0
        start = self.pos - 1
        while not self.at_end() and (c in '-+.:eETZ' or c.isdecimal()):
            if c in '.eE':
                is_real = True
            elif c == '-':
                hyphens += 1
            elif c in ':TZ':
                is_datetime = True
            c = self.text[self.pos]
            self.pos += 1
        self.pos -= 1 # wind back to terminating non-numeric non-date char
        text = self.text[start:self.pos]
        if is_datetime:
            convert, token = self.read_datetime(text)
        elif hyphens == 2:
            convert = (datetime.date.fromisoformat if isoparse is None
                       else isoparse)
            token = _Kind.DATE
        elif is_real:
            convert = float
            token = _Kind.REAL
        else:
            convert = int
            token = _Kind.INT
        try:
            value = convert(text)
            if token is _Kind.DATE and isoparse is not None:
                value = value.date()
            self.add_token(token, value)
        except ValueError as err:
            if is_datetime and len(text) > 19:
                self.reread_datetime(text, convert)
            else:
                self.error(f'invalid number or date/time: {text}: {err}')


    def read_datetime(self, text):
        if isoparse is None:
            convert = datetime.datetime.fromisoformat
            if text.endswith('Z'):
                text = text[:-1] # Py std lib can't handle UTC 'Z'
        else:
            convert = isoparse
        convert = (datetime.datetime.fromisoformat if isoparse is None
                   else isoparse)
        return convert, _Kind.DATE_TIME


    def reread_datetime(self, text, convert):
        try:
            value = convert(text[:19])
            self.add_token(_Kind.DATE_TIME, value)
            self.warn(f'skipped timezone data, used {text[:19]!r}, got '
                      f'{text!r}')
        except ValueError as err:
            self.error(f'invalid datetime: {text}: {err}')


    def read_name(self):
        match = self.match_any_of(_BAREWORDS)
        if match in _BOOL_FALSE:
            self.add_token(_Kind.BOOL, False)
            return
        elif match in _BOOL_TRUE:
            self.add_token(_Kind.BOOL, True)
            return
        elif match in _ANY_VALUE_TYPES:
            self.add_token(_Kind.TYPE, match)
            return
        start = self.pos - 1
        if self.text[start].isupper():
            identifier = self. match_identifier(start, 'identifier')
            self.add_token(_Kind.IDENTIFIER, identifier)
        else:
            i = self.text.find('\n', self.pos)
            text = self.text[self.pos - 1:i if i > -1 else self.pos + 8]
            self.error(f'expected const or identifier, got {text!r}')


    def read_field_vtype(self):
        while self.pos < len(self.text) and self.text[self.pos].isspace():
            self.pos += 1
        identifier = self.match_identifier(self.pos, 'field vtype')
        self.add_token(_Kind.TYPE, identifier)


    def peek(self):
        return '\0' if self.at_end() else self.text[self.pos]


    def getch(self): # advance
        c = self.text[self.pos]
        self.pos += 1
        return c


    def match_identifier(self, start, what):
        while self.pos < len(self.text):
            if (not self.text[self.pos].isalnum() and
                    self.text[self.pos] != '_'):
                break
            self.pos += 1
        identifier = self.text[start:self.pos][:MAX_IDENTIFIER_LEN]
        if identifier:
            return identifier
        text = self.text[start:start + 10]
        self.error(f'expected {what}, got {text}…')


    def match_to(self, target, *, error_text):
        if not self.at_end():
            i = self.text.find(target, self.pos)
            if i > -1:
                text = self.text[self.pos:i]
                self.pos = i + len(target) # skip past target
                return text
        self.error(error_text)


    def match_any_of(self, targets):
        if self.at_end():
            return None
        start = self.pos - 1
        for target in sorted(targets, key=lambda t: (len(t), t),
                             reverse=True):
            if self.text.startswith(target, start):
                self.pos += len(target) - 1 # skip past target
                return target


    def add_token(self, kind, value=None):
        self.tokens.append(_Token(kind, value, self.pos))


class Error(Exception):
    pass


class _Token:

    def __init__(self, kind, value=None, pos=-1):
        self.kind = kind
        self.value = value # literal, i.e., correctly typed item
        self.pos = pos


    def __str__(self):
        parts = [self.kind.name]
        if self.value is not None:
            parts.append(f'={self.value!r}')
        return ''.join(parts)


    def __repr__(self):
        parts = [f'{self.__class__.__name__}({self.kind.name}']
        if self.value is not None:
            parts.append(f', {self.value!r}')
        parts.append(')')
        return ''.join(parts)


@enum.unique
class _Kind(enum.Enum):
    TTYPE_BEGIN = enum.auto()
    TTYPE_END = enum.auto()
    TABLE_BEGIN = enum.auto()
    TABLE_END = enum.auto()
    LIST_BEGIN = enum.auto()
    LIST_END = enum.auto()
    MAP_BEGIN = enum.auto()
    MAP_END = enum.auto()
    COMMENT = enum.auto()
    NULL = enum.auto()
    BOOL = enum.auto()
    INT = enum.auto()
    REAL = enum.auto()
    DATE = enum.auto()
    DATE_TIME = enum.auto()
    STR = enum.auto()
    BYTES = enum.auto()
    TYPE = enum.auto()
    IDENTIFIER = enum.auto()
    EOF = enum.auto()


class List(collections.UserList):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.comment = None
        self.vtype = None


class Map(collections.UserDict):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.comment = None
        self.ktype = None
        self.vtype = None
        self._pending_key = _MISSING


    def append(self, value):
        '''If there's no pending key, sets the value as the pending key;
        otherwise adds a new item with the pending key and this value and
        clears the pending key.'''
        if self._pending_key is _MISSING:
            if not isinstance(value, (int, datetime.date,
                                      datetime.datetime, str, bytes)):
                prefix = ('map keys may only be of type int, date, '
                          'datetime, str, or bytes, got ')
                if isinstance(value, Table):
                    raise Error(f'{prefix} a Table ( … ) maybe bytes '
                                '(: … :) was intended?')
                else:
                    raise Error(f'{prefix} {value!r} of type {type(value)}')
            self._pending_key = value
        else:
            self.data[self._pending_key] = value
            self._pending_key = _MISSING


class _CheckNameMixin:

    def _check_name(self, name):
        if not name[0].isupper():
            raise Error(
                f'names must start with a capital letter, got {name}')
        for x in name[1:]:
            if not (x.isalnum() or x == '_'):
                raise Error('names may only contain letters, digits, or '
                            f'underscores, got {name}')


class TType(_CheckNameMixin):

    def __init__(self, name, fields=None):
        self.name = name
        self.fields = []
        if fields is not None:
            for field in fields:
                if isinstance(field, str):
                    self.fields.append(Field(field))
                else:
                    self.fields.append(field)


    @property
    def name(self):
        return self._name


    @name.setter
    def name(self, name):
        if name is not None:
            self._check_name(name)
        self._name = name


    def append(self, name_or_field, vtype=None):
        if isinstance(name_or_field, Field):
            self.fields.append(name_or_field)
        else:
            self.fields.append(Field(name_or_field, vtype))


    def set_vtype(self, index, vtype):
        self.fields[index].vtype = vtype


    def __bool__(self):
        return bool(self.name) and bool(self.fields)


    def __hash__(self):
        return hash(self.name)


    def __lt__(self, other):
        return self.name < other.name


    def __len__(self):
        return len(self.fields)


    def __repr__(self):
        fields = ', '.join(repr(field) for field in self.fields)
        return f'{self.__class__.__name__}({self.name!r}, {fields})'


class Field(_CheckNameMixin):

    def __init__(self, name, vtype=None):
        self.name = name
        self.vtype = vtype


    @property
    def name(self):
        return self._name


    @name.setter
    def name(self, name):
        self._check_name(name)
        self._name = name


    def __repr__(self):
        return f'{self.__class__.__name__}({self.name!r}, {self.vtype!r})'


class Table:
    '''Used to store a UXF table.

    A Table has a list of fields (name, optional type) and a records list
    which is a list of lists of scalars. with each sublist having the same
    number of items as the number of fields. It also has a .comment
    attribute. (Note that the lists in a Table are plain lists not UXF
    Lists.)

    The only type-safe way to add values to a table is via .append() for
    single values or += for single values or a sequence of values.

    When a Table is iterated each row is returned as a namedtuple.
    '''

    def __init__(self, *, name=None, fields=None, records=None,
                 comment=None):
        '''
        A Table may be created empty, e.g., Table(). However, if records is
        not None, then both the name and fields must be given.

        records can be a flat list of values (which will be put into a list
        of lists with each sublist being len(fields) long), or a list of
        lists in which case each list is _assumed_ to be len(fields)
        long.

        comment is an optional str.
        '''
        self._Class = None
        self.ttype = TType(name, fields)
        self.records = []
        self.comment = comment
        if records:
            if not name:
                raise Error('can\'t create an unnamed nonempty table')
            if not self.ttype:
                raise Error('can\'t create a nonempty table without fields')
            if isinstance(records, (list, List)):
                if self._Class is None:
                    self._make_record_class()
                self.records = list(records)
            else:
                for value in records:
                    self.append(value)


    @property
    def name(self):
        return self.ttype.name


    @name.setter
    def name(self, name):
        self.ttype.name = name


    @property
    def fields(self):
        return self.ttype.fields


    def field(self, column):
        return self.ttype.fields[column]


    def append(self, value):
        '''Use to append a value to the table. The value will be added to
        the last row if that isn't full, or as the first value in a new
        row'''
        if self._Class is None:
            self._make_record_class()
        if not self.records or len(self.records[-1]) >= len(self.ttype):
            self.records.append([])
        self.records[-1].append(value)


    @property
    def is_scalar(self):
        for field in self.fields:
            if field.vtype is None:
                break # any type allowed so need to check records themselves
            if field.vtype not in _VALUE_TYPES:
                return False # non-scalar expected so not a scalar table
        else:
            return True # all vtypes specified and all scalar
        for row in self.records:
            for x in row:
                if not is_scalar(x):
                    return False
        return True


    def _make_record_class(self):
        if not self.name:
            raise Error('can\'t use an unnamed table')
        if not self.fields:
            raise Error('can\'t create a table with no fields')
        self._Class = collections.namedtuple( # prefix avoids name clashes
            f'UXF{self.name}', [field.name for field in self.fields])


    def __iadd__(self, value):
        if not self.name:
            raise Error('can\'t append to an unnamed table')
        if not self.fields:
            raise Error('can\'t append to a table with no fields')
        if isinstance(value, (list, List, tuple)):
            for v in value:
                self.append(v)
        else:
            self.append(value)
        return self


    def __getitem__(self, row):
        '''Return the row-th record as a namedtuple'''
        try:
            return self._Class(*self.records[row])
        except TypeError as err:
            if 'missing' in str(err):
                err = 'table\'s ttype has fewer fields than in a row'
                raise Error(err) from None


    def __iter__(self):
        if self._Class is None:
            self._make_record_class()
        try:
            for record in self.records:
                yield self._Class(*record)
        except TypeError as err:
            if 'missing' in str(err):
                raise Error('table\'s ttype has fewer fields than in a row')


    def __len__(self):
        return len(self.records)


    def __str__(self):
        return (f'Table {self.name!r} {self.fields!r} with '
                f'{len(self.records)} records #{self.comment!r}')


    def __repr__(self):
        return (f'{self.__class__.__name__}(name={self.name!r}, '
                f'fields={self.fields!r}, '
                f'records={self.records!r}, comment={self.comment!r})')


def _parse(tokens, *, text, check=False, fixtypes=False,
           warn_is_error=False, filename='-'):
    parser = _Parser(check=check, fixtypes=fixtypes,
                     warn_is_error=warn_is_error, filename=filename)
    data = parser.parse(tokens, text)
    ttypes = parser.ttypes
    return data, ttypes


class _Parser(_ErrorMixin):

    def __init__(self, *, check=False, fixtypes=False, warn_is_error=False,
                 filename='-'):
        self.check = check
        self.fixtypes = fixtypes
        self.warn_is_error = warn_is_error
        self.filename = filename
        self._what = 'parser'


    def clear(self):
        self.stack = []
        self.ttypes = {}
        self.pos = -1


    def parse(self, tokens, text):
        if not tokens:
            return
        self.clear()
        self.tokens = tokens
        self.text = text
        data = None
        self._parse_ttypes()
        for i, token in enumerate(self.tokens):
            kind = token.kind
            collection_start = self._is_collection_start(kind)
            if data is None and not collection_start:
                self.error(f'expected a map, list, or table, got {token}')
            if collection_start:
                self._on_collection_start(token)
                if data is None:
                    data = self.stack[0]
            elif self._is_collection_end(kind):
                self._on_collection_end(token)
            elif kind is _Kind.COMMENT:
                self._handle_comment(i, token)
            elif kind is _Kind.IDENTIFIER:
                self._handle_identifier(i, token)
            elif kind is _Kind.TYPE:
                self._handle_type(i, token)
            elif kind in {_Kind.NULL, _Kind.BOOL, _Kind.INT, _Kind.REAL,
                          _Kind.DATE, _Kind.DATE_TIME, _Kind.STR,
                          _Kind.BYTES}:
                self.stack[-1].append(token.value)
            elif kind is _Kind.EOF:
                break
            else:
                self.error(f'unexpected token, got {token}')
        return data


    def _handle_comment(self, i, token):
        parent = self.stack[-1]
        prev_token = self.tokens[i - 1]
        if not self._is_collection_start(prev_token.kind):
            self.error('comments may only be put at the beginning of a '
                       f'map, list, or table, not after {prev_token}')
        parent.comment = token.value


    def _handle_identifier(self, i, token):
        parent = self.stack[-1]
        if not isinstance(parent, Table):
            self.error('ttype name may only appear at the start of a '
                       f'table, {token}')
        if self.tokens[i - 1].kind is _Kind.TABLE_BEGIN or (
                self.tokens[i - 1].kind is _Kind.COMMENT and
                self.tokens[i - 2].kind is _Kind.TABLE_BEGIN):
            ttype = self.ttypes.get(token.value)
            if ttype is None:
                self.error(f'undefined table ttype, {token}')
            parent.ttype = ttype
        else: # should never happen
            self.error('ttype name may only appear at the start of a '
                       f'table, {token}')


    def _handle_type(self, i, token):
        parent = self.stack[-1]
        if isinstance(parent, List):
            if parent.vtype is not None:
                self.error('can only have at most one vtype for a list, '
                           f'got {token}')
            parent.vtype = token.value
        elif isinstance(self.stack[-1], Map):
            if parent.ktype is None:
                parent.ktype = token.value
            elif parent.vtype is None:
                parent.vtype = token.value
            else:
                self.error('can only have at most one ktype and one vtype '
                           f'for a map, got {token}')
        else:
            self.error('ktypes and vtypes are only allowed at the start '
                       f'of maps and lists, got {token}')


    def _on_collection_start(self, token):
        kind = token.kind
        if kind is _Kind.MAP_BEGIN:
            value = Map()
        elif kind is _Kind.LIST_BEGIN:
            value = List()
        elif kind is _Kind.TABLE_BEGIN:
            value = Table()
        else:
            self.error(
                f'expected to create map, list, or table, got {token}')
        if self.stack:
            self.stack[-1].append(value) # add the collection to the parent
        self.stack.append(value) # make the collection the current parent


    def _on_collection_end(self, token):
        if self.check:
            self._check(self.stack[-1])
        if not self.stack:
            self.error(f'unexpected {token} suggests unmatched map, list, '
                       'or table start/end pair')
        self.stack.pop()


    def _is_collection_start(self, kind):
        return kind in {_Kind.MAP_BEGIN, _Kind.LIST_BEGIN,
                        _Kind.TABLE_BEGIN}


    def _is_collection_end(self, kind):
        return kind in {_Kind.MAP_END, _Kind.LIST_END,
                        _Kind.TABLE_END}


    def _parse_ttypes(self):
        used = set()
        ttype = None
        for index, token in enumerate(self.tokens):
            if token.kind is _Kind.TTYPE_BEGIN:
                if ttype is not None and ttype.name is not None:
                    self.ttypes[ttype.name] = ttype
                ttype = TType(None)
            elif token.kind is _Kind.IDENTIFIER:
                if ttype.name is None:
                    ttype.name = token.value
                else:
                    ttype.append(token.value)
            elif token.kind is _Kind.TYPE:
                if len(ttype) > 0:
                    vtype = token.value
                    ttype.set_vtype(-1, vtype)
                    if vtype[0].isupper():
                        used.add(vtype)
                else:
                    self.error(
                        f'encountered type without field name: {token}')
            elif token.kind is _Kind.TTYPE_END:
                if ttype is not None and bool(ttype):
                    self.ttypes[ttype.name] = ttype
                self.tokens = self.tokens[index + 1:]
            else:
                break # no TTypes at all
        if self.ttypes: # Check that all ttypes referred to are defined
            diff = used - set(self.ttypes.keys())
            if diff:
                diff = sorted(diff)
                if len(diff) == 1:
                    self.error(f'ttype uses undefined type: {diff[0]!r}')
                else:
                    diff = ', '.join(repr(t) for t in diff)
                    self.error(f'ttype uses undefined types: {diff}')


    def _check(self, item):
        if isinstance(item, List) and item.vtype is not None:
            self._check_list(item)
        elif isinstance(item, Map) and (item.vtype is not None or
                                        item.ktype is not None):
            self._check_map(item)
        elif isinstance(item, Table) and (
                any(field.vtype is not None for field in item.fields)):
            self._check_table(item)


    def _check_list(self, lst):
        vclass = _type_for_name(lst.vtype)
        for i in len(lst):
            value, fixed, err = _maybe_fixtype(
                lst[i], vclass, check=self.check, fixtypes=self.fixtypes)
            if fixed:
                lst[i] = value
            if err is not None:
                self.warn(str(err))


    def _check_map(self, m):
        kclass = _type_for_name(m.ktype)
        vclass = _type_for_name(m.vtype)
        d = {}
        for key, value in m.items():
            key, _, err = _maybe_fixtype(
                key, kclass, check=self.check, fixtypes=self.fixtypes)
            if err is not None:
                self.warn(str(err))
            value, _, err = _maybe_fixtype(
                value, vclass, check=self.check, fixtypes=self.fixtypes)
            if err is not None:
                self.warn(str(err))
            if self.fixtypes:
                d[key] = value
        if self.fixtypes:
            m.data = d


    def _check_table(self, table):
        columns = len(table.fields)
        vclasses = [_type_for_name(table.fields[column].vtype)
                    for column in range(columns)]
        for row in range(len(table.records)):
            if len(row) != columns:
                self.warn(f'expected row of {columns} columns, got '
                          f'{len(row)} columns')
            for column in range(len(row)):
                value, fixed, err = _maybe_fixtype(
                    table[row][column], vclasses[column], check=self.check,
                    fixtypes=self.fixtypes)
                if fixed:
                    table[row][column] = value
                if err is not None:
                    self.warn(str(err))


def dump(filename_or_filelike, data, *, indent=2,
         one_way_conversion=False, use_true_false=False):
    '''
    filename_or_filelike is sys.stdout or a filename or an open writable
    file (text mode UTF-8 encoded). If filename_or_filelike is a filename
    with a .gz suffix then the output will be gzip-compressed.

    data is a Uxf or a list, List, dict, Map, or Table, that this function
    will write to the filename_or_filelike in UXF format.

    Set indent to 0 (and use_true_false to True) to minimize the file size.

    Set one_way_conversion to True to convert bytearray items to bytes, and
    sets, frozensets, tuples, and collections.deques to Lists rather than
    raise an Error.

    If use_true_false is False (the default), bools are output as 'yes' or
    'no'; but if use_true_false is True the are output as 'true' or 'false'.
    '''
    pad = ' ' * indent
    close = False
    if isinstance(filename_or_filelike, str):
        opener = (gzip.open if filename_or_filelike[-3:].upper().endswith(
                  '.GZ') else open)
        file = opener(filename_or_filelike, 'wt', encoding=UTF8)
        close = True
    else:
        file = filename_or_filelike
    try:
        if not isinstance(data, Uxf):
            data = Uxf(data)
        _Writer(file, data, pad, one_way_conversion, use_true_false)
    finally:
        if close:
            file.close()


def dumps(data, *, indent=2, one_way_conversion=False,
          use_true_false=False):
    '''
    data is a Uxf or a list, List, dict, Map, or Table that this function
    will write to a string in UXF format which will then be returned.

    Set indent to 0 (and use_true_false to True) to minimize the string's
    size.

    Set one_way_conversion to True to convert bytearray items to bytes, and
    sets, frozensets, tuples, and collections.deques to Lists rather than
    raise an Error.

    If use_true_false is False (the default), bools are output as 'yes' or
    'no'; but if use_true_false is True the are output as 'true' or 'false'.
    '''
    pad = ' ' * indent
    string = io.StringIO()
    if not isinstance(data, Uxf):
        data = Uxf(data)
    _Writer(string, data, pad, one_way_conversion, use_true_false)
    return string.getvalue()


class _Writer:

    def __init__(self, file, uxf_obj, pad, one_way_conversion,
                 use_true_false):
        self.file = file
        self.one_way_conversion = one_way_conversion
        self.yes = 'true' if use_true_false else 'yes'
        self.no = 'false' if use_true_false else 'no'
        self.write_header(uxf_obj.custom)
        if uxf_obj.ttypes:
            self.write_ttypes(uxf_obj.ttypes)
        self.write_value(uxf_obj.data, pad=pad)


    def write_header(self, custom):
        self.file.write(f'uxf {VERSION}')
        if custom:
            self.file.write(f' {custom}')
        self.file.write('\n')


    def write_ttypes(self, ttypes):
        for ttype in sorted(ttypes.values()):
            self.file.write(f'= {ttype.name}')
            for field in ttype.fields:
                self.file.write(f' {field.name}')
                if field.vtype is not None:
                    self.file.write(f':{field.vtype}')
            self.file.write('\n')


    def write_value(self, item, indent=0, *, pad, map_value=False):
        if isinstance(item, (set, frozenset, tuple, collections.deque)):
            if self.one_way_conversion:
                item = list(item)
            else:
                raise Error(f'can only convert {type(item)} to List if '
                            'one_way_conversion is True')
        if isinstance(item, (list, List)):
            return self.write_list(item, indent, pad=pad,
                                   map_value=map_value)
        if isinstance(item, (dict, Map)):
            return self.write_map(item, indent, pad=pad,
                                  map_value=map_value)
        if isinstance(item, Table):
            return self.write_table(item, indent, pad=pad,
                                    map_value=map_value)
        return self.write_scalar(item, indent=indent, pad=pad,
                                 map_value=map_value)


    def write_list(self, item, indent=0, *, pad, map_value=False):
        tab = '' if map_value else pad * indent
        comment = getattr(item, 'comment', None)
        vtype = getattr(item, 'vtype', None)
        if len(item) == 0:
            self.file.write(f'{tab}[')
            if comment is not None:
                self.file.write(f' #<{escape(comment)}>')
            if vtype is not None:
                self.file.write(f' {vtype}')
            if comment is not None or vtype is not None:
                self.file.write(' ')
            self.file.write(']\n')
        else:
            self.file.write(f'{tab}[')
            if comment is not None:
                self.file.write(f' #<{escape(comment)}>')
            if vtype is not None:
                self.file.write(f' {vtype}')
            indent += 1
            scalar = is_scalar(item[0])
            if scalar:
                kwargs = dict(indent=0, pad=' ', map_value=False)
                if comment is not None or vtype is not None:
                    self.file.write(' ')
            else:
                self.file.write('\n')
                kwargs = dict(indent=indent, pad=pad, map_value=False)
            for value in item:
                self.write_value(value, **kwargs)
                if scalar:
                    kwargs['indent'] = 1 # 0 for first item
            tab = pad * (indent - 1)
            self.file.write(']\n' if scalar else f'{tab}]\n')
        return True


    def write_map(self, item, indent=0, *, pad, map_value=False):
        tab = '' if map_value else pad * indent
        comment = getattr(item, 'comment', None)
        ktype = getattr(item, 'ktype', None)
        vtype = getattr(item, 'vtype', None)
        if len(item) == 0:
            self.file.write(f'{tab}{{')
            if comment is not None:
                self.file.write(f' #<{escape(comment)}>')
            if ktype is not None:
                self.file.write(f' {ktype}')
            if vtype is not None:
                self.file.write(f' {vtype}')
            if (comment is not None or ktype is not None or
                    vtype is not None):
                self.file.write(' ')
            self.file.write('}\n')
        elif len(item) == 1:
            self.file.write(f'{tab}{{')
            if comment is not None:
                self.file.write(f' #<{escape(comment)}>')
            if ktype is not None:
                self.file.write(f' {ktype}')
            if vtype is not None:
                self.file.write(f' {vtype}')
            key, value = list(item.items())[0]
            self.write_scalar(key, 1, pad=' ')
            self.file.write(' ')
            self.write_value(value, 1, pad=' ', map_value=True)
            self.file.write('}\n')
        else:
            self.file.write(f'{tab}{{')
            if comment is not None:
                self.file.write(f' #<{escape(comment)}>')
            if ktype is not None:
                self.file.write(f' {ktype}')
            if vtype is not None:
                self.file.write(f' {vtype}')
            self.file.write('\n')
            indent += 1
            for key, value in item.items():
                self.write_scalar(key, indent, pad=pad)
                self.file.write(' ')
                if not self.write_value(value, indent, pad=pad,
                                        map_value=True):
                    self.file.write('\n')
            tab = pad * (indent - 1)
            self.file.write(f'{tab}}}\n')
        return True


    def write_table(self, item, indent=0, *, pad, map_value=False):
        tab = '' if map_value else pad * indent
        comment = getattr(item, 'comment', None)
        self.file.write(f'{tab}(')
        if comment is not None:
            self.file.write(f' #<{escape(comment)}> ')
        self.file.write(item.ttype.name)
        if len(item) == 0:
            self.file.write(')')
            return False
        elif len(item) == 1:
            self.file.write(' ')
            self.write_record(item[0], map_value)
            self.file.write(')')
            return False
        else:
            self.file.write('\n')
            indent += 1
            for record in item:
                self.file.write(pad * indent)
                self.write_record(record, map_value)
                self.file.write('\n')
            tab = pad * (indent - 1)
            self.file.write(f'{tab})\n')
            return True


    def write_record(self, record, map_value):
        sep = ''
        for value in record:
            self.file.write(sep)
            self.write_value(value, 0, pad='', map_value=map_value)
            sep = ' '


    def write_scalar(self, item, indent=0, *, pad, map_value=False):
        if not map_value:
            self.file.write(pad * indent)
        if item is None:
            self.file.write('?')
        elif isinstance(item, bool):
            self.file.write(self.yes if item else self.no)
        elif isinstance(item, (int, float)):
            self.file.write(str(item))
        elif isinstance(item, (datetime.date, datetime.datetime)):
            self.file.write(item.isoformat())
        elif isinstance(item, str):
            self.file.write(f'<{escape(item)}>')
        elif isinstance(item, bytes):
            self.file.write(f'(:{item.hex().upper()}:)')
        elif isinstance(item, bytearray):
            if not self.one_way_conversion:
                raise Error('can only convert bytearray to bytes if '
                            'one_way_conversion is True')
            self.file.write(f'(:{item.hex().upper()}:)')
        else:
            print(f'error: ignoring unexpected item of type {type(item)}: '
                  f'{item!r}', file=sys.stderr)
        return False


def is_scalar(x):
    return x is None or isinstance(
        x, (bool, int, float, datetime.date, datetime.datetime, str, bytes,
            bytearray))


def _type_for_name(typename):
    return dict(bool=bool, bytes=(bytes, bytearray), date=datetime.date,
                datetime=datetime.datetime, int=int, list=List, map=Map,
                real=float, str=str, table=Table).get(typename)


def _name_for_type(vtype):
    return {bool: 'bool', bytearray: 'bytes', bytes: 'bytes',
            datetime.date: 'date', datetime.datetime: 'datetime',
            float: 'real', int: 'int', List: 'list', Map: 'map',
            str: 'str', Table: 'table', type(None): '?'}.get(vtype)


def _maybe_fixtype(value, vtype, *, check=False, fixtypes=False):
    '''Returns value (possibly fixed), fixed (bool), err (None or Error)'''
    if (vtype is None or value is None or check is False or
            isinstance(value, vtype)):
        return value, False, None
    if fixtypes:
        new_value, fixed = _try_fixtype(value, vtype)
        if fixed:
            return new_value, True, None
    if check:
        expected = _name_for_type(vtype)
        actual = _name_for_type(type(value))
        err = Error(f'expected value of type {expected}, got value '
                    f'{value!r} of type {actual}')
        return value, False, err


def _try_fixtype(value, outtype):
    if isinstance(outtype, str):
        return str(value), True
    vclass = type(value)
    if isinstance(vclass, str) and isinstance(outtype, (
            bool, int, float, datetime.date, datetime.datetime)):
        new_value = naturalize(value)
        return new_value, isinstance(new_value, outtype)
    if isinstance(vclass, int) and isinstance(outtype, float):
        return float(value), True
    if isinstance(vclass, float) and isinstance(outtype, int):
        return int(value), True
    return value, False


def naturalize(s):
    '''Given string s returns True if the string is 't', 'true', 'y', 'yes',
    or False if the string is 'f', 'false', 'n', 'no' (case-insensitive), or
    an int if s holds a parsable int, or a float if s holds a parsable
    float, or a datetime.datetime if s holds a parsable ISO8601 datetime
    string, or a datetime.date if s holds a parsable ISO8601 date string, or
    failing these returns the string s unchanged.
    '''
    u = s.upper()
    if u in {'T', 'TRUE', 'Y', 'YES'}:
        return True
    if u in {'F', 'FALSE', 'N', 'NO'}:
        return False
    try:
        return int(s)
    except ValueError:
        try:
            return float(s)
        except ValueError:
            try:
                if 'T' in s:
                    if isoparse is not None:
                        return isoparse(s)
                    return datetime.datetime.fromisoformat(s)
                else:
                    if isoparse is not None:
                        return isoparse(s).date()
                    return datetime.date.fromisoformat(s)
            except ValueError:
                return s


def canonicalize(name, prefix='T_'):
    '''Given a name and an optional prefix, returns a name that is a valid
    table or field name. (See uxfconvert.py for uses.)'''
    cs = []
    for c in name:
        if c.isalnum() or c == '_':
            cs.append(c)
        elif c.isspace():
            if cs and cs[-1] != '_':
                cs.append('_')
    if cs and not cs[0].isupper() and cs[0].isalpha():
        cs[0] = cs[0].upper()
    s = ''.join(cs)
    if prefix and not prefix[0].isupper() and prefix[0].isalpha():
        prefix[0] = prefix[0].upper()
    if not s or not s[0].isupper():
        s = prefix + s
    if not s or not s[0].isupper():
        s = f'T{id(s)}'
    return s[:MAX_IDENTIFIER_LEN]


if __name__ == '__main__':
    import os

    if len(sys.argv) < 2 or sys.argv[1] in {'-h', '--help', 'help'}:
        raise SystemExit('''\
usage: uxf.py \
[-c|--check] [-f|--fix-types] [-w|--warn-is-error] [-iN|--indent=N] \
<infile.uxf[.gz]> [<outfile.uxf[.gz]>]
   or: python3 -m uxf ...same options as above...

If check is set any given types are checked against the actual \
values and warnings given if appropriate.
If fixtypes is set mistyped values are correctly typed where possible \
(e.g., int ↔ float, str → date, etc.). If fixtypes is set then check is \
automatically set too.
If warn-is-error is set warnings are treated as errors \
(i.e., the program will terminate with the first error or warning message).
If an outfile is specified and ends .gz it will be gzip-compressed.
Indent defaults to 2 and accepts a range of 0-8. \
The default is silently used if an out of range value is given.

To get an uncompressed .uxf file run: `uxf.py infile.uxf.gz outfile.uxf` or
simply `gunzip infile.uxf.gz`.

To produce a compressed and compact .uxf file run: \
`uxf.py -i0 infile.uxf outfile.uxf.gz`

Converting uxf to uxf will alphabetically order any ttypes.
''')
    check = False
    fixtypes = False
    warn_is_error = False
    indent = 2
    args = sys.argv[1:]
    infile = outfile = None
    for arg in args:
        if arg in {'-c', '--check'}:
            check = True
        elif arg in {'-f', '--fix-types'}:
            fixtypes = True
            check = True
        elif arg in {'-w', '--warn-is-error'}:
            warn_is_error = True
        elif arg.startswith(('-i', '--indent=')):
            if arg[1] == 'i':
                indent = int(arg[2:])
            else:
                indent = int(arg[9:])
            if not 0 <= indent <= 9:
                indent = 2
        elif infile is None:
            infile = arg
        else:
            outfile = arg
    try:
        if (outfile is not None and os.path.abspath(infile) ==
                os.path.abspath(outfile)):
            raise Error('won\'t overwrite {outfile}')
        uxf_obj = load(infile, check=check, fixtypes=fixtypes,
                       warn_is_error=warn_is_error)
        outfile = sys.stdout if outfile is None else outfile
        dump(outfile, uxf_obj, indent=indent)
    except (FileNotFoundError, Error) as err:
        print(f'Error:{err}')

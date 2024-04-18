import typing
import enum
import re

from hiredict.types import HiRedictObject

# For reference: https://github.com/antirez/RESP3/blob/master/spec.md

class HiRedictTokenType(enum.IntEnum):
    SimpleString = 0
    SimpleError = 1
    Integer = 2
    BulkString = 3
    Array = 4
    ArrayItem = 5
    Null = 6
    Boolean = 7
    Double = 8
    BigNumber = 9
    BulkError = 10
    VerbatimString = 11
    Map = 11
    MapKey = 12
    MapValue = 13
    Set = 14
    SetItem = 15
    Push = 16

class HiRedictToken():
    
    __slots__ = (
        "_type",
        "_value"
    )

    _type: HiRedictTokenType
    _value: str

    def __init__(self, tokenType: HiRedictTokenType, tokenValue: str) -> None:
        self._type = tokenType
        self._value = tokenValue
        
    def __str__(self) -> str:
        return f"HiRedictToken({self._type}, \"{self._value}\")"

    @property
    def type(self) -> HiRedictTokenType:
        return self._type
    
    @property 
    def value(self) -> str:
        return self._value

class HiRedictTokenPattern():
    
    __slots__ = (
        "_regex",
        "_tokenType"
    )

    _regex: re.Pattern
    _tokenType: HiRedictTokenType

    def __init__(self,
                 pattern: str,
                 tokenType: HiRedictTokenType) -> None:
        self._regex = re.compile(pattern)
        self._tokenType = tokenType

    @property
    def tokenType(self) -> HiRedictTokenType:
        return self._tokenType
    
    def match(self, string: str) -> typing.Optional[re.Match]:
        return self._regex.match(string)

_PATTERNS = (
    HiRedictTokenPattern("\+(.+)\r\n", HiRedictTokenType.SimpleString),
    HiRedictTokenPattern("\-(.+)\r\n", HiRedictTokenType.SimpleError),
    HiRedictTokenPattern(":(\-?\+?[0-9]+)\r\n", HiRedictTokenType.Integer),
    HiRedictTokenPattern("$\"?(.+)\"?\r\n", HiRedictTokenType.BulkString),
    HiRedictTokenPattern("*(.+)\r\n", HiRedictTokenType.SimpleString),
    HiRedictTokenPattern("+(.+)\r\n", HiRedictTokenType.SimpleString),
    HiRedictTokenPattern("+(.+)\r\n", HiRedictTokenType.SimpleString),
    HiRedictTokenPattern("+(.+)\r\n", HiRedictTokenType.SimpleString),
    HiRedictTokenPattern("+(.+)\r\n", HiRedictTokenType.SimpleString),
    HiRedictTokenPattern("+(.+)\r\n", HiRedictTokenType.SimpleString),
    HiRedictTokenPattern("+(.+)\r\n", HiRedictTokenType.SimpleString),
    HiRedictTokenPattern("+(.+)\r\n", HiRedictTokenType.SimpleString),
    HiRedictTokenPattern("+(.+)\r\n", HiRedictTokenType.SimpleString),
    HiRedictTokenPattern("+(.+)\r\n", HiRedictTokenType.SimpleString),
    HiRedictTokenPattern("+(.+)\r\n", HiRedictTokenType.SimpleString),
    HiRedictTokenPattern("+(.+)\r\n", HiRedictTokenType.SimpleString),
)

class HiRedictParser():

    __slots__ = (
        "_protocol",
        "_patterns"
    )

    _protocol: int
    _patterns: typing.List[HiRedictTokenPattern]
    
    def __init__(self, protocol: int = 2) -> None:
        self._protocol = protocol
        self._patterns

    def _lex(self, data: bytes) -> typing.List[HiRedictToken]:
        tokens = list()
        
        return tokens
        pass

    def parse(self, data: bytes) -> HiRedictObject:
        pass
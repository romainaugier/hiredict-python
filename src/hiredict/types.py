import typing
import weakref
import enum

class HiRedictContext():
    pass

class HiRedictObject():
    
    def __init__(self, ctx: HiRedictContext, name: str) -> None:
        self._ctx = weakref.ref(ctx)
        self._name = name

class HiRedictListPushMode(enum.IntEnum):
    LEFT = 0
    RIGHT = 1

class HiRedictListPopMode(enum.IntEnum):
    LEFT = 0
    RIGHT = 1
        
class HiRedictList():

    def __len__(self) -> int:
        pass
    
    def __getitem__(self, index: int) -> typing.Any:
        pass

    def __setitem__(self, index: int, v: typing.Any) -> None:
        pass

    def items(self) -> typing.List[typing.Any]:
        pass

    def push(self,
             v: typing.Any,
             mode: HiRedictListPushMode = HiRedictListPushMode.RIGHT) -> bool:
        pass

    def pushMany(self,
                 v: typing.Iterable,
                 mode: HiRedictListPushMode = HiRedictListPushMode.RIGHT) -> bool:
        pass

    def pop(self,
            mode: HiRedictListPopMode = HiRedictListPopMode.RIGHT) -> typing.Any:
        pass

    def popMany(self,
                mode: HiRedictListPopMode = HiRedictListPopMode.RIGHT) -> typing.List[typing.Any]:
        pass

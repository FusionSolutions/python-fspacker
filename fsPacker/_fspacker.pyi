# Builtin modules
from typing import Any, Tuple, IO
# Third party modules
# Local modules
# Program
class PackerError(Exception): ...
class PackingError(PackerError): ...
class UnpackingError(PackerError): ...

def dumps(data:Any, *, version:int=..., recursiveLimit:int=...) -> bytes: ...
def dump(data:Any, file:IO[bytes], *, version:int=..., recursiveLimit:int=...) -> None: ...
def loads(data:bytes, maxIndexSize:int=..., recursiveLimit:int=...) -> Tuple[int, Any]: ...
def load(file:IO[bytes], maxIndexSize:int=..., recursiveLimit:int=...) -> Tuple[int, Any]: ...

"""
This type stub file was generated by pyright.
"""

from typing import Any, Callable, Dict, List, ParamSpec, TypeVar


logger = ...
class Data:
    alpha_2: str
    name: str

    def __init__(self, **fields) -> None:
        ...
    
    def __getattr__(self, key):
        ...
    
    def __setattr__(self, key, value): # -> None:
        ...
    
    def __repr__(self): # -> str:
        ...
    
    def __dir__(self): # -> list[str]:
        ...
    
P = ParamSpec("P")
R = TypeVar("R")

def lazy_load(f: Callable[P, R]) -> Callable[P, R]: # -> (self: Unknown, *args: Unknown, **kw: Unknown) -> Unknown:
    ...

class Database:
    data_class_base = Data
    data_class_name: str = ...
    root_key: str = ...
    no_index: List[str] = ...
    def __init__(self, filename: str) -> None:
        ...
    
    @lazy_load
    def __iter__(self): # -> Iterator[Unknown]:
        ...
    
    @lazy_load
    def __len__(self): # -> int:
        ...
    
    @lazy_load
    def get(self, name: str = ..., alpha_2: str = ..., **kw: Dict[Any, Any]) -> Data:
        ...
    
    @lazy_load
    def lookup(self, value: str) -> Data:
        ...
    



from abc import abstractmethod
from functools import wraps
from importlib.util import find_spec
from pathlib import Path
from typing import Collection, Any, Mapping, Type, Tuple, ParamSpec, TypeVar, Callable, Iterator, Protocol

from .typing import DataTable, DataStructure, ParsedDataRow, ParsedDataTable, ParsedDataStructure


class Serializer:
    @abstractmethod
    def write_table(self, table: DataTable, fp: Path | str, headers: Collection[str] = None, default: Any = None,
                    **serializer_kwargs) -> None:
        raise NotImplementedError

    @abstractmethod
    def append_table(self, table: DataTable, fp: Path | str, headers: Collection[str] = None, default: Any = None,
                     **serializer_kwargs) -> None:
        raise NotImplementedError

    @abstractmethod
    def dump(self, structure: DataStructure, fp: Path | str, schema: Mapping[str, Collection[str]], default: Any = None,
             **serializer_kwargs) -> None:
        raise NotImplementedError

    @abstractmethod
    def iter_table(self, fp: Path | str, constructor: Type = None, default: Any = None,
                   **parser_kwargs) -> Iterator[ParsedDataRow]:
        raise NotImplementedError

    @abstractmethod
    def iter_structure(self, fp: Path | str, constructor: Type = None, default: Any = None,
                       **parser_kwargs) -> Iterator[Tuple[str, ParsedDataRow]]:
        raise NotImplementedError

    @abstractmethod
    def read_table(self, fp: Path | str, constructor: Type = None, default: Any = None,
                   **parser_kwargs) -> ParsedDataTable:
        raise NotImplementedError

    @abstractmethod
    def load(self, fp: Path | str, constructor: Type = None, default: Any = None,
             **parser_kwargs) -> ParsedDataStructure:
        raise NotImplementedError

    @abstractmethod
    def read_headers(self, fp: Path | str, **parser_kwargs) -> Collection[str]:
        pass

    @abstractmethod
    def read_schema(self, fp: Path | str, **parser_kwargs) -> Mapping[str, Collection[str]]:
        pass

import dataclasses
from typing import Dict, Any, Mapping, List, Iterable, Tuple, ClassVar, Protocol


class DataClass(Protocol):
    __dataclass_fields__: ClassVar[Dict[str, 'dataclasses.Field']]
    __dataclass_params__: ClassVar[Any]


# Generic data structures
DataRow = Mapping[str, Any] | DataClass
DataTable = Iterable[DataRow]
DataStructure = Iterable[Tuple[str, DataTable]] | Mapping[str, DataTable]


# Output data structures
ParsedDataRow = Dict[str, Any] | DataClass
ParsedDataTable = List[ParsedDataRow]
ParsedDataStructure = Mapping[str, ParsedDataTable]

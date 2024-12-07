from typing import ClassVar, Generic, TypeVar

from pydantic import BaseModel

TModel = TypeVar('TModel')


class BaseClickPyQuery(BaseModel, Generic[TModel]):
    Model: ClassVar[type[TModel]]  # type: ignore
    QUERY: ClassVar[str]

    def query(self) -> str:
        return self.QUERY.format(**self.__dict__)

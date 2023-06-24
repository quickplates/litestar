from abc import ABC, abstractmethod
from typing import Generic, TypeVar

T = TypeVar("T")


class Builder(ABC, Generic[T]):
    """Base class for builders."""

    @abstractmethod
    def build(self) -> T:
        pass

    def __call__(self) -> T:
        return self.build()

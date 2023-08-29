from abc import ABC, abstractmethod


class GraphicObject(ABC):

    def __init__(self, name: str) -> None:
        self.name = name

    @abstractmethod
    def get_points(self) -> list['Point']:
        pass

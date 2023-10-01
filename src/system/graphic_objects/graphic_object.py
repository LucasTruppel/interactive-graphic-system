from abc import ABC, abstractmethod


class GraphicObject(ABC):

    def __init__(self, name: str, color: str) -> None:
        self.name = name
        self.color = color

    @abstractmethod
    def get_points(self) -> list['Point']:
        pass

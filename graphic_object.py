from abc import ABC, abstractmethod


class GraphicObject:

    def __init__(self, name: str):
        self.name = name

    @abstractmethod
    def get_points(self):
        pass

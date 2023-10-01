from enum import Enum


class PointClippingState(Enum):
    ENABLED = 1
    DISABLED = 2


class LineClippingState(Enum):
    COHEN_SUTHERLAND = 1
    LIANG_BARSKY = 2
    DISABLED = 3


class PolygonClippingState(Enum):
    SUTHERLAND_HODGMAN = 1
    DISABLED = 2

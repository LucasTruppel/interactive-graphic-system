from enum import Enum


class ClippingState(Enum):
    pass


class PointClippingState(ClippingState):
    ENABLED = 1
    DISABLED = 2


class LineClippingState(ClippingState):
    COHEN_SUTHERLAND = 1
    LIANG_BARSKY = 2
    DISABLED = 3


class PolygonClippingState(ClippingState):
    SUTHERLAND_HODGMAN = 1
    DISABLED = 2

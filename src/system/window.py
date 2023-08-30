class Window:

    def __init__(self, x_min: float, y_min: float, x_max: float, y_max: float) -> None:
        self.x_min = x_min
        self.y_min = y_min
        self.x_max = x_max
        self.y_max = y_max

    def move_up(self) -> None:
        shift = 0.2*abs(self.y_max - self.y_min)
        self.y_min += shift
        self.y_max += shift

    def move_down(self) -> None:
        shift = 0.2 * abs(self.y_max - self.y_min)
        self.y_min -= shift
        self.y_max -= shift

    def move_left(self) -> None:
        shift = 0.2 * abs(self.x_max - self.x_min)
        self.x_min -= shift
        self.x_max -= shift

    def move_right(self) -> None:
        shift = 0.2 * abs(self.x_max - self.x_min)
        self.x_min += shift
        self.x_max += shift

    def zoom_in(self) -> None:
        x_dif = 0.1 * abs(self.x_max - self.x_min)
        self.x_min += x_dif
        self.x_max -= x_dif
        y_dif = 0.1 * abs(self.y_max - self.y_min)
        self.y_min += y_dif
        self.y_max -= y_dif

    def zoom_out(self) -> None:
        x_dif = 0.1 * abs(self.x_max - self.x_min)
        self.x_min -= x_dif
        self.x_max += x_dif
        y_dif = 0.1 * abs(self.y_max - self.y_min)
        self.y_min -= y_dif
        self.y_max += y_dif

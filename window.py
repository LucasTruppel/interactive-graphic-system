class Window:

    def __init__(self, x_min, y_min, x_max, y_max):
        self.x_min = x_min
        self.y_min = y_min
        self.x_max = x_max
        self.y_max = y_max

    def move_up(self):
        shift = int(0.2*abs(self.y_max - self.y_min))
        self.y_min += shift
        self.y_max += shift

    def move_down(self):
        shift = int(0.2 * abs(self.y_max - self.y_min))
        self.y_min -= shift
        self.y_max -= shift

    def move_left(self):
        shift = int(0.2 * abs(self.x_max - self.x_min))
        self.x_min -= shift
        self.x_max -= shift

    def move_right(self):
        shift = int(0.2 * abs(self.x_max - self.x_min))
        self.x_min += shift
        self.x_max += shift

    def zoom_in(self):
        x_dif = int(0.1 * abs(self.x_max - self.x_min))
        self.x_min += x_dif
        self.x_max -= x_dif
        y_dif = int(0.1 * abs(self.y_max - self.y_min))
        self.y_min += y_dif
        self.y_max -= y_dif

    def zoom_out(self):
        x_dif = int(0.1 * abs(self.x_max - self.x_min))
        self.x_min -= x_dif
        self.x_max += x_dif
        y_dif = int(0.1 * abs(self.y_max - self.y_min))
        self.y_min -= y_dif
        self.y_max += y_dif


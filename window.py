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
        self.x_max -= int(0.2 * abs(self.x_max - self.x_min))
        self.y_max -= int(0.2 * abs(self.y_max - self.y_min))

    def zoom_out(self):
        self.x_max += int(0.2 * abs(self.x_max - self.x_min))
        self.y_max += int(0.2 * abs(self.y_max - self.y_min))


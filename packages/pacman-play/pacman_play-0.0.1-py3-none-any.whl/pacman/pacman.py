D_UP = 0
D_DOWN = 1
D_LEFT = 2
D_RIGHT = 3

CH_UP = "U"
CH_DOWN = b"\xe2\x88\xa9"
CH_LEFT = b"\xe2\x86\x84"
CH_RIGHT = "C"


class Pacman:
    """
    The little thing that eats.
    """

    def __init__(self, x, y, w, h, d):
        """
        Initialize pacman.

        :param x, y: Initial position.
        :param w, h: Screen dimensions.
        :param d: Direction. Use constant D_UP, etc.
        """
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.d = d

    def char(self):
        """
        Get unicode character that represents this pacman.
        e.g. "C" for right, "U" for up, etc.
        """
        if self.d == D_UP:
            return CH_UP
        if self.d == D_DOWN:
            return CH_DOWN
        if self.d == D_LEFT:
            return CH_LEFT
        if self.d == D_RIGHT:
            return CH_RIGHT

    def step(self):
        """
        Move the pacman in the direction.
        Wraps around if goes out of bounds.
        """
        if self.d == D_UP:
            self.y -= 1
        if self.d == D_DOWN:
            self.y += 1
        if self.d == D_LEFT:
            self.x -= 1
        if self.d == D_RIGHT:
            self.x += 1

        if self.x < 0:
            self.x = self.w - 1
        if self.x >= self.w:
            self.x = 0
        if self.y < 0:
            self.y = self.h - 1
        if self.y >= self.h:
            self.y = 0

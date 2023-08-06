from coopstructs.vectors import Vector2

class Rectangle:
    def __init__(self, x, y, height, width):
        self.x = x
        self.y = y
        self.height = height
        self.width = width

    def points_tuple(self):
        return ((self.x, self.y), (self.x + self.width, self.y), (self.x + self.width, self.y + self.height),
                (self.x, self.y + self.height))

    @property
    def center(self) -> Vector2:
        return Vector2(self.x + self.width / 2, self.y + self.height / 2)

    def __str__(self):
        return f"TopLeft: <{self.x}, {self.y}>, Size: H{self.height} x W{self.width}"








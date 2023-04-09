 #By:
 	# Anuja Patil , Neethu Duggi , Vishwa Patel , Apurva Ratnaparkhi

from typing import Union
from dataclasses import dataclass

@dataclass
class Vector2:
    x: float = 0
    y: float = 0

    @property
    def sqrMagnitude(self):
        return self.x ** 2 + self.y ** 2

    @property
    def magnitude(self):
        return self.sqrMagnitude ** 0.5

    def normalise(self):
        return self / self.magnitude

    def __iter__(self):
        yield self.x
        yield self.y

    def __add__(self, other: "Vector2"):
        return Vector2(self.x + other.x, self.y + other.y)

    def __sub__(self, other: "Vector2"):
        return Vector2(self.x - other.x, self.y - other.y)

    def __mul__(self, other: Union["Vector2", int, float]):
        if isinstance(other, Vector2):
            return Vector2(self.x * other.x, self.y * other.y)
        else:
            return Vector2(self.x * other, self.y * other)         

    def __mod__(self, other: Union["Vector2", int, float]):
        if isinstance(other, Vector2):
            return Vector2(self.x % other.x, self.y % other.y)
        else:
            return Vector2(self.x % other, self.y % other)            

    def __pow__(self, other: Union["Vector2", int, float]):
        if isinstance(other, Vector2):
            return Vector2(self.x ** other.x, self.y ** other.y)
        else:
            return Vector2(self.x ** other, self.y ** other)


    def __truediv__(self, other: Union["Vector2", int, float]):
        if isinstance(other, Vector2):
            return Vector2(self.x / other.x, self.y / other.y)
        else:
            return Vector2(self.x / other, self.y / other)

    def __floordiv__(self, other: Union["Vector2", int, float]):
        if isinstance(other, Vector2):
            return Vector2(self.x // other.x, self.y // other.y)
        else:
            return Vector2(self.x // other, self.y // other)


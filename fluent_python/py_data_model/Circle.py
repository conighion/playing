import math
from functools import cached_property  # available with python 3.9 and greater.


class LazyProperty:
    def __init__(self, func):
        self.func = func

    def __get__(self, instance, cls):
        if instance is None:
            return self
        else:
            value = self.func(instance)
            setattr(instance, self.func.__name__, value)
            return value


class Circle:
    def __init__(self, radius):
        self.radius = radius

    @LazyProperty
    def area(self):
        print('Computing area')
        return math.pi * self.radius ** 2

    @LazyProperty
    def perimeter(self):
        print('Computing perimeter')
        return 2 * math.pi * self.radius


class Square:
    def __init__(self, side=1):
        self.side = side

    @cached_property
    def area(self):
        print('Computing area')
        return self.side ** 2

    @cached_property
    def perimeter(self):
        print('Computing perimeter')
        return self.side * 4

    def __repr__(self):
        return f'Square({self.side!r})'


# Cached properties. Note that it calculates the area only the first time. Then it is an attribute.
circle = Circle(4)
print(circle.area)
print(circle.area)

# Lazy properties are build in functools from python >=3.9
square = Square(5)
print(square.area)
print(square.area)

# If I change the side of the square though the area is not updated when is called again
square.side = 12
print(square.area)

# Same for the LazyProperty implementation
circle.radius = 40
circle.area


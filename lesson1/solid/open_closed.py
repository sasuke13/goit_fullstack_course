import math

class Rect:
    def __init__(self, width, height):
        self.width = width
        self.height = height
    
    def area(self):
        return self.width * self.height

class Circle:
    def __init__(self, radius):
        self.radius = radius
    
    def area(self):
        return self.radius * self.radius * math.pi


def total_area(shapes):
    sum = 0
    for el in shapes:
        sum += el.area()
    return sum


if __name__ == '__main__':
    shapes = [Rect(10, 10), Rect(4, 5), Circle(3)]
    area = total_area(shapes)
    print(area)
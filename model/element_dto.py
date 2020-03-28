class Element:
    def __init__(self, locator, x, y, width, height):
        self.locator = locator
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def position(self):
        return self.x, self.y

    def size(self):
        return self.width, self.height

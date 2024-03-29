class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def manhattan_distance(self, other):
        return abs(self.x - other.x) + abs(self.y - other.y)

    def __str__(self):
        return "(%s,%s)" % (self.x, self.y)

    def __repr__(self):
        return "(%s,%s)" % (self.x, self.y)

    def __add__(self, other):
        return Point(self.x + other.x, self.y + other.y)

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __hash__(self):
        return hash("%s" % self)


def process_wire(wire):
    current = Point(0, 0)
    path = [current]
    for action_infos in wire:
        action_type, distance = action_infos[0], int(action_infos[1:])
        if action_type == "R":
            offset = Point(1, 0)
        elif action_type == "L":
            offset = Point(-1, 0)
        elif action_type == "U":
            offset = Point(0, 1)
        else:
            offset = Point(0, -1)
        for _ in range(distance):
            current = current + offset
            path.append(current)
    return path

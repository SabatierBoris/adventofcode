class Node:
    def __init__(self, name, orbit=None):
        self.name = name
        self.orbit = orbit
        self.__distance = None

    def distance(self):
        if self.__distance is not None:
            return self.__distance

        if self.orbit is None:
            self.__distance = 0
        else:
            self.__distance = 1 + self.orbit.distance()
        return self.__distance

    def distance_with(self, other):
        if self.orbit == other.orbit:
            return 0

        print(
            "%s(%s) <-> %s(%s)"
            % (self.name, self.distance(), other.name, other.distance())
        )

        if self.distance() > other.distance():
            return 1 + self.orbit.distance_with(other)
        return 1 + self.distance_with(other.orbit)


def generate_tree(data):
    objects = {}

    for root, obj in data:
        if root not in objects:
            objects[root] = Node(root)
        if obj in objects:
            objects[obj].orbit = objects[root]
        else:
            objects[obj] = Node(obj, objects[root])

    return objects

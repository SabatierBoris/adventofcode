import random


class Droid:
    NORTH = 1
    SOUTH = 2
    WEST = 3
    EAST = 4

    def __init__(self, program):
        self.__program = program
        self.__last_action = None
        self.__previous_position = None
        self.__position = [0, 0]
        self.__maps = {}
        self.__oxygen_system = None
        self.__initial_position = [0, 0]
        for y in range(-19, 22):
            self.__maps[y] = {}
            for x in range(-21, 25):
                self.__maps[y][x] = " "
        self.__maps[0][0] = "."

    def send_action(self, code):
        self.__last_action = code
        self.__program.send_input(code)

    def move_north(self):
        self.send_action(Droid.NORTH)

    def move_south(self):
        self.send_action(Droid.SOUTH)

    def move_west(self):
        self.send_action(Droid.WEST)

    def move_east(self):
        self.send_action(Droid.EAST)

    def execute(self):
        self.__program.execute()

    def explore(self):
        print(self.__position)
        direction_distance = self.direction_distance_to_first_unkown(
            self.__position, []
        )
        if direction_distance is None:
            print("Finit !!!", self.__oxygen_system)
            print(self.distance(self.__initial_position, self.__oxygen_system))
            return False
        self.go_to(direction_distance[0])
        return True

    def distance(self, start, end):
        return self.min_direction_distance(start, end, [])[1]

    def min_direction_distance(self, current, target, previous_positions):
        direction_to_check = [Droid.NORTH, Droid.SOUTH, Droid.WEST, Droid.EAST]

        direction_distance = []
        for direction in direction_to_check:
            next_position = self.compute_next_position(direction, current)
            if next_position in previous_positions:
                # Already explore
                continue
            value = self.__maps.get(next_position[1], {}).get(next_position[0], None)
            if value == "#":
                # Dead end
                continue
            if next_position == target:
                return (0, direction)
            sub_distance = self.min_direction_distance(
                next_position, target, previous_positions + [current]
            )
            if sub_distance is None:
                # Dead end
                continue
            distance = sub_distance[1] + 1
            direction_distance.append((direction, distance))

        if len(direction_distance) == 0:
            return None
        return min(direction_distance, key=lambda a: a[1])

    def direction_distance_to_first_unkown(self, position, previous_positions):
        direction_to_check = [Droid.NORTH, Droid.SOUTH, Droid.WEST, Droid.EAST]

        direction_distance = []

        for direction in direction_to_check:
            next_position = self.compute_next_position(direction, position)
            if next_position in previous_positions:
                # Already explore
                continue
            value = self.__maps.get(next_position[1], {}).get(next_position[0], None)
            if value == "#":
                # Dead end
                continue

            distance = 0
            if value == ".":
                sub_distance = self.direction_distance_to_first_unkown(
                    next_position, previous_positions + [position]
                )
                if sub_distance is None:
                    # Dead end
                    continue
                distance = sub_distance[1] + 1
            direction_distance.append((direction, distance))

        if len(direction_distance) == 0:
            return None
        return min(direction_distance, key=lambda a: a[1])

    def go_to(self, direction):
        if direction == Droid.NORTH:
            self.move_north()
        elif direction == Droid.SOUTH:
            self.move_south()
        elif direction == Droid.WEST:
            self.move_west()
        else:
            self.move_east()

    def stay(self):
        self.go_to(self.__last_action)

    def display(self):
        for y, line in self.__maps.items():
            for x, value in line.items():
                if [x, y] == self.__position:
                    value = "D"
                print(value, end="")
            print("")

    def read_sensor(self):
        try:
            value = next(self.__program)
            if value == 0:  # WALL
                self.place("#")
            elif value == 1:  # Move Ok
                self.place(".")
                self.move()
            else:  # Move OK and oxygen system found
                self.place(".")
                self.__oxygen_system = self.compute_next_position()
                self.move()
                print("Oxygen system")
        except Exception:
            print("Sensor : ", "Error")
            pass

    def place(self, value):
        item_position = self.compute_next_position()
        if item_position[1] not in self.__maps:
            self.__maps[item_position[1]] = {}
        self.__maps[item_position[1]][item_position[0]] = value

    def move(self):
        self.__previous_position = list(self.__position)
        self.__position = self.compute_next_position()

    def compute_next_position(self, direction=None, position=None):
        if direction is None:
            direction = self.__last_action

        if position is None:
            position = self.__position

        if direction == 1:
            return [position[0], position[1] + 1]
        elif direction == 2:
            return [position[0], position[1] - 1]
        elif direction == 3:
            return [position[0] - 1, position[1]]
        else:
            return [position[0] + 1, position[1]]

    def is_running(self):
        return self.__program.is_running()

    def init_oxygen(self):
        self.__position = None
        self.__maps[self.__oxygen_system[1]][self.__oxygen_system[0]] = "O"

    def expand_oxygen(self):
        new_oxygen_positions = []
        direction_to_check = [Droid.NORTH, Droid.SOUTH, Droid.WEST, Droid.EAST]
        for y, line in self.__maps.items():
            for x, value in line.items():
                if value != "O":
                    continue

                for direction in direction_to_check:
                    next_position = self.compute_next_position(direction, (x, y))

                    if self.__maps[next_position[1]][next_position[0]] == ".":
                        new_oxygen_positions.append(next_position)

        oxygen_expand = False
        for new_oxygen_position in new_oxygen_positions:
            oxygen_expand = True
            self.__maps[new_oxygen_position[1]][new_oxygen_position[0]] = "O"

        return oxygen_expand

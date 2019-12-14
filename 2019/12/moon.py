class Moon:
    def __init__(self, x, y, z):
        self.position = [x, y, z]
        self.velocity = [0, 0, 0]

    def update_velocity(self, other):
        for i in range(3):
            self.update_velocity_for_axe(other, i)

    def update_velocity_for_axe(self, other, axe):
        if self.position[axe] < other.position[axe]:
            self.velocity[axe] += 1
        elif self.position[axe] > other.position[axe]:
            self.velocity[axe] -= 1
        else:
            pass

    def move(self):
        for i in range(3):
            self.move_axe(i)

    def move_axe(self, axe):
        self.position[axe] += self.velocity[axe]

    def get_energy(self):
        return sum([abs(i) for i in self.position]) * sum(
            [abs(i) for i in self.velocity]
        )

    def __repr__(self):
        return "pos<x=%4d, y=%4d, z=%4d>, vel<x=%4d, y=%4d, z=%4d>" % (
            *self.position,
            *self.velocity,
        )

    def __eq__(self, other):
        return self.position == other.position and self.velocity == other.velocity

    def get_info(self, axe):
        return (self.position[axe], self.velocity[axe])

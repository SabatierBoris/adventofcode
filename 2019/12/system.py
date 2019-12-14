import re
from moon import Moon


class System:
    def __init__(self, datas):
        self.__moons = []

        r = r"^<x=(?P<x>-?\d+), y=(?P<y>-?\d+), z=(?P<z>-?\d+)>$"

        for data in datas:
            match = re.match(r, data)
            self.__moons.append(
                Moon(
                    int(match.group("x")), int(match.group("y")), int(match.group("z"))
                )
            )

    def update(self):
        for a in self.__moons:
            for b in self.__moons:
                a.update_velocity(b)

        for a in self.__moons:
            a.move()

    def update_axe(self, axe):
        for a in self.__moons:
            for b in self.__moons:
                a.update_velocity_for_axe(b, axe)

        for a in self.__moons:
            a.move_axe(axe)

    def __repr__(self):
        return "\n".join([str(m) for m in self.__moons])

    def get_energy(self):
        return sum([moon.get_energy() for moon in self.__moons])

    def find_loop(self):
        initial_state = [Moon(*m.position) for m in self.__moons]

        axe_infos = []
        for axe in range(3):
            previous_state = []
            current_state = self.get_state_for_axe(axe)
            i = 0
            while current_state not in previous_state:
                previous_state.append(current_state)
                self.update_axe(axe)
                i += 1
                current_state = self.get_state_for_axe(axe)

            axe_infos.append(i - previous_state.index(current_state))
            print(axe_infos)
        return axe_infos

    def get_state_for_axe(self, axe):
        return [m.get_info(axe) for m in self.__moons]

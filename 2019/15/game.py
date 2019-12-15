class Game:
    def __init__(self, program):
        self.__program = program
        self.__state = []
        self.__score = 0
        self.__ball_pos = (0, 0)
        self.__cursor_pos = (0, 0)
        self.__wait_input = False

    def execute(self):
        self.__program.execute()

    def update_state(self):
        x = 0
        y = 0
        i = 0
        for output in self.__program:
            i += 1
            if i == 1:
                x = output
            elif i == 2:
                y = output
            elif (x, y) == (-1, 0):
                self.__score = output
                i = 0
            else:
                if len(self.__state) <= y:
                    self.__state.append([])
                if len(self.__state[y]) <= x:
                    self.__state[y].append(0)
                if output == 4:
                    self.__ball_pos = (x, y)
                elif output == 3:
                    self.__cursor_pos = (x, y)
                self.__state[y][x] = output
                i = 0
        self.__wait_input = True

    def get_cursor_pos(self):
        return self.__cursor_pos

    def get_ball_pos(self):
        return self.__ball_pos

    def get_nb_of_block(self):
        i = 0
        for line in self.__state:
            for value in line:
                if value == 2:
                    i += 1
        return i

    def display(self):
        print("Score : %d" % (self.__score))
        for line in self.__state:
            for value in line:
                display = " "
                if value == 1:  # Wall
                    display = "#"
                elif value == 2:  # block
                    display = "X"
                elif value == 3:  # paddle
                    display = "-"
                elif value == 4:  # ball
                    display = "O"
                print(display, end="")
            print("")

    def move_left(self):
        self.__wait_input = False
        self.__program.send_input(-1)

    def move_right(self):
        self.__wait_input = False
        self.__program.send_input(1)

    def dont_move(self):
        self.__wait_input = False
        self.__program.send_input(0)

    def is_running(self):
        return self.__program.is_running()

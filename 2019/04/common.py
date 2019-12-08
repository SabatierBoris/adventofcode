def six_digit_filter(password):
    return password < 1000000


def six_digit_generator(passwords):
    for password in passwords:
        if six_digit_filter(password):
            yield password


def never_decrease_filter(password):
    previous = 10
    while password > 0:
        current = password % 10
        if previous < current:
            return False
        previous = current
        password //= 10
    return True


def never_decrease_generator(passwords):
    for password in passwords:
        if never_decrease_filter(password):
            yield password


def two_adjacent_filter(password):
    previous = None
    while password > 0:
        current = password % 10
        if previous == current:
            return True
        previous = current
        password //= 10
    return False


def two_adjacent_generator(passwords):
    for password in passwords:
        if two_adjacent_filter(password):
            yield password


def new_two_adjacent_filter(password):
    previous = None
    count = 0
    while password > 0:
        # print(password)
        current = password % 10
        if previous is not None and previous != current:
            if count == 2:
                return True
            count = 0
        count += 1
        previous = current
        password //= 10
    if count == 2:
        return True
    return False


def new_two_adjacent_generator(passwords):
    for password in passwords:
        if new_two_adjacent_filter(password):
            yield password

import random
import itertools

ROWS = 10
COLS = 10
ALL_POSITIONS = frozenset(itertools.product(range(COLS), range(ROWS)))
DIRECTIONS = {
    's': (0, -1),
    'j': (0, 1),
    'v': (1, 0),
    'z': (-1, 0),
}


def nakresli_mapu(coordinates, fruit):
    # list('abcd') -> ['a', 'b', 'c', 'd']
    # List Comprehensions - https://docs.python.org/3/tutorial/datastructures.html#list-comprehensions
    # [i for i in range(4)] -> [0, 1, 2, 3]
    game_plan = [list('.' * COLS) for _ in range(ROWS)]

    for col, row in coordinates[:-1]:
        game_plan[row][col] = 'x'  # tělo hada - malé x
    col, row = coordinates[-1]
    game_plan[row][col] = 'X'  # hlava hada - velké X

    for col, row in fruit:
        game_plan[row][col] = '?'

    for row in game_plan:
        print(' '.join(row))  # '<->'.join(['a', 'b', 'c']) -> 'a<->b<->c'


def pohyb(coordinates, direction, fruit):
    last = coordinates[-1]  # hlava hada
    vector = DIRECTIONS[direction]  # směr posunu, sever -> (0, -1)
    new = (last[0] + vector[0], last[1] + vector[1])  # nový čláek hada

    if (
            new in coordinates or
            new[0] < 0 or new[0] >= COLS or
            new[1] < 0 or new[1] >= ROWS
    ):
        raise ValueError('Game over')

    coordinates.append(new)
    if new in fruit:
        fruit.remove(new)
        if not fruit:  # přidej jen pokud není žádné ovoce na herním plánu
            generate_fruit(fruit, coordinates)
    else:
        coordinates.pop(0)


def generate_fruit(fruit, coordinates):
    fruit_set = set(fruit)
    coordinates_set = set(coordinates)

    # sety lze odečítat, všechny pozice - obaszené = volné
    free_positions = list((ALL_POSITIONS - fruit_set) - coordinates_set)

    # náhodne vyber jednu volnou pozici
    if free_positions:
        fruit.append(random.choice(free_positions))


def game():
    snake = [(0, 0), (1, 0), (2, 0)]
    fruit = []
    generate_fruit(fruit, snake)

    nakresli_mapu(snake, fruit)
    moves = 0
    while len(snake) < (ROWS * COLS):
        direction = input("Zadej směr [sjvz]: ")
        if direction not in DIRECTIONS:
            raise ValueError('Invalid direction')

        pohyb(snake, direction, fruit)
        moves += 1
        if moves % 30 == 0:
            generate_fruit(fruit, snake)

        nakresli_mapu(snake, fruit)
    print('Vítězství')


game()

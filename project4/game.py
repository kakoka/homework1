from classes import Storage, Player, Ships
from func import get_input_function

NUMBER_OF_SHIPS = [3, 2]#[4, 3, 3, 2, 2, 2, 1, 1, 1, 1]
input_function = get_input_function()

mnozhestvo = []
field = []
a = ''
b = '*'

def construct_ships(num):
    ship_coordinates = []

    x = int(input_function('X кордината: '))
    y = int(input_function('Y кордината: '))
    z = int(input_function('Ориентация, 0 - горизонтально, 1 - вертикально: '))

    if z == 0:
        ship_coordinates = [(x, y) for x in range(x, x + num)]
    if z == 1:
        ship_coordinates = [(x, y) for y in range(y, y + num)]

    print(ship_coordinates)
    mnozhestvo.append(ship_coordinates)

    return (ship_coordinates)

def construct_player(num):
    ship_coordinates = []

    name = input_function('Ваше имя: ')
    num = int(input_function('Номер: '))
    return (name, num)

def field_generation(field):
    field = [[a] * 10 for i in range(10)]
    return field

def print_field(field):
    print('0|', '1|', '2|', '3|', '4|', '5|', '6|', '7|', '8|', '9|')
    for i in range(10):
        # print('i')
        for j in range(10):
            print(' |', field[i][j], end='')
        print('')
    return

def place_ships():
    return

def main():
    f = field_generation(field)
    print_field(f)
    storage = Storage()
    #player 1 init

    player1 = input_function('Игрок 1 - Ваше имя: ')
    for i in NUMBER_OF_SHIPS:
        ship = Ships.construct(player1, construct_ships(i))
        storage.items.append(ship)

    # print('monozhestvo: ', mnozhestvo)
    player1 = Player.construct(player1, 1, mnozhestvo)
    storage.player.append(player1)
    player1.properties()
    #init end

    #mnozhestvo.clear()

    #player 2 init
    # player2 = input_function('Игрок 2 - Ваше имя: ')
    # for i in NUMBER_OF_SHIPS:
    #     ship = Ships.construct(player2, construct_ships(i))
    #     print_field(f)
    #     storage.items.append(ship)
    # player2 = Player.construct(player2, 1, mnozhestvo)
    # storage.player.append(player2)
    # print(mnozhestvo)



    ships = storage.items
    # active_players = storage.player
    #
    # print('под капотом player1\n')
    #player1.properties()
    print('Координаты кораблей player1: ', player1.pset)
    # d = player1.pset
    for i in range(len(player1.pset)):
        for j in range(len(player1.pset[i])):
            for q in range(len(player1.pset[i][j])):
                # for t in range(len(player1.pset[i][j][q])):
                Y = player1.pset[i][j][q][0]
                X = player1.pset[i][j][q][1]
                print('X: ', X, 'Y:', Y)
                f[X][Y] = '*'
    print_field(f)

    # print('под капотом player2\n')
    # player2.properties()

    # for index, plr in enumerate(active_players):
    #     if [plr for plr in plr if plr[index].name == player1.name is True]:
    #         plr.properties()

    # print(active_players)

    # print(players[1].pset)
    #players[2].properties()
    # print(player1.name)
    # print(ships[1].name)

    # for i in range(len(ships)):
    #     ships[i].properties()

    # for i in range(len(active_players)):
    #     active_players[i].properties()

    # # #
    # for index, shipp in enumerate(ships):
    #     if [shipp for shipp in ships if shipp[index].name == player1.name is True]:
    #         shipp.properties()

if __name__ == '__main__':
    main()

from termcolor import colored
from classes import Storage, Player, Ships
from func import get_input_function

#задаем количество кораблей списком, символы для вывода полей

NUMBER_OF_SHIPS = [4, 3, 3, 2, 2, 2, 1, 1, 1, 1]
a = ' '
b = 'O'
input_function = get_input_function()
mnozhestvo = []
field = [[a] * 10 for i in range(10)]

def input_xyz(num):

    '''проверка на корректность ввода '''
    # эта функция принимает на вход цифру, обозначающцую количество палуб на корабле
    # далее происходит ввод координат, и проверка на то, что эти координаты не буквы
    # если палуб больше 1, то добавляется ввод ориентации корабля

    st = False
    while st is False:
        try:
            try:
                x = int(input_function('X кордината: ')) - 1
                st = True
            except ValueError:
                print('Вы вели не число!')
                st = False
            try:
                y = int(input_function('Y кордината: ')) - 1
                st = True
            except ValueError:
                print('Вы ввели не число')
                st = False
            if num > 1:
                try:
                    z = int(input_function('Ориентация, горизонтально - 0, вертикально - 1 : '))
                    if z == 0 or z == 1:
                        st = True
                        return (x, y, z)
                    else:
                        st = False
                        raise IndexError
                except TypeError:  # ValueError:
                    print('0 или 1')
                    st = False
            else:
                st = True
                z = 0
                return(x, y, z)
        except:
            print('Not 0 or 1, try agian!')
            st = False
def construct_ships(num):
    '''эта функция конструирует корабли'''
    # на вход поступает количество палуб корабля
    # далее происходит проверка на
    # 1. выход за границы игрового поля
    # 2. наложение кораблей или пересечение кораблей
    # 3. нахождение кораблей рядом друг с другом

    ship_coordinates = []
    st = False
    while st is False:
        try:
            rt = input_xyz(num)
            x = rt[0]
            y = rt[1]

            #если палуб больше одной
            if num > 1:
                z = rt[2]
            else:
                z = 0

            # print(x)
            # except ValueError:
            #     print('wrong value')

            if x < 0 or x >= 10 or y < 0 or y >= 10 is True:
                 raise IndexError
            else:
                if z == 0:
                    ship_coordinates = [(x, y) for x in range(x, x + num)]
                elif z == 1: # and x >= 0 and x <= 10 and y >= 1 and y <= 10:
                    ship_coordinates = [(x, y) for y in range(y, y + num)]

            print(ship_coordinates)
            mnozhestvo.append(ship_coordinates)
            st = True
            return (ship_coordinates)
        except IndexError:
             print('Координаты выходят за границы поля, try again')

def construct_player(num):
    '''эта функция нужна для конструирование игроков'''
    ship_coordinates = []

    name = input_function('Ваше имя: ')
    num = int(input_function('Номер: '))
    return (name, num)

# def field_generation(field):
#     field = [[a] * 10 for i in range(10)]
#     return field


def print_field(field):
    '''функция вывода на экран игрового поля'''
    print('X:| 1| 2| 3| 4| 5| 6| 7| 8| 9|10|Y:')

    for i in range(10):
        print('  ', end = '')
        # print('| {} '.format(field[i][j]), end='')
        for j in range(10):
            # print(str.join('.', field[i][j]))
            print('| {}'.format(field[i][j]), end = '')
        print('| {}'.format(i+1))
    return

def place_ships():
    return

def print_ship_after_placement(field, ship):
    '''показ корабля после того как поставили его на поле'''
    for i in range(len(ship.xyz)):
        for j in range(len(ship.xyz[i])):
        # for q in range(len(player.pset[i][j])):
                # for t in range(len(player1.pset[i][j][q])):
            Y = ship.xyz[i][j][0]
            X = ship.xyz[i][j][1]
            print('X: ', X, 'Y:', Y)
            try:
                field[X][Y] = colored('O', 'yellow', 'on_green', attrs=['bold'])
            except IndexError:
                print('За границами игрового поля!')
    print_field(field)
    return

def main():

    f = field #field_generation(field)
    print_field(f)
    storage = Storage()
    #player 1 init
    COUNT = 0

    player1 = input_function('Игрок 1 - Ваше имя: ')
    for i in NUMBER_OF_SHIPS:
        ship = Ships.construct(player1, construct_ships(i))
        storage.items.append(ship)
        print_ship_after_placement(f, storage.items[COUNT])
        COUNT += 1
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

    #now its func

    # for i in range(len(player1.pset)):
    #     for j in range(len(player1.pset[i])):
    #         for q in range(len(player1.pset[i][j])):
    #             # for t in range(len(player1.pset[i][j][q])):
    #             Y = player1.pset[i][j][q][0]
    #             X = player1.pset[i][j][q][1]
    #             print('X: ', X, 'Y:', Y)
    #             f[X][Y] = colored('*', 'yellow', 'on_green', attrs=['bold'])
    # print_field(f)

    #end now

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

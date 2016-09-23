from termcolor import colored
import random
from classes import Storage, Player, Ships
from func import get_input_function

#задаем количество кораблей списком, символы для вывода полей

NUMBER_OF_SHIPS = [2, 2, 2]#[4, 3, 3, 2, 2, 2, 1, 1, 1, 1]
a = ' '
b = 'O'
input_function = get_input_function()
mnozhestvo = []
mnozhestvo_set_ships = set()
mnozhestvo_set_halo = set()
field = [[a] * 10 for i in range(10)]
halo_pattern_h = [0, 0, 1, 1, 1, 0, -1, -1, -1]
halo_pattern_v = [0, -1, -1, -1, 0, 1, 1, 1, 0]
halo_pattern = [-1, 0, 1]
halo = []
#COUNT = 0

def input_xyz_auto(num):
    '''бездушный робот генерит координаты случайным образом'''
    x = int((random.choice([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])) - 1)
    y = int((random.choice([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])) - 1)
    z = bool(random.choice([0, 1]))
    return(x, y, z)

def input_xyz(num):

    '''ручной ввод - проверка на корректность ввода '''
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
def construct_ships(num, l):
    '''эта функция конструирует корабли'''
    # на вход поступает количество палуб корабля
    # далее происходит проверка на
    # 1. выход за границы игрового поля
    # 2. наложение кораблей или пересечение кораблей
    # 3. нахождение кораблей рядом друг с другом
    #count = 0
    ship_coordinates = []
    st = False
    while st is False:
        try:
            rt = input_xyz_auto(num)
            x = rt[0]
            y = rt[1]
            z = rt[2]
            #настроено на робота (нет отрицательных значений и букв)
            if x + num > 10 or y + num > 10 or x + num > 10 and y + num> 10 is True:
                raise IndexError
            else:#запускаем мегапроверку

                #горизонтальная ориентация
                if z == 0:
                    ship_coordinates = [(x, y) for x in range(x, x + num)]
                    # проверка по горизонтали - halo
                    # мы ставим корабль только тогда, когда он не пересекается с другими и
                    # находится не зоне действия других кораблей
                    for i in ship_coordinates:

                        #print('one coord', i[0], 'second_coord', i[1])

                        # первый корабль на поле - заполняем halo
                        if l is 0:
                            print('счетчик!!!!!!!!!!!!!!!!!!', l)
                            print('Ставим первый корабль: ', ship_coordinates)
                            for d, z in [(d, z) for d in halo_pattern_h for z in halo_pattern_v]:
                                halo_x = i[0] + d
                                halo_y = i[1] + z
                                halo_pair = (halo_x, halo_y)
                                #halo.append(halo_pair)
                                mnozhestvo_set_halo.add(halo_pair)

                        # для всех следующих проверяем, попадают ли точки корабля в множество точек halo
                        # если нет - добавляем, если да, то просим переввести корабль
                        elif l is not 0:
                            print('счетчик!!!!!!!!!!!!!!!!!', l)
                            print('Координаты проверяемого корабля: ', ship_coordinates)
                            for q in ship_coordinates:
                                #print('Множество точек добавляемого корабля', q)
                                q = set(q)
                                print('fdsfsdfsdf',q)
                                # сравниваем попадают ли точки добавляемого корабля в множество halo имеющихся кораблей
                                # если не попадают, добавляем к множеству точек, точки нового корабля
                                if q not in mnozhestvo_set_halo:
                                #if mnozhestvo_set_halo.isdisjoint(q) is True:
                                    #print('результат сравнения для горизонтали: ', mnozhestvo_set_halo.isdisjoint(q))
                                    print('Не попадаем в множество')
                                    for d, z in [(d, z) for d in halo_pattern_h for z in halo_pattern_v]:
                                        halo_x = i[0] + d
                                        halo_y = i[1] + z
                                        halo_pair = (halo_x, halo_y)
                                        #halo.append(halo_pair)
                                        #if mnozhestvo_set_halo.isdisjoint(halo_pair) is False:
                                        mnozhestvo_set_halo.add(halo_pair)
                                # если попадают - ошибка!
                                elif q in mnozhestvo_set_halo:
                                #elif mnozhestvo_set_halo.isdisjoint(q) is False:
                                    #print('результат сравнения: ', q.isdisjoint(mnozhestvo_set_halo))
                                    #print('Попадаем на неправильные клетки! Надо переставить корабль')
                                    raise IndexError

                    #mnozhestvo_set_halo.add(halo_pair)
                #вертикальная ориентация
                elif z == 1:
                    ship_coordinates = [(x, y) for y in range(y, y + num)]
                    # проверка по вертикали - halo
                    # мы ставим корабль только тогда, когда он не пересекается с другими и
                    # находится не зоне действия других кораблей
                    for i in ship_coordinates:
                        #print('one coord', i[0], 'second_coord', i[1])
                        if l == 0:
                            for d, z in [(d, z) for d in halo_pattern_h for z in halo_pattern_v]:
                                #print('счетчик', l)
                                halo_x = i[0] + d
                                halo_y = i[1] + z
                                halo_pair = (halo_x, halo_y)
                                #halo.append(halo_pair)
                                mnozhestvo_set_halo.add(halo_pair)

                        # для всех следующих проверяем, попадают ли точки корабля в множество точек halo
                        # если нет - добавляем, если да, то просим переввести корабль
                        elif l != 0:
                            print('Координаты проверяемого корабля: ', ship_coordinates)
                            #print('счетчик', l)
                            for q in ship_coordinates:
                                #    q = ship_coordinates
                                #print('Множество точек добавляемого корабля', q)

                                # сравниваем попадают ли точки добавляемого корабля в множество halo имеющихся кораблей
                                if q not in mnozhestvo_set_halo:
                                #if mnozhestvo_set_halo.isdisjoint(q) is True:
                                    #print('результат сравнения: ', q.isdisjoint(mnozhestvo_set_halo))
                                    print('Не попадаем в множество')
                                    for d, z in [(d, z) for d in halo_pattern_h for z in halo_pattern_v]:
                                        halo_x = i[0] + d
                                        halo_y = i[1] + z
                                        halo_pair = (halo_x, halo_y)
                                        #halo.append(halo_pair)
                                        #if mnozhestvo_set_halo.isdisjoint(halo_pair) is False:
                                        mnozhestvo_set_halo.add(halo_pair)
    #                                   #mnozhestvo_set_halo.add(halo_pair)
                                elif q in mnozhestvo_set_halo:
                                #elif mnozhestvo_set_halo.isdisjoint(q) is False:
                                    #print('результат сравнения: ', q.isdisjoint(mnozhestvo_set_halo))
                                    #print('Попадаем! Надо переставить корабль')
                                    raise IndexError


            # список с координатами кораблей
            mnozhestvo.append(ship_coordinates)

            # множество с координатами кораблей
            #mnozhestvo_set_ships.add(ship_coordinates.)

            #print('ALL_SHIPS: множество координат кораблей', mnozhestvo_set_ships)
            print('ALL_SHIPS HALO: множество точек вокруг кораблей', mnozhestvo_set_halo, len(mnozhestvo_set_halo))

            #mnozhestvo_set_ships.

            st = True
            return (ship_coordinates)
        except IndexError:
            st = False
            print('Координаты выходят за границы поля, или корабли стоят рядом, try again')

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
            # X1 = X + 1
            # Y1 = Y + 1
            print('X: ', X, 'Y:', Y)
            try:
                field[X][Y] = 'O' #colored('O', 'yellow', 'on_green', attrs=['bold'])
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
    l = len(storage.items)
    print('колиичество кораблей', l)
    player1 = ('pasha')#input_function('Игрок 1 - Ваше имя: ')
    for i in NUMBER_OF_SHIPS:
        ship = Ships.construct(player1, construct_ships(i, l))
        storage.items.append(ship)
        l = len(storage.items)
        print('колиичество кораблей', l)
        print_ship_after_placement(f, storage.items[COUNT])
        COUNT += 1
    # print('monozhestvo: ', mnozhestvo)
    player1 = Player.construct(player1, 1, mnozhestvo)
    storage.player.append(player1)
    #player1.properties()
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

#from termcolor import colored

# Реализация игры для двух тупых роботов

import random
from classes import Storage, Player, Ships
from func import get_input_function

#задаем количество кораблей списком, символы для вывода полей

NUMBER_OF_SHIPS = [4, 3, 3, 2, 2, 2, 1, 1, 1, 1] #паттерн для создания кораблей
a = ' '
b = 'O'
input_function = get_input_function()
mnozhestvo = [] #множество кординат всех коралбей одного игрока
mnozhestvo_set_ships = set()
mnozhestvo_set_halo = [] #множество точек, окружиющие корабли, куда нельзя ставить другие корабли
halo_pattern_h = [-1, 0, 1]#[0, 0, 1, 1, 1, 0, -1, -1, -1]
halo_pattern_v = [1, 0, -1]#[0, -1, -1, -1, 0, 1, 1, 1, 0]
halo_pattern = [-1, 0, 1]
halo = []

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

    state = False
    while state is False:
        try:
            try:
                x = int(input_function('X кордината [1 - 10]: ')) - 1
                state = True
            except ValueError:
                print('Вы вели не число!')
                state = False
            try:
                y = int(input_function('Y кордината [1 - 10]: ')) - 1
                state = True
            except ValueError:
                print('Вы ввели не число, введите число в диапазоне от 1 до 10.')
                state = False
            if num > 1:
                try:
                    z = int(input_function('Ориентация, горизонтально - 0, вертикально - 1 [0, 1]: '))
                    if z == 0 or z == 1:
                        state = True
                        return (x, y, z)
                    else:
                        state = False
                        raise IndexError
                except TypeError:  # ValueError:
                    print('0 или 1')
                    state = False
            else:
                state = True
                z = 0
                return(x, y, z)
        except:
            print('Ошибка ввода, введите данные еще раз')
            state = False
def construct_ships(num, l):

    '''эта функция конструирует корабли и размещает их на поле'''
    # на вход поступает количество палуб корабля и длина списка storage.itmes в котором хранятся создаваемые корабли,
    # если список нулевой, то создаем корабли по списку.
    # Далее происходит проверка на:
    # 1. выход за границы игрового поля
    # 2. наложение кораблей или пересечение кораблей
    # 3. нахождение кораблей рядом друг с другом
    # Дабы не маятся с ручным вводом, все за нас делает тупой робот.

    ship_coordinates = []
    state = False
    while state is False:
        try:
            # получаем от робота координаты
            rt = input_xyz_auto(num)  #функция, которая генерит рандомные координаты
            x = rt[0] #координата x
            y = rt[1] #координата y
            z = rt[2] #z - ориентация 0 - горизонтально, 1 - вертикально

            #эта проверка настроена на робота, который генерирует не отрицательные целые числа)
            #для человека - проверка на значение еще будет включать проверку на знак числа

            if x + num > 10 or y + num > 10 or x + num > 10 and y + num > 10 is True:
                raise IndexError
            else:
                #запускаем мегапроверку

                #для горизонтальной ориентация корабля
                if z is False:
                    ship_coordinates = [(x, y) for x in range(x, x + num)]
                    # проверка по горизонтали - halo
                    # мы ставим корабль только тогда, когда он не пересекается с другими кораблями и
                    # находится не зоне действия других кораблей
                    for i in ship_coordinates:
                        # первый корабль на поле - заполняем halo - окружение
                        if l is 0:
                            for d, z in [(d, z) for d in halo_pattern_h for z in halo_pattern_v]:
                                halo_x = i[0] + d
                                halo_y = i[1] + z
                                halo_pair = (halo_x, halo_y)
                                mnozhestvo_set_halo.append(halo_pair)
                        # для всех следующих проверяем, попадают ли точки корабля в множество точек halo
                        # если нет - добавляем новые, если попали не туда, то просим переввести корабль
                        # робот повторяет ввод
                        elif l is not 0:
                            # сравниваем попадают ли точки добавляемого корабля в множество halo имеющихся кораблей
                            # если не попадают, добавляем к множеству точек, точки нового корабля
                            if i in mnozhestvo_set_halo:
                                #print('Попадаем на неправильные клетки! Надо переставить корабль') #это для ручного ввода
                                raise IndexError

                                #если попадают - ошибка!
                            else:
                                #print('Не попадаем в множество')
                                halo_pair = (i[0], i[1])
                                mnozhestvo_set_halo.append(halo_pair)
                #для вертикальной ориентация корабля
                elif z is True:
                    ship_coordinates = [(x, y) for y in range(y, y + num)]
                    # проверка по вертикали - halo
                    # мы ставим корабль только тогда, когда он не пересекается с другими и
                    # находится не зоне действия других кораблей
                    for i in ship_coordinates:
                        if l == 0:
                            for d, z in [(d, z) for d in halo_pattern_h for z in halo_pattern_v]:
                                halo_x = i[0] + d
                                halo_y = i[1] + z
                                halo_pair = (halo_x, halo_y)
                                #halo.append(halo_pair)
                                mnozhestvo_set_halo.append(halo_pair)
                        # для всех следующих проверяем, попадают ли точки корабля в множество точек halo
                        # если нет - добавляем, если да, то просим переввести корабль
                        elif l != 0:
                                # сравниваем попадают ли точки добавляемого корабля в множество halo имеющихся кораблей
                            if i in mnozhestvo_set_halo:
                                    raise IndexError
                            else:
                                #print('Не попадаем в множество')
                                halo_pair = (i[0], i[1])#(halo_x, halo_y)
                                mnozhestvo_set_halo.append(halo_pair)

            # добавляем координаты корабля в список с координатами кораблей
            # добавляем  halo в список координат, в которые нельзя ставить корабль

            for i in ship_coordinates:
                for d, z in [(d, z) for d in halo_pattern_h for z in halo_pattern_v]:
                    halo_x = i[0] + d
                    halo_y = i[1] + z
                    halo_pair = (halo_x, halo_y)
                    mnozhestvo_set_halo.append(halo_pair)

            state = True
            mnozhestvo.append(ship_coordinates)
            return (ship_coordinates)
        except IndexError:
            state = False
            #print('Координаты выходят за границы поля, или корабли стоят рядом, try again')

def construct_player(num):
    '''эта функция нужна для конструирование игроков'''
    ship_coordinates = []

    name = input_function('Ваше имя: ')
    num = int(input_function('Номер: '))
    return (name, num)

def field_generation():
     field = [[a] * 10 for i in range(10)]
     return field


def field_positions_generation():
    '''генерируем все доступные варианты выстрелов'''
    positions = []
    for i in range(10):
        for j in range(10):
            pos = (i, j)
            positions.append(pos)
    return positions


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
            Y = ship.xyz[i][j][0]
            X = ship.xyz[i][j][1]
            try:
                field[X][Y] = 'O' #colored('O', 'yellow', 'on_green', attrs=['bold']) #в виндовсе не пашет
            except IndexError:
                print('За границами игрового поля!')
    return(field)

def print_field_after_shoot_popal(field, x, y):
    '''если попали в корабль ставим крестик'''
    for i in range(len(field)):
        for j in range(len(field[i])):
            try:
                field[x][y] = 'X'
            except IndexError:
                print('За границами игрового поля!')
    return(field)

def print_field_after_shoot_nepopal(field, x, y):
    '''если не попаль ставить пробел'''
    for i in range(len(field)):
        for j in range(len(field[i])):
            try:
                field[x][y] = '.'
            except IndexError:
                print('За границами игрового поля!')
    return(field)

def convert_to_list(mnozhestvo):
    '''ковертация списка списков из кортежей в строку списко кортежей'''
    ee = []
    for i in mnozhestvo:
        for j in i:
            ee.append(j)
    return (ee)


# def players_ships(player, *field, num):
#   '''че-то пока не успел сделать функцию, которая генерит и игроков и поля... в To Do Items''
#     COUNT = 0
#     l = len(storage.items)
#     for i in NUMBER_OF_SHIPS:
#         ship = Ships.construct(player, construct_ships(i, l))
#         storage.items.append(ship)
#         l = len([ship for ship in ships if ship.name is player])
#         f1 = print_ship_after_placement(field, storage.items[COUNT])
#         COUNT += 1
#     converted = convert_to_list(mnozhestvo)
#     storage.player.append(Player.construct(player, num, converted))
#     players[0].properties()
#     return print_field(field)

def main():

    storage = Storage()
    ships = storage.items
    players = storage.player

    mnozhestvo.clear()
    mnozhestvo_set_halo.clear()
    mnozhestvo_set_ships.clear()

    # player 1 init
    f = field_generation()
    COUNT = 0
    l = len(storage.items)
    player = 'robot1' # input_function('Игрок 1 - Ваше имя: ') #human only!
    for i in NUMBER_OF_SHIPS:
        ship = Ships.construct(player, construct_ships(i, l))
        storage.items.append(ship)
        l = len([ship for ship in ships if ship.name is player])
        f1 = print_ship_after_placement(f, storage.items[COUNT])
        COUNT += 1
    converted = convert_to_list(mnozhestvo)
    storage.player.append(Player.construct(player, 1, converted))
    print(players[0].name) #properties()
    print_field(f1)

    #player 2 init
    mnozhestvo.clear()
    mnozhestvo_set_halo.clear()
    mnozhestvo_set_ships.clear()
    g = field_generation()
    player = 'robot2' #input_function('Игрок 2 - Ваше имя: ')
    l = len([ship for ship in ships if ship.name is player])
    for i in NUMBER_OF_SHIPS:
        ship = Ships.construct(player, construct_ships(i, l))
        storage.items.append(ship)
        l = len([ship for ship in ships if ship.name is player])
        g1 = print_ship_after_placement(g, storage.items[COUNT])
        COUNT += 1
    converted = convert_to_list(mnozhestvo)
    storage.player.append(Player.construct(player, 2, converted))
    print(players[1].name) #properties() #Player.construct(player, 2, mnozhestvo)
    print_field(g1)

    #все возможные ходы игрока robot1
    player_one_positions = field_positions_generation()
    #print(len(player_one_positions))
    #все возможные ходы игрока robot2
    player_two_positions = field_positions_generation()
    #перемешиваем списки ходов
    random.shuffle(player_two_positions)
    random.shuffle(player_one_positions)


    flags = True
    flags2 = False

    # идея логики игры в том, что есть два игрока, у которых есть набор координат.
    # игроки поочередно обмениваются вопросами, есть ли в их наборе определенные координаты
    # если запрашиваемые координаты отсутсвуют, то - игрок "не попал", если присутствуют - то "попал"
    # игра продолжается до тех пор, пока в списке хотя бы из одного игроков не кончатся координаты

    # но что-то у меня в логике не так
    # подглючивает, где-то что-то упустил
    # игра продолжается до тех пор, пока не закончатся координаты в списках одного из игроков
    state = True
    while state is True:
        #if len(players[0].pset) == 0 or len(players[1].pset) == 0:
        #    state = False
            #break
    #while state:

        # игрок 1 стреляет

        #if len(players[1].pset) != 0:
        #elif len(players[0].pset) != 0 or len(players[1].pset) != 0:
        while flags is True and flags2 is False and len(players[1].pset) != 0:
            # выбор координаты для выстрела
            i = random.choice(player_one_positions)
            # проверка есть ли эта координата в списке координат кораблей игрока 2
            if i in players[1].pset:
                # если есть, то
                # 1) удаляем ее из списка координат игрока 2
                # 2) удаляем ее из списка возможных выстрелов игрока 1
                # 3) обновляем поле игрока 2
                # 4) стреляем еще раз
                print(players[0].name, i, 'Попал!')

                #random.shuffle(player_one_positions)
                #print('robot2', len(players[1].pset))
                print_field_after_shoot_popal(g1, i[0], i[1])
                players[1].pset.remove(i)
                player_one_positions.remove(i)
                flags = True
                if len(players[1].pset) == 0:
                    state = False
                    flags = False
                    flags2 = False
                    # if len(players[0].pset) == 0:
                    # state = False  # and flags2 is False and flags is True:
                    print('Игрок ', players[0].name, 'победил. Свое поле G1')
                    print(players[0].name, players[0].pset)
                    print(players[1].name, players[1].pset)
                    print('Свое поле G1: ')
                    print_field(f1)  # свое поле
                    print('Поле соперника F1: ')
                    print_field(g1)
                    break # чужое
                #else:
                 #   pass
            elif i not in players[1].pset:
                # если нет, то удаляем координату из списка возможных выстрелов игрока 1
                # и переход хода
                print(players[0].name, i, 'Не попал!')
                print_field_after_shoot_nepopal(g1, i[0], i[1])
                player_one_positions.remove(i)
                flags2 = True  #переход хода
                flags = False  #переход
            #else:
            #    pass
                #break
                    #break  #flags = False
        # if len(players[0].pset) == 0: # and len(players[1].pset) != 0:
        #     state = False
        #     flags = False
        #     flags2 = False
        #     # if len(players[0].pset) == 0:
        #     # state = False  # and flags2 is False and flags is True:
        #     print('Игрок ', players[1].name, 'победил. Свое поле G1')
        #     print(players[1].name, players[1].pset)
        #     print(players[0].name, players[0].pset)
        #     print('Свое поле G1: ')
        #     print_field(g1)  # свое поле
        #     print('Поле соперника F1: ')
        #     print_field(f1)  # чужое
        # else:
        #     pass
                #break
        while flags2 is True and flags is False and len(players[0].pset) != 0:
            r = random.choice(player_two_positions)
            if r in players[0].pset:
                print(players[1].name, r, 'Попал!')
                print_field_after_shoot_popal(f1, r[0], r[1])
                players[0].pset.remove(r)
                player_two_positions.remove(r)
                #print(len(player_one_positions))
                #print('robot1', len(players[0].pset))
                #random.shuffle(player_one_positions)
                flags2 = True
                if len(players[0].pset) == 0:
                    state = False
                    flags = False
                    flags2 = False
                    print('Игрок ', players[1].name, 'победил. Поле F1')
                    print(players[1].name, players[1].pset)
                    print(players[0].name, players[0].pset)
                    print('Cвое поле F1: ')
                    print_field(g1)  # свое поле
                    print('Поле соперника G1: ')
                    print_field(f1)
                    break # чужое
                else:
                    pass
            elif r not in players[0].pset:
                print(players[1].name, r, 'не попал!')
                print_field_after_shoot_nepopal(f1, r[0], r[1])
                player_two_positions.remove(r)
                print(len(player_one_positions))
                flags2 = False
                flags = True
            # else:
            #     pass
                #break
                #break
        # if len(players[1].pset) == 0: # and len(players[0].pset) != 0:
        #     # state = False  # and flags is True and flags2 is False:
        #     print('Игрок ', players[0].name, 'победил. Поле F1')
        #     print(players[0].name, players[0].pset)
        #     print(players[1].name, players[1].pset)
        #     print('Cвое поле F1: ')
        #     print_field(f1)  # свое поле
        #     print('Поле соперника G1: ')
        #     print_field(g1)  # чужое
        #     state = False
        #     flags = False
        #     flags2 = False
            #break
        # else:
        #     pass


            #break
    # else:
    #     print('!')
    #break
    #flags = True
    #else:
        #print('dsd!')

    print('конец игры!')

if __name__ == '__main__':
    main()

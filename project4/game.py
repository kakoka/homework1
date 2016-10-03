# from termcolor import colored

# Реализация игры для двух тупых роботов

import random
from classes import Storage, Player, Ships
from func import get_input_function

# задаем количество кораблей списком, символы для вывода полей

NUMBER_OF_SHIPS = [4, 3, 3, 2, 2, 2, 1, 1, 1, 1] #паттерн для создания кораблей
input_function = get_input_function()
ship_coordinates_list = []  # множество кординат всех кораблей одного игрока
ship_halo_coordinates = []  # множество точек, окружающие корабли, куда нельзя ставить другие корабли
halo_pattern_h = [-1, 0, 1]  # это паттерны для обхода координат кораблей, для построения зоны, куда нельзя
halo_pattern_v = [1, 0, -1]  # ставить корабли

# определяем функции

def input_ships_coordinates_by_robot(num):
    '''бездушный робот генерит координаты случайным образом'''

    x = int(random.choice([0, 1, 2, 3, 4, 5, 6, 7, 8, 9]))  # x координата
    y = int(random.choice([0, 1, 2, 3, 4, 5, 6, 7, 8, 9]))  # y координата
    z = bool(random.choice([0, 1]))  # z - задает ориентацию корабля 0 - по горизонтали, 1 - по вертикали
    return (x, y, z)


def input_ship_coordinates_by_human(num):
    '''нужна в случае если игроки люди, ручной ввод - проверка на корректность ввода '''
    # эта функция принимает на вход цифру, обозначающцую количество палуб на корабле
    # далее происходит ввод координат, и проверка на то, что эти координаты не буквы
    # если палуб больше 1, то добавляется ввод ориентации корабля

    state = False
    while state is False:
        try:
            try:
                x = int(input_function('X кордината [1 - 10]: ')) - 1
            except ValueError:
                print('Вы вели не число!')
            try:
                y = int(input_function('Y кордината [1 - 10]: ')) - 1
            except ValueError:
                print('Вы ввели не число, введите число в диапазоне от 1 до 10.')
            if num > 1:
                try:
                    z = int(input_function('Ориентация, горизонтально - 0, вертикально - 1 [0, 1]: '))
                    if z == 0 or z == 1:
                        return (x, y, z)
                    else:
                        raise IndexError
                except TypeError:  # ValueError:
                    print('0 или 1')
                    state = False
            else:
                z = 0
                return (x, y, z)
        except:
            print('Ошибка ввода, введите данные еще раз')
            state = False


def construct_ships(num, len_of_ships_list_in_storage):
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
            got_coordinates = input_ship_coordinates_by_human(num)  # функция, которая генерит рандомные координаты
            got_coordinates = input_ships_coordinates_by_robot(num)
            x = got_coordinates[0]  # координата x
            y = got_coordinates[1]  # координата y
            z = got_coordinates[2]  # z - ориентация 0 - горизонтально, 1 - вертикально

            # эта проверка настроена на робота, который генерирует не отрицательные целые числа)
            # для человека - проверка на значение еще будет включать проверку на знак числа

            if x + num > 10 or y + num > 10 or x + num > 10 and y + num > 10 is True:
                raise IndexError
            else:
                # запускаем мегапроверку

                # для горизонтальной ориентация корабля
                if z is False:
                    # генерируем пару x, y
                    ship_coordinates = [(x, y) for x in range(x, x + num)]

                    # проверка по горизонтали
                    # мы ставим корабль только тогда, когда он не пересекается с другими кораблями и
                    # находится вне зоны действия других кораблей

                    for i in ship_coordinates:

                        # это для первого первый корабль на поле - заполняем halo - окружение
                        if len_of_ships_list_in_storage is 0:
                            for d, z in [(d, z) for d in halo_pattern_h for z in halo_pattern_v]:
                                halo_x = i[0] + d
                                halo_y = i[1] + z
                                halo_pair = (halo_x, halo_y)
                                ship_halo_coordinates.append(halo_pair)
                        # для всех следующих проверяем, попадают ли точки корабля в множество точек halo
                        # если нет - добавляем новые, если попали не туда, то просим переввести корабль
                        # робот повторяет ввод
                        elif len_of_ships_list_in_storage is not 0:
                            # сравниваем попадают ли точки добавляемого корабля в множество halo имеющихся кораблей
                            # если не попадают, добавляем к множеству точек, точки нового корабля
                            if i in ship_halo_coordinates:
                                #print('Попадаем на неправильные клетки! Надо переставить корабль') #это для ручного ввода
                                raise IndexError

                                # если попадают - ошибка!
                            else:
                                #print('Не попадаем в множество')
                                halo_pair = (i[0], i[1])
                                ship_halo_coordinates.append(halo_pair)
                # для вертикальной ориентация корабля
                elif z is True:
                    ship_coordinates = [(x, y) for y in range(y, y + num)]
                    # проверка по вертикали - halo
                    # мы ставим корабль только тогда, когда он не пересекается с другими и
                    # находится не в зоне действия других кораблей
                    for i in ship_coordinates:
                        if len_of_ships_list_in_storage == 0:
                            for d, z in [(d, z) for d in halo_pattern_h for z in halo_pattern_v]:
                                halo_x = i[0] + d
                                halo_y = i[1] + z
                                halo_pair = (halo_x, halo_y)
                                ship_halo_coordinates.append(halo_pair)

                        # для всех следующих проверяем, попадают ли точки корабля в множество точек halo
                        # если нет - добавляем, если да, то просим переввести корабль
                        elif len_of_ships_list_in_storage != 0:
                            # сравниваем попадают ли точки добавляемого корабля в множество halo имеющихся кораблей
                            if i in ship_halo_coordinates:
                                raise IndexError
                            else:
                                # print('Не попадаем в множество')
                                halo_pair = (i[0], i[1])
                                ship_halo_coordinates.append(halo_pair)

            # добавляем координаты корабля в список с координатами кораблей
            # добавляем  halo в список координат, в которые нельзя ставить корабль

            for i in ship_coordinates:
                for d, z in [(d, z) for d in halo_pattern_h for z in halo_pattern_v]:
                    halo_x = i[0] + d
                    halo_y = i[1] + z
                    halo_pair = (halo_x, halo_y)
                    ship_halo_coordinates.append(halo_pair)

            #state = True
            ship_coordinates_list.append(ship_coordinates)
            return (ship_coordinates)
        except IndexError:
            state = False
            # print('Координаты выходят за границы поля, или корабли стоят рядом, try again')


def construct_player(num):
    '''эта функция нужна для конструирование игроков, когда в игре не роботы'''
    name = input_function('Ваше имя: ')
    num = int(input_function('Номер: '))
    return (name, num)


def field_generation():
    '''генерируем пустое поле'''
    field = [[' '] * 10 for i in range(10)]
    return field


def field_positions_generation():
    '''генерируем все варианты выстрелов'''
    positions = []
    for i in range(10):
        for j in range(10):
            pos = (i, j)
            positions.append(pos)
    return positions


def render_field(field):
    '''функция вывода на экран игрового поля'''
    print('X:| 1| 2| 3| 4| 5| 6| 7| 8| 9|10|Y:')

    for i in range(len(field)):
        print('  ', end='')
        for j in range(len(field[i])):
            print('| {}'.format(field[i][j]), end='')
        print('| {}'.format(i + 1))
    return


def place_ships():
    return


def render_field_after_ships_placement(field, ship):
    '''показ корабля после того как поставили его на поле'''
    for i in range(len(ship.xyz)):
        for j in range(len(ship.xyz[i])):
            x = ship.xyz[i][j][0]
            y = ship.xyz[i][j][1]
            try:
                field[x][y] = 'O'  # colored('O', 'yellow', 'on_green', attrs=['bold']) #в виндовсе не пашет
            except IndexError:
                print('За границами игрового поля!')
    return (field)


def shoot_popal(field, x, y):
    '''если попал в корабль ставим крестик'''
    try:
        field[x][y] = 'X'
    except IndexError:
        print('За границами игрового поля!')
    return


def shoot_mimo(field, x, y):
    '''если не попал ставим точку'''
    try:
        field[x][y] = '.'
    except IndexError:
        print('За границами игрового поля!')
    return


def convert_to_list(mnozhestvo):
    '''ковертация списка списков из кортежей в строку списко кортежей'''
    ee = []
    for i in mnozhestvo:
        for j in i:
            ee.append(j)
    return (ee)

def main():

    # начальные приготовления

    storage = Storage()
    ships = storage.items
    players = storage.player
    ship_coordinates_list.clear()


    # для создания игроков и кораблей можно было бы и отдельную функцию написать
    # но я не успел, в итоге дублирование кода, что не хорошо
    # созадем первого игрока

    player_1_field = field_generation()  # создаем поле боя для первого игрока
    COUNT = 0
    len_of_ships_list = len(storage.items)
    player = 'robot1'  # input_function('Игрок 1 - Ваше имя: ') #human only!
    for i in NUMBER_OF_SHIPS:
        ship = Ships.construct(player, construct_ships(i, len_of_ships_list))
        storage.items.append(ship)
        len_of_ships_list = len([ship for ship in ships if ship.name is player])
        render_field_after_ships_placement(player_1_field, storage.items[COUNT])
        #print(player_1_field)
        COUNT += 1
    converted = convert_to_list(ship_coordinates_list)
    storage.player.append(Player.construct(player, 1, converted))

    #выводим имя и поле с расставленными кораблями игрока 1

    print('Расстановка кораблей ', players[0].name)
    render_field(player_1_field)

    # создаем второго игрока

    ship_coordinates_list.clear()
    ship_halo_coordinates.clear()
    player_2_field = field_generation()  # поле боя для второго игрока

    player = 'robot2'  # input_function('Игрок 2 - Ваше имя: ')
    len_of_ships_list = len([ship for ship in ships if ship.name is player])
    for i in NUMBER_OF_SHIPS:
        ship = Ships.construct(player, construct_ships(i, len_of_ships_list))
        storage.items.append(ship)
        len_of_ships_list = len([ship for ship in ships if ship.name is player])
        render_field_after_ships_placement(player_2_field, storage.items[COUNT])
        COUNT += 1
    converted = convert_to_list(ship_coordinates_list)
    storage.player.append(Player.construct(player, 2, converted))

    #выводим имя и поле с расставленными кораблями игрока 2
    print('Расстановка кораблей игрока ', players[1].name)
    render_field(player_2_field)

    input_function('For start - press Enter.')
    # все возможные ходы игрока robot1
    player_one_positions = field_positions_generation()

    # все возможные ходы игрока robot2
    player_two_positions = field_positions_generation()

    # перемешиваем списки ходов
    random.shuffle(player_two_positions)
    random.shuffle(player_one_positions)

    game_state = True
    flag_player_1 = True
    flag_player_2 = False

    # идея логики игры в том, что есть два игрока, у которых есть набор координат.
    # игроки поочередно обмениваются вопросами, есть ли в их наборе определенные координаты
    # если запрашиваемые координаты отсутсвуют, то - игрок "не попал", если присутствуют - то "попал"
    # игра продолжается до тех пор, пока в списке хотя бы из одного игроков не кончатся координаты
    # можно было все запихнуть в функцию, что правильно, опять дублирование кода


    while game_state is True:

        while flag_player_1 is True and flag_player_2 is False and len(players[1].pset) != 0:

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
                shoot_popal(player_2_field, i[0], i[1])
                players[1].pset.remove(i)
                player_one_positions.remove(i)
                flag_player_1 = True
                if len(players[1].pset) == 0:

                    # проверяем длину строки с координатами игрока 2 после попадания,
                    # если она нулевая, значит игрок 1 победил
                    # выводим поля с отмеченными выстрелами и подбитыми кораблями

                    game_state = False
                    flag_player_1 = False
                    flag_player_2 = False
                    print('\nИгрок ', players[0].name, 'победил.\nСвое поле:')
                    render_field(player_1_field)  # свое поле
                    print('Поле соперника: ')
                    render_field(player_2_field)
                    break
            elif i not in players[1].pset:
                # если нет, то удаляем координату из списка возможных выстрелов игрока 1
                # и переход хода
                print(players[0].name, i, 'Мимо!')
                shoot_mimo(player_2_field, i[0], i[1])
                player_one_positions.remove(i)
                flag_player_2 = True  # переход хода
                flag_player_1 = False

        # для второго игрока делаем все то же самое что и для первого

        while flag_player_2 is True and flag_player_1 is False and len(players[0].pset) != 0:
            r = random.choice(player_two_positions)

            if r in players[0].pset:
                print(players[1].name, r, 'Попал!')
                shoot_popal(player_1_field, r[0], r[1])
                players[0].pset.remove(r)
                player_two_positions.remove(r)
                flag_player_2 = True

                if len(players[0].pset) == 0:
                    game_state = False
                    flag_player_1 = False
                    flag_player_2 = False
                    print('\nИгрок ', players[1].name, 'победил.\nСвое поле: ')
                    render_field(player_2_field)  # свое поле
                    print('Поле соперника: ')
                    render_field(player_1_field)
                    break  # чужое

            elif r not in players[0].pset:
                print(players[1].name, r, 'Мимо!')
                shoot_mimo(player_1_field, r[0], r[1])
                player_two_positions.remove(r)
                flag_player_2 = False
                flag_player_1 = True


    print('Конец игры!')


if __name__ == '__main__':
    main()

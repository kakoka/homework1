# -*- coding: utf-8 -*-

# `random` module is used to shuffle field, see§:
# https://docs.python.org/3/library/random.html#random.shuffle
import random


# Empty tile, there's only one empty cell on a field:
EMPTY_MARK = 'x'

# Dictionary of possible moves if a form of:
# key -> delta to move the empty tile on a field.
MOVES = {
    'w': -4,
    's': 4,
    'a': -1,
    'd': 1,
}


def shuffle_field():

    matrix = list(range(1, 16))
    for i in range(len(matrix)):
        matrix[i] = "{0:02d}".format(matrix[i])
    matrix = matrix + [EMPTY_MARK]
    random.shuffle(matrix)
    return matrix

def print_field(field):
    for i in range(0, len(field), 4):
        print(field[i:i+4])

def is_game_finished(field):
    #This func return if == True or if != False
    sort_m = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12', '13', '14', '15', 'x']
    return sort_m is field

def perform_move(field, key):
    ind = field.index(EMPTY_MARK)
    step = MOVES[key]
    if (ind + step) < 0 or (ind + step) > 16:
        raise IndexError('!!!')
    else:
        field[ind + step], field[ind] = field[ind], field[ind + step]
    return field


def handle_user_input():

    q = input("Please, make a choice:")

    while q not in MOVES.keys():
        print("not correct!")
        q = input("Please, type 'a' 's' 'w' 'd' to make a choice:")
    return q

def main():
    try:
        game_matrix = shuffle_field()
        print_field(game_matrix)
        while is_game_finished(game_matrix) is False:
            print(is_game_finished(game_matrix))
            try:
                #print(is_game_finished(game_matrix))
                key_ = handle_user_input()
                perform_move(game_matrix, key_)
                print_field(game_matrix)
            except IndexError:
                print("!")
                print_field(game_matrix)
    except KeyboardInterrupt:
        print('\nshutting down\n')

if __name__ == '__main__':
    # See what this means:
    # http://stackoverflow.com/questions/419163/what-does-if-name-main-do

        main()

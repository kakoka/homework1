# -*- coding: utf-8 -*-
import random
EMPTY_MARK = 'x'
MOVES = {
    'w': -4,
    's': 4,
    'a': -1,
    'd': 1,
}
def shuffle_field():
    matrix = list(range(1, 16))
    matrix = matrix + [EMPTY_MARK]
    random.shuffle(matrix)
    return matrix

def print_field(field):
    for i in range(0, len(field), 4):
        print((field[i:i+4]))

def is_game_finished(field):
    result = field == list(range(1, 16)) + [EMPTY_MARK]
    return result

def perform_move(field, key):
    ind = field.index(EMPTY_MARK)
    step = MOVES[key]
    if (ind + step) < 0 or (ind + step) >= 16:
        raise IndexError("This move is not approved, please do another")
    else:
        field[ind + step], field[ind] = field[ind], field[ind + step]
    return field

def handle_user_input():

    q = input("Please, make a choice:")

    while q not in MOVES.keys():
        print("Only 'a' 's' 'w' 'd' accepted!\n")
        q = input("Please, type 'a' 's' 'w' 'd' to make a choice:")
    return q

def main():
    # matrix_chek
    # if \N=\sum_{i=1}^{n_i=15} n_i+e %2 != 0 then regenerate matrix
    # https://ru.wikipedia.org/wiki/Игра_в_15#.D0.9C.D0.B0.D1.82.D0.B5.D0.BC.D0.B0.D1.82.D0.B8.D1.87.D0.B5.D1.81.D0.BA.D0.BE.D0.B5_.D0.BE.D0.BF.D0.B8.D1.81.D0.B0.D0.BD.D0.B8.D0.B5
    def chek_up(field):
        position = field.index(EMPTY_MARK)
        if position in range(1, 4):
            e = 1
        elif position in range(5, 8):
            e = 2
        elif position in range(9, 12):
            e = 3
        else:
            e = 4
        sum = 0
        count = 0
        # print(e)
        for z in range(1, 16):
            if field[z] == EMPTY_MARK:
                pass
            else:
                for k in range(z, 16):
                    if field[k] == EMPTY_MARK:
                        pass
                    else:
                        if field[z] > field[k]:
                            count += 1
                            sum = count + e
        return sum

    game_matrix = shuffle_field()

    #chek-up matrix
    while chek_up(game_matrix) % 2 != 0:

        #regenerate matrix
        game_matrix = shuffle_field()

    print_field(game_matrix)
    turns = 0
    while is_game_finished(game_matrix) is False:
        try:
            key_ = handle_user_input()
            perform_move(game_matrix, key_)
            print_field(game_matrix)
            turns += 1
        except IndexError as err:
            print(err)
            print_field(game_matrix)
        except KeyboardInterrupt:
            #print("Number of you terns:", turns)
            print('\nshutting down\n')
    print("You win! Number of you terns:", turns)

if __name__ == '__main__':
    # See what this means:
    # http://stackoverflow.com/questions/419163/what-does-if-name-main-do

        main()

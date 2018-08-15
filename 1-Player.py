import os
import sys
import random
from time import sleep
from copy import deepcopy

ships = {
    'Aircraft Carrier': {'size': 5, 'mark': 'A'},
    'Battleship': {'size': 4, 'mark': 'B'},
    'Submarine': {'size': 3, 'mark': 'S'},
    'Destroyer': {'size': 3, 'mark': 'D'},
    'Patrol Boat': {'size': 2, 'mark': 'P'},
}


def get_open_slots(ship):
    slots = []

    for row in xrange(high):
        for col in xrange(wide - ship['size'] + 1):
            slot = []
            for i in xrange(ship['size']):
                if backend_grid[row][col+i] == '_':
                    slot.append([row, col+i])
                else:
                    slot = []
                    break
            else:
                slots.append(slot)

    for col in xrange(wide):
        for row in xrange(high - ship['size'] + 1):
            for i in xrange(ship['size']):
                if backend_grid[row+i][col] == '_':
                    slot.append([row+i, col])
                else:
                    slot = []
                    break
            else:
                slots.append(slot)
            slot = []

    return slots


def place_ships():
    for ship in ships.values():
        slots = get_open_slots(ship)
        random_slot = random.choice(slots)
        mark_slot(random_slot, ship)


def mark_slot(slot, ship):
    for x, y in slot:
        backend_grid[x][y] = ship['mark']


def show_board(grid):
    os.system('cls')
    for row in grid:
        print ' '.join(row)
    print


def get_guess():
    while True:
        guess = raw_input('\nGuess x y\n----> ')
        if guess in ['reveal', 'cheat', 'exit', 'quit']:
            return guess
        try:
            x, y = map(int, guess.split())
            if x not in range(wide) or y not in range(high):
                print '\nWarning: You are leaving the mission area........'
                print 'coordinates each must be in range 0-9.\n'.format(wide, high)
                continue
            return x + 1, y + 1
        except Exception:
            print '\nPlease enter coordinates in this format: x y \neg--> 0 0\neg--> 3 7'


def guess_hit():
    ''' play '''
    global used
    while True:
        guess = get_guess()
        if guess in ['reveal', 'cheat']:
            show_board(backend_grid)
        elif guess in ['exit', 'quit']:
            sys.exit()
        else:
            if guess in used:
                print '\nYou\'ve already guessed this. Try again.\n'
                continue
            guess_x, guess_y = guess
            used.append(guess)
            break
    # identify what is at the guessed coordinate as 'landed_on'
    landed_on = backend_grid[guess_y][guess_x]
    # if it's not a MISS, mark the HIT on both grids
    if landed_on != '_':
        backend_grid[guess_y][guess_x] = chr(254)
        player_grid[guess_y][guess_x] = chr(254)
        # check for intact portions of hit ship
        rem = 0
        for row in backend_grid:
            if landed_on in row:
                rem += 1
        # if none, it's a sinker
        if rem == 0:
            for type, ship in ships.items():
                if landed_on == ship['mark']:
                    # pause for dramatic effect
                    print '\n...'
                    sleep(.75)
                    print '...'
                    sleep(.75)
                    print '... You sank my {} !!!\n'.format(type)
                    sleep(1)
            show_board(player_grid)
            return True
        else:
            print '\n... HIT ...\n'
            show_board(player_grid)
    else:
        # do this if it's a MISS
        backend_grid[guess_y][guess_x] = 'o'
        player_grid[guess_y][guess_x] = 'o'
        print '\n... MISS ...\n'
        show_board(player_grid)


def print_win(turns):
    for i in xrange(3):
        print '!!! YOU SANK EM ALL !!!'
        print '...(in {} turns)'.format(turns)
        sleep(1)
        show_board(backend_grid_copy)
        print '!!! YOU SANK EM ALL !!!'
        print '...(in {} turns)'.format(turns)
        sleep(1)
        show_board(player_grid)


if __name__ == '__main__':
    os.system('cls')
    print '\n **** Welcome to (1P) Battleship **** \n'
    sleep(1)
    print 'I\'ll ask you you to guess a coordinate'
    sleep(1)
    print 'and then I\'ll show you if it hit anything. \n'
    sleep(1)
    wide = 10
    high = 10
    print 'The maximum / default grid size is {}x{}.'.format(wide, high)
    if raw_input('Enter "small" if you want a smaller grid.\n-----> ') == "small":
        print
        wide = min(10, int(raw_input('width  = ')))
        high = min(10, int(raw_input('height = ')))
    print
    # build matrix 'backend_grid' and matrix 'player_grid'
    backend_grid = []
    player_grid = []
    # put in numbers for x-axis
    backend_grid.append([' '] + map(str, range(wide)))
    player_grid.append([' '] + map(str, range(wide)))
    # put in numbers for y-axis as well as all '_'s
    for i in range(high):
        backend_grid.append([str(i)] + ['_'] * wide)
        player_grid.append([str(i)] + ['_'] * wide)
    show_board(player_grid)
    place_ships()
    backend_grid_copy = deepcopy(backend_grid)
    ships_remaining = len(ships)
    turns = 0
    used = []
    while ships_remaining > 0:
        print '{} ships remaining'.format(ships_remaining)
        if guess_hit():
            ships_remaining -= 1
        turns += 1
    else:
        print_win(turns)

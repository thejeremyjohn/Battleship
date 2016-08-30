# TO DO: finish docs, debug
import sys
import random
from time import sleep
from copy import deepcopy

# ships in the game
ships = [
	(5, 'Aircraft Carrier'),
	(4, 'Battleship'),
	(3, 'Submarine'),
	(3, 'Destroyer'),
	(2, 'Patrol Boat')
	]

def show_board(grid):
	''' Prints the given grid. '''
	print
	for row in grid:
		print ' '.join(row)
	print


def place_ships():
	''' Places ships in backend_grid. '''
	for ship in ships:
		# randomized coordinate to "draw" ship.
		rand_y = random.randint(1, high+1)
		rand_x = random.randint(1, wide+1)
		# direction to "draw"
		directions = ['hori_right', 'hori_left', 'vert_down', 'vert_up']
		# bruteforce placement. BUG: ships are sometimes omitted
		while directions != []:
			set_direction = random.choice(directions)
			directions.remove(set_direction)
			try:
				if set_direction == 'hori_right':
					if backend_grid[rand_y][rand_x] == '_':
						for x in xrange(ship[0]):
							if backend_grid[rand_y][rand_x + x] != '_':
								break
						else:
							for x in xrange(ship[0]):
								backend_grid[rand_y][rand_x + x] = ship[1][0]
							directions = []
							continue
				elif set_direction == 'hori_left':
					if backend_grid[rand_y][rand_x] == '_':
						if rand_x - ship[0] >= 1:
							for x in xrange(ship[0]):
								if backend_grid[rand_y][rand_x - x] != '_':
									break
							else:
								for x in xrange(ship[0]):
									backend_grid[rand_y][rand_x - x] = ship[1][0]
								directions = []
								continue
						else:
							continue
				elif set_direction == 'vert_down':
					if backend_grid[rand_y][rand_x] == '_':
						for y in xrange(ship[0]):
							if backend_grid[rand_y + y][rand_x] != '_':
								break
						else:
							for y in xrange(ship[0]):
								backend_grid[rand_y + y][rand_x] = ship[1][0]
							directions = []
							continue
				elif set_direction == 'vert_up':
					if backend_grid[rand_y][rand_x] == '_':
						if rand_y - ship[0] >= 1:
							for y in xrange(ship[0]):
								if backend_grid[rand_y - y][rand_x] != '_':
									break
							else:
								for y in xrange(ship[0]):
									backend_grid[rand_y - y][rand_x] = ship[1][0]
								directions = []
								continue
						else:
							continue
				rand_y = random.randint(1, high+1)
				rand_x = random.randint(1, wide+1)
				directions = ['hori_right', 'hori_left', 'vert_down', 'vert_up']
			except IndexError:
				rand_y = random.randint(1, high+1)
				rand_x = random.randint(1, wide+1)


def get_guess():
	while True:
		guess = raw_input('\nGuess x y\n----> ')
		if guess in ['reveal', 'cheat', 'exit', 'quit']:
			return guess
		try:
			x, y = map(int, guess.split())
			if x not in range(wide) or y not in range(high):
				print '\nWarning: You are leaving the mission area........'
				print 'x and y must be LESS than {} and {}, respectively.\n'.format(wide, high)
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
		# the char 'landed_on' will match the first letter of the ship
		# pause for dramatic effect
		if rem == 0:
			for ship in ships:
				if landed_on == ship[1][0]:
					print '\n...'
					sleep(.75)
					print '...'
					sleep(.75)
					print '... You sank my {} !!!\n'.format(ship[1])
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


if __name__ == '__main__':
	print '\n **** Welcome to (1P) Battleship **** \n'
	sleep(1)
	print 'I\'ll ask you you to guess a coordinate'
	sleep(1)
	print 'and then I\'ll show / tell you if it hits. \n'
	sleep(1)
	wide = 10
	high = 10
	print 'The maximum / default grid size is {}x{}.'.format(wide, high)
	if raw_input('Enter "y" or "yes" if you want a smaller grid.\n-----> ') in ['y', 'yes', 'yeah', 'sure', 'ya', 1]:
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
		if guess_hit():
			ships_remaining -= 1
		turns += 1
	else:
		print '!!! YOU SANK EM ALL !!!'
		print '...(in {} turns)'.format(turns)
		sleep(1)
		show_board(backend_grid_copy)
		print '!!! YOU SANK EM ALL !!!'
		print '...(in {} turns)'.format(turns)
		sleep(1)
		show_board(player_grid)
		print '!!! YOU SANK EM ALL !!!'
		print '...(in {} turns)'.format(turns)
		sleep(1)
		show_board(backend_grid_copy)
		print '!!! YOU SANK EM ALL !!!'
		print '...(in {} turns)'.format(turns)
		sleep(1)
		show_board(player_grid)
		print '!!! YOU SANK EM ALL !!!'
		print '...(in {} turns)'.format(turns)
		sleep(1)
		show_board(backend_grid_copy)
		print '!!! YOU SANK EM ALL !!!'
		print '...(in {} turns)'.format(turns)
		sleep(1)
		show_board(player_grid)

"""
Clone of 2048 game.
"""

import random
import itertools

# Directions, DO NOT MODIFY
UP = 1
DOWN = 2
LEFT = 3
RIGHT = 4

# Offsets for computing tile indices in each direction.
# DO NOT MODIFY this dictionary.
OFFSETS = {UP: (1, 0),
           DOWN: (-1, 0),
           LEFT: (0, 1),
           RIGHT: (0, -1)}


def find_adjacent(left, line):
    """
    find the indices of the next set of adjacent 2048 numbers in the list

    Args:
        left: start index of the "left" value
        line:  the list of 2048 numbers

    Returns:
        left, right:  indices of the next adjacent numbers in the list
            if there are no more adjacent numbers, left will be
            len(line) - 1

    """

    # find the next non zero index for left
    while left < (len(line) - 1) and line[left] == 0:
        left += 1

    right = left + 1
    # find the next non zero index after left
    while right < len(line) and line[right] == 0:
        right += 1

    return left, right

def merge(line):
    """
    Merge the tiles in a line of 2048

    Assumes the line should be merged left (0) to right (len(line))

    Args:
        line:  a line of 2048 numbers
    """
    
    result = [0] * len(line)
    current = left = 0

    # find adjacent elements adding them when they match
    # or just inserting the next item when they don't
    while left < len(line):
        left, right = find_adjacent(left, line)
        # when right is beyond list end, no need to test
        if right < len(line) and line[left] == line[right]:
            result[current] = line[left] + line[right]
            left = right + 1
        else:
            result[current] = line[left]
            left = right 

        current +=1

    # the rest of result have already been filled in with 0's
    # so we're done
    return result


class TwentyFortyEight:
    """
    Class to run the game logic.
    """

    def __init__(self, grid_height, grid_width):
        """
        initialize grid of height, width
        """
        self._height = grid_height
        self._width = grid_width
        # initial tiles for direction from which to traverse
        self._initial_tiles = {
                UP: [(0, col) for col in range(self._width)], 
                DOWN: [(self._height - 1, col) for col in range(self._width)],
                LEFT: [(row, 0) for row in range(self._height)],
                RIGHT: [(row, self._width - 1) for row in range(self._height)]
                }

        # number of tiles to traverse per direction
        self._num_tiles = {
                UP: self._height, 
                DOWN: self._height,
                LEFT: self._width,
                RIGHT: self._width
                }

        self.reset()
        self.counter = 1
        self.changed = None

    def reset(self):
        """
        Reset the game so the grid is empty except for two
        initial tiles.
        """
        self._grid = [[0 for _ in range(self._width)]
                    for _ in range(self._height)]
        self.new_tile()
        self.new_tile()

    def __str__(self):
        """
        Return a string representation of the grid for debugging.
        """
        strings = [[str(val) if val != 0 else str(val + 1) for val in row] for row in self._grid]
        # get max len per column for alignment 
        lens = [max(map(len, col)) for col in zip(*strings)]
        # create a format string for each column
        fmt = ','.join('{{:{}}}'.format(length) for length in lens)
        # apply format to each column in each row
        table = [fmt.format(*row) for row in strings]
        return '\n'.join(table)

    def get_grid_height(self):
        """
        Get the height of the board.
        """
        return self._height

    def get_grid_width(self):
        """
        Get the width of the board.
        """
        return self._width

    def move(self, direction, is_check=False):
        """
        Move all tiles in the given direction and add
        a new tile if any tiles moved.
        """
        # keep track of whether board changed
        self.changed = False

        # iterate over all initial tiles for the direction
        # merge the line associated with the initial tile
        # and put it back in the grid
        for start in self._initial_tiles[direction]:
            # to keep track of tiles associated with line elements
            line_grid_map = {}
            line = []
            cur = start
            for index in range(self._num_tiles[direction]):
                line_grid_map[index] = cur
                line.append(self.get_tile(*cur))
                # update row and col
                row = cur[0] + OFFSETS[direction][0]
                col = cur[1] + OFFSETS[direction][1]
                cur = (row, col)

            merged = merge(line)
            for index in range(self._num_tiles[direction]):
                row, col = line_grid_map[index]
                old_val = self.get_tile(row, col)
                new_val = merged[index]
                if old_val != new_val:
                    if is_check:
                        return True

                    self.changed = True
                    self.set_tile(row, col, merged[index])

        if self.changed:
            self.new_tile()

        self.counter += 1

    def _empty_tiles(self):
        """
        return tiles (as tuples) that are empty
        """
        tuples = []
        for row in range(self._height):
            for col in range(self._width):
                if self._grid[row][col] == 0:
                    tuples.append((row, col))

        return tuples

    def new_tile(self):
        """
        Create a new tile in a randomly selected empty
        square.  The tile should be 2 90% of the time and
        4 10% of the time.
        """
        # get empty tiles 
        empties = self._empty_tiles()
        # create distribution from which to choose value
        value_distribution = [4,2,2,2,2,2,2,2,2,2]
        if len(empties) > 0:
            row, col = random.choice(empties)
            val = random.choice(value_distribution)
            self.set_tile(row, col, val)

    def set_tile(self, row, col, value):
        """
        Set the tile at position row, col to have the given value.
        """
        self._grid[row][col] = value

    def get_tile(self, row, col):
        """
        Return the value of the tile at position row, col.
        """
        return self._grid[row][col]

    def move_and_print_state(self, direction):
        # direction = self._transform_dir_tuple_to_direction(direction_list)
        self.move(direction)
        # print(str(self.counter) + ". move:")
        # print("##########" + "\n" + str(self) + "\n" + "##########" + "\n")
        return self.table_as_array()

    @staticmethod
    def _transform_dir_tuple_to_direction(direction_list):
        return direction_list.index(1) + 1

    def table_as_array(self):
        strings = [[val if val != 0 else val + 1 for val in row] for row in self._grid]
        #return list(itertools.chain.from_iterable(strings))
        return tuple(itertools.chain.from_iterable(strings))

    def reward(self):
        if self.changed:
            return self.table_as_array().count(1) / 16
        else:
            return -1

    def is_ended(self):
        if max(max(self._grid)) == 2048:
            return True
        moves = [1, 2, 3, 4]
        while moves:
            direction = moves.pop()
            if self.move(direction, is_check=True):
                return False
        return True


if __name__ == "__main__":
    game = TwentyFortyEight(4, 4)
    game.reset()
    print(game)

    valid_keystrokes = ("w", "s", "a", "d")

    key = None
    while key != "q":
        key = input()
        if key in valid_keystrokes:
            direction_list = [1 if key == k else 0 for k in valid_keystrokes]
            game.move_and_print_state(direction_list)
            # print(game.table_as_array())



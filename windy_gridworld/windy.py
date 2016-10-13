import numpy as np


class WindyGridWorld:

    def __init__(self, grid_size, winner_tile, windy_array, initial=None, only_first_row=True):

        self.grid_size = grid_size  # tuple (row, col)
        self.__index_shift = np.asarray([1, 1])

        self._current_position = np.asarray(initial) - self.__index_shift if initial else self._set_initial_position(only_first_row)

        self._winner_tile = np.asarray(winner_tile) - self.__index_shift  # tuple (row, col)

        assert len(windy_array) == grid_size[1]

        self._windy_array = windy_array

        # 1. Up; 2. Right; 3. Down; 4. Left; 5. Upper right; 6. Lower right; 7. Lower left; 8. Upper left
        self._moves = {1: np.asarray([-1, 0]), 2: np.asarray([0, 1]), 3: np.asarray([1, 0]), 4: np.asarray([0, -1]),
                       5: np.asarray([-1, 1]), 6: np.asarray([1, 1]), 7: np.asarray([1, -1]), 8: np.asarray([-1, -1])}

        # print(self._current_position + self.__index_shift)

    def step(self, action):
        # Moving according to action
        next_pos = self._current_position + self._moves[action]
        # Check if next state is out of the table because of the move
        if self.is_out_of_bounds(next_pos):
            next_pos = self._current_position

        # The effect of wind
        wind = self._windy_array[next_pos[1]]
        next_pos[0] -= wind
        # Check if next stage is out of the table because of the wind
        if self.is_out_of_bounds(next_pos):
            next_pos[0] = 0 if wind > 0 else self.grid_size[0] - 1

        self.set_current_position(next_pos)
        return self.current_pos(), self._reward(action), self._is_finished()

    def _reward(self, action):
        return -1 if action < 5 else -np.sqrt(2)

    def current_pos(self):
        return tuple(self._current_position + self.__index_shift)

    def set_current_position(self, pos):
        self._current_position = pos

    def _set_initial_position(self, only_first_row):
        if only_first_row:
            return np.asarray([np.random.randint(0, self.grid_size[0]), 0])
        return np.asarray([np.random.randint(self.grid_size[0]),
            np.random.randint(self.grid_size[1])])

    def _is_finished(self):
        return True if np.all(np.equal(self._current_position, self._winner_tile)) else False

    def is_out_of_bounds(self, pos):
        if pos[0] < 0 or pos[0] >= self.grid_size[0] or pos[1] < 0 or pos[1] >= self.grid_size[1]:
            return True
        return False

if __name__ == "__main__":
    game = WindyGridWorld((6, 10), (6, 10), [0, 0, -2, -1, -1, 0, 0, 0, 0, 0])
    for _ in range(15):
        # action = np.random.randint(1, 5)
        action = 2
        pos, r, done = game.step(action)
        print(action, pos, r, done)
        if done:
            break

"""This is the v1 of the random walker module, which combines the concept of a
random walker with a grid. In this case, we have simplified the idea of a
random walker to take steps on a grid, and the step itself is an index on the
grid.  This is done to facilitate bounds checking with a grid index lookup, but
I will do this differently in subsequent iterations.
"""

import warnings
import numpy as np


def walk(num_steps=100000, check_bounds=False):
    """Walk a random walker for n steps.

    Args:
        num_steps: number of steps
        check_bounds: whether or not to check the bounds of the walker

    """
    walker = Walker(field_range=(100, 100), start_pos=(50, 50))
    for _ in range(num_steps):
        walker.step(check_bounds=check_bounds)
    return walker


class Walker():
    """ Defines a random walker which walks on a grid.

    Steps are taken in terms of indicies on a 2D grid.
        
    The grid is defined to start at (0,0) and extend to whatever range we
    specify. Offset can be added if grid is desired to be shifted.

    An internal structure, grid, is used to track where the walker is. Note
    that printing the grid will look wrong because we use a numpy array to
    represent the grid - the first dimension of the array is set to the maximum
    size of the x-space (field_range[0]), the second dimension of the array is
    set to the maximum size of the y-space (field_range[1]).

    Since the first index of a 2D array is the 'row position' and the second
    index of a 2D array is the 'column position', the way that position is
    stored will appear transposed when printed. Just FYI.
    """

    def __init__(self, field_range=(50, 50), start_pos=(0, 0)):
        """Defines the space a walker can walk in (2D grid) and start position.


        Args:
            field_range Tuple(int, int): The (x,y) coordinate of the upper x
                bound and the upper y bound
            start_pos Tuple(int, int): The (x,y) coordinate of the starting
                position of the walker.
        """

        x_max, y_max = field_range[0], field_range[1]
        self.grid = np.zeros((x_max, y_max))
        self.pos = (start_pos[0], start_pos[1])

        self.history = [self.pos]


    def check_valid(self, pos):
        """Determines whether or not the current position is valid.

        Whether or not a position is valid is based on the rules of the board.
        For example, if the position is outside of the board, this is always
        invalid.

        Other rules that can be defined:
            - Already visited site then invalid
            - Number of crossings exceeds x then invalid

        The only default rule is that you cannot be outside the board.

        Args:
            pos: (x, y) position
        """
        x, y = pos[0], pos[1]

        try:
            test = self.grid[x, y]
        except IndexError:
            return False
        if x < 0 or y < 0:
            return False
        return True


    def _show_pos_ascii(self):
        """Put an -1 where the Walker is at.

        Grid is displayed with (0,0) on the lower left, with ascending x to the
        right and ascending y up. We have to play some games to make this print
        right.
        """
        l, w = self.grid.shape
        total = l * w
        vis = np.array(['_' for _ in range(total)], dtype=str).reshape((w, l))
        vis[self.pos[1], self.pos[0]] = 'X'
        print(vis[::-1,:])


    def show_pos(self, option="ascii"):
        '''Shows the position of the walker.

        Args:
            option (str): The type of visualization to use
        '''
        if option == 'ascii':
            self._show_pos_ascii()
        else:
            warnings.warn(("Option {} is not supported for"
                " visualization. Defaulting to 'ascii'").format(option)
            )


    def _step(self):
        """Step up down left or right"""
        left = 0
        right = 1
        up = 2
        down = 3
        x, y = 0, 1
        direction = np.random.randint(0, 4)
        pos = self.pos
        select = {
            left: (pos[x] - 1, pos[y]),
            right: (pos[x] + 1, pos[y]),
            up: (pos[x], pos[y] + 1),
            down: (pos[x], pos[y] - 1),
        }
        return select[direction]


    def step(self, check_bounds=True):
        pos = self._step()
        if check_bounds:
            while not self.check_valid(pos):
                pos = self._step()
        self.history.append(pos)
        self.pos = pos

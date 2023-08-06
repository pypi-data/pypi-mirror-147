"""
GAMES for :mod:`conway_pygame` application.

:creationdate:  18/04/2022 21:58
:moduleauthor: François GUÉRIN <fguerin@ville-tourcoing.fr>
:modulename: conway_pygame.GAMES
"""
import logging
import random
from typing import List, Sequence

__author__ = "fguerin"
logger = logging.getLogger(__name__)


class CellArray:
    """A 2D array of cells."""

    _cells: List[List[int]]

    def __init__(self, width, height, states: Sequence[int], initial_state: int = 0):
        """Initialize the cell array."""
        self.width = width
        self.height = height
        self.state_class: Sequence[int] = states
        self._cells = [[initial_state for _ in range(width)] for __ in range(height)]

    def get_cell(self, x, y):
        """Get a cell at a position."""
        return self._cells[y][x]

    def set_cell(self, x, y, state: int):
        """Set a cell at a position."""
        self._cells[y][x] = state

    def get_neighbours(self, x, y):
        """Return the neighbors of the cell at x, y."""
        x_plus_1 = (x + 1) % self.width
        x_minus_1 = (x - 1) if x > 1 else self.width - 1
        y_plus_1 = (y + 1) % self.height
        y_minus_1 = (y - 1) if y > 1 else self.height - 1

        return [
            self.get_cell(x_minus_1, y_minus_1),
            self.get_cell(x_minus_1, y),
            self.get_cell(x_minus_1, y_plus_1),
            self.get_cell(x_plus_1, y_minus_1),
            self.get_cell(x_plus_1, y),
            self.get_cell(x_plus_1, y_plus_1),
            self.get_cell(x, y_plus_1),
            self.get_cell(x, y_minus_1),
        ]

    def random_alive(self, initial_state: int = 0):
        """Randomly set a cell to alive."""
        _x = random.randint(0, self.width - 1)
        _y = random.randint(0, self.height - 1)
        _choices = [state for state in self.state_class if state != initial_state]
        self.set_cell(_x, _y, random.choice(_choices))

    def get_state(self, x, y) -> int:
        """Return True if the cell at x, y is alive."""
        return self.get_cell(x, y)

    def set_state(self, x, y, state: int) -> None:
        """Set the cell at x, y to alive."""
        self.set_cell(x, y, state)

    def alive_neighbours(self, x, y) -> List[int]:
        """Return the alive neighbors of the cell at x, y."""
        _neighbours = self.get_neighbours(x, y)
        # logging.debug(f"Neighbours: {pprint.pformat(_neighbours)}")
        return [neighbour for neighbour in _neighbours if neighbour != 0]

    def count_alive_neighbours(self, x, y) -> int:
        """Return the number of alive neighbors of the cell at x, y."""
        return len(self.alive_neighbours(x, y))

    @property
    def cells(self):
        """Return the cells."""
        return self._cells

    @cells.setter
    def cells(self, cells):
        """Set the cells."""
        self._cells = cells


class GameOfLife:
    """Game of life."""

    _states: Sequence[int] = (0, 1)
    _initial_state: int = 0

    def __init__(self, width, height, initial_alive_cells: int = 100):
        """Initialize the game."""
        self.width = width
        self.height = height
        self._cells = CellArray(width, height, states=self._states, initial_state=self._initial_state)
        # Initialize random cells
        for _ in range(initial_alive_cells):
            self._cells.random_alive(self._initial_state)
        logging.info(
            f"{self.__class__.__name__}::Initialized with {self.width}×{self.height} - "
            f"Starts with {initial_alive_cells} alive cells "
            f"({initial_alive_cells / (self.width * self.height) * 100:.2f}%)."
        )

    def update(self):
        """Update the cell array with the next generation."""
        self._cells = self.next_generation()

    @property
    def states(self):
        """Return the states."""
        return self._states

    @property
    def cells(self):
        """Return the cells."""
        return self._cells

    @cells.setter
    def cells(self, cells):
        """Set the cells."""
        self._cells = cells

    def next_generation(self):
        """Compute the next generation."""
        logging.debug(f"{self.__class__.__name__}::Next generation")
        next_cells = CellArray(self.width, self.height, states=self._states)
        for x in range(self.width):
            for y in range(self.height):
                _alive_neighbours = self.cells.alive_neighbours(x, y)
                _alive_neighbours_count = len(_alive_neighbours)
                _current_state = self.cells.get_state(x, y)

                next_cells.set_state(x, y, self.next_state(_current_state, _alive_neighbours, _alive_neighbours_count))

        return next_cells

    def next_state(self, current_state, alive_neighbours, alive_neighbours_count) -> int:
        """Return the next state of the cell."""
        raise NotImplementedError


class Conway(GameOfLife):
    """
    Conway's Game of Life.

    .. note::
       Rules: B3/S23
    """

    def next_state(self, current_state, alive_neighbours, alive_neighbours_count):
        """Return the next state of the cell."""
        if current_state == 0:
            if alive_neighbours_count == 3:
                return 1
        else:
            if alive_neighbours_count in (2, 3):
                return 1
        return 0


class HighLife(GameOfLife):
    """
    HighLife is a game of life with a few changes.

    .. note::
       Rules: B36/S23
    """

    def next_state(self, current_state, alive_neighbours, alive_neighbours_count) -> int:
        """Return the next state of the cell."""
        if current_state == 0 and alive_neighbours_count in (3, 6):
            return 1
        if current_state == 1 and alive_neighbours_count in (2, 3):
            return 1
        return 0


class DayAndNight(GameOfLife):
    """
    DayAndNight is a game of life with a few changes.

    .. note::
       Rules: B3678/S345678
    """

    _initial_state: int = 0

    def next_state(self, current_state, alive_neighbours, alive_neighbours_count) -> int:
        """Return the next state of the cell."""
        if current_state == 0:
            if alive_neighbours_count in (3, 6, 7, 8):
                return 1
        else:
            if alive_neighbours_count in (3, 4, 6, 7, 8):
                return 1
        return 0


class Immigration(GameOfLife):
    """
    Immigration is a game of life with a few changes.

    .. note::
       Rules: B3/S23 - 2 alive states
    """

    _states: Sequence[int] = (0, 1, 2)

    def next_state(self, current_state, alive_neighbours, alive_neighbours_count) -> int:
        """Return the next state of the cell."""
        alive_1_count = len([cell for cell in alive_neighbours if cell == 1])
        if current_state == 0:
            if alive_neighbours_count == 3:
                if 2 <= alive_1_count <= 3:
                    return 1
                else:
                    return 2
        else:
            if alive_neighbours_count in (2, 3):
                return current_state
        return 0


class QuadLife(GameOfLife):
    """
    Replicator is a game of life with a few changes.

    .. note::
       Rules: This one uses standard conway's rules, but uses 4 "alive" cell states.
    """

    _states: Sequence[int] = (0, 1, 2, 3, 4)

    def next_state(self, current_state, alive_neighbours, alive_neighbours_count) -> int:
        """Return the next state of the cell."""
        _new_state = 0
        if alive_neighbours_count:
            _new_state = max(alive_neighbours, key=alive_neighbours.count)
            if isinstance(_new_state, list):
                _new_state = _new_state[0]

        if current_state == 0 and alive_neighbours_count == 3:
            _states_set = set(alive_neighbours)
            if _states_set == {1, 2, 3}:
                return 4
            elif _states_set == {2, 3, 4}:
                return 1
            elif _states_set == {3, 4, 1}:
                return 2
            elif _states_set == {4, 1, 2}:
                return 3
            return _new_state

        if current_state != 0 and alive_neighbours_count in (2, 3):
            return _new_state

        return 0


class Replicator(GameOfLife):
    """
    Replicator is a game of life with a few changes.

    .. note::
       Rules: B1357/S1357
    """

    def next_state(self, current_state, alive_neighbours, alive_neighbours_count) -> int:
        """Return the next state of the cell."""
        if current_state == 0:
            if alive_neighbours_count in (1, 3, 5, 7):
                return 1
        else:
            if alive_neighbours_count in (1, 3, 5, 7):
                return 1
        return 0


class Flakes(GameOfLife):
    """
    Flakes is a game of life with a few changes.

    .. note::
       Rules: B3/S012345678
    """

    def next_state(self, current_state, alive_neighbours, alive_neighbours_count) -> int:
        """Return the next state of the cell."""
        if current_state == 0:
            if alive_neighbours_count == 3:
                return 1
        else:
            if 0 <= alive_neighbours_count <= 8:
                return 1
        return 0


class ThirtyFourLife(GameOfLife):
    """
    ThirtyFourLife is a game of life with a few changes.

    .. note::
       Rules: B34/S34
    """

    def next_state(self, current_state, alive_neighbours, alive_neighbours_count) -> int:
        """Return the next state of the cell."""
        if current_state == 0:
            if alive_neighbours_count in (3, 4):
                return 1
        else:
            if 3 <= alive_neighbours_count <= 4:
                return 1
        return 0


class Amoeba(GameOfLife):
    """
    Amoeba is a game of life with a few changes.

    .. note::
       Rules: B357/S1358
    """

    def next_state(self, current_state, alive_neighbours, alive_neighbours_count) -> int:
        """Return the next state of the cell."""
        if current_state == 0:
            if alive_neighbours_count in (3, 5, 7):
                return 1
        else:
            if alive_neighbours_count in (1, 3, 5, 8):
                return 1
        return 0


class IceBall(GameOfLife):
    """
    IceBall is a game of life with a few changes.

    .. note::
       Rules: B25678/S5678
    """

    def next_state(self, current_state, alive_neighbours, alive_neighbours_count) -> int:
        """Return the next state of the cell."""
        if current_state == 0:
            if alive_neighbours_count in (2, 5, 6, 8):
                return 1
        else:
            if alive_neighbours_count in (5, 6, 7, 8):
                return 1
        return 0


class Diamoeba(GameOfLife):
    """
    Diamoeba is a game of life with a few changes.

    .. note::
       Rules: B35678/S5678
    """

    def next_state(self, current_state, alive_neighbours, alive_neighbours_count) -> int:
        """Return the next state of the cell."""
        if current_state == 0:
            if alive_neighbours_count == 3 or 5 <= alive_neighbours_count <= 8:
                return 1
        else:
            if 5 <= alive_neighbours_count <= 8:
                return 1
        return 0


class Maze(GameOfLife):
    """
    Maze is a game of life with a few changes.

    .. note::
       Rules: B3/S12345
    """

    def next_state(self, current_state, alive_neighbours, alive_neighbours_count) -> int:
        """Return the next state of the cell."""
        if current_state == 0:
            if alive_neighbours_count == 3:
                return 1
        else:
            if 1 <= alive_neighbours_count <= 5:
                return 1
        return 0


class SnowLife(GameOfLife):
    """
    SnowLife is a game of life with a few changes.

    .. note::
       Rules: B3/S1237
    """

    def next_state(self, current_state, alive_neighbours, alive_neighbours_count) -> int:
        """Return the next state of the cell."""
        if current_state == 0:
            if alive_neighbours_count == 3:
                return 1
        else:
            if alive_neighbours_count in (1, 2, 3, 7):
                return 1
        return 0


class Coral(GameOfLife):
    """
    Coral is a game of life with a few changes.

    .. note::
       Rules: B3/S45678
    """

    def next_state(self, current_state, alive_neighbours, alive_neighbours_count) -> int:
        """Return the next state of the cell."""
        if current_state == 0:
            if alive_neighbours_count == 3:
                return 1
        else:
            if 4 <= alive_neighbours_count <= 8:
                return 1
        return 0


class WalledCities(GameOfLife):
    """
    Walled Cities is a variant of Conway's Game of Life.

    .. note::
       Rules: B45678/S2345
    """

    def next_state(self, current_state, alive_neighbours, alive_neighbours_count) -> int:
        """Return the next state of the cell."""
        if current_state == 0:
            if alive_neighbours_count in (4, 5, 6, 7, 8):
                return 1
        else:
            if alive_neighbours_count in (2, 3, 4, 5):
                return 1
        return 0


class Seeds(GameOfLife):
    """
    Seeds is a game of life with a few changes.

    .. note::
       Rules: B2/S
    """

    def next_state(self, current_state, alive_neighbours, alive_neighbours_count) -> int:
        """Return the next state of the cell."""
        if current_state == 0:
            if alive_neighbours_count == 2:
                return 1
        return 0


class TwoXTwo(GameOfLife):
    """
    2x2 is a special case of the Game of Life.

    .. note::
       Rules: B36/S125
    """

    def next_state(self, current_state, alive_neighbours, alive_neighbours_count) -> int:
        """Return the next state of the cell."""
        if current_state == 0:
            if alive_neighbours_count in (3, 6):
                return 1
        else:
            if alive_neighbours_count in (1, 2, 5):
                return 1
        return 0


class Morley(GameOfLife):
    """
    Morley's Game of Life.

    .. note::
       Rules: B368/S245
    """

    def next_state(self, current_state, alive_neighbours, alive_neighbours_count) -> int:
        """Return the next state of the cell."""
        if current_state == 0:
            if alive_neighbours_count in (3, 6, 8):
                return 1
        else:
            if alive_neighbours_count in (2, 4, 5):
                return 1
        return 0


class Anneal(GameOfLife):
    """
    Anneal is a variation of Conway's Game of Life.

    .. note::
       Rules: B4678/S35678
    """

    def next_state(self, current_state, alive_neighbours, alive_neighbours_count) -> int:
        """Return the next state of the cell."""
        if current_state == 0:
            if alive_neighbours_count in (4, 6, 7, 8):
                return 1
        else:
            if alive_neighbours_count in (3, 5, 6, 7, 8):
                return 1
        return 0

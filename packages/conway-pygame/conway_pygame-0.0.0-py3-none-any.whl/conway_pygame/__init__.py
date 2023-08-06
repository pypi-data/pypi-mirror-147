"""Conway's game of life."""
import logging
import random
from pathlib import Path
from time import sleep
from typing import List

import click
import pygame
from pygame.locals import *  # noqa

__version__ = VERSION = "0.1.0"

CELL_SIZE = 6
ASSETS_DIR = (Path(__file__).parent / "assets").resolve()
DEBUG = False
FRAME_INTERVAL = 0.1  # Used if DEBUG is True


@click.command(name="conway_pygame")
@click.option("-w", "--width", default=160, help="Width of the grid.")
@click.option("-h", "--height", default=120, help="Height of the grid.")
@click.option("-n", "--initial", default=2000, help="Number of living cells at start.")
@click.option(
    "-d",
    "--debug",
    default=False,
    is_flag=True,
    help="DEBUG mode - Slow down the game and write rounds to stdout.",
)
@click.version_option(version=VERSION, message="conway_pygame %(version)s")
def start_conway(width: int, height: int, initial: int, debug: bool) -> None:
    """Conway's game of life using `pygame <https://www.pygame.org/>`_."""
    global DEBUG
    if debug:
        DEBUG = True
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)

    app = App(
        width=width,
        height=height,
        cell_size=CELL_SIZE,
        initial_alive_cells=initial,
    )
    app.on_execute()


class App:
    """Graphic application to display the game."""

    _image_alive = None
    _image_dead = None
    _generation = 0

    def __init__(self, width: int, height: int, cell_size: int, initial_alive_cells: int = 100):
        """Initialize the windowed application."""
        self.width = width
        self.height = height

        self.cell_size = cell_size
        self._display_surf = None
        self._running = True

        self.game_of_life = GameOfLife(
            width=self.width,
            height=self.height,
            initial_alive_cells=initial_alive_cells,
        )

    def on_init(self):
        """Initialize the application window."""
        pygame.init()
        self._display_surf = pygame.display.set_mode(
            (self.cell_size * self.width, self.cell_size * self.height),
            pygame.HWSURFACE | pygame.DOUBLEBUF | pygame.HWACCEL,
            16,
        )
        self._image_alive = pygame.image.load(ASSETS_DIR / "alive.png").convert()
        self._image_dead = pygame.image.load(ASSETS_DIR / "dead.png").convert()

        self._running = True
        return self._running

    def on_event(self, event):
        """Manage events."""
        if event.type == pygame.QUIT:
            self._running = False
            logging.info(f"Quit event received - {self._generation} rounds played.")

    def on_loop(self):
        """Manage the main loop actions."""
        logging.debug(f"on_loop {self._generation}")
        self.game_of_life.update()
        DEBUG and sleep(FRAME_INTERVAL)
        self._generation += 1

    def on_render(self):
        """Render the frame."""
        for y in range(self.game_of_life.height):
            for x in range(self.game_of_life.width):
                if self.game_of_life.cells.is_alive(x, y):
                    self._display_surf.blit(self._image_alive, (x * self.cell_size, y * self.cell_size))
                else:
                    self._display_surf.blit(self._image_dead, (x * self.cell_size, y * self.cell_size))
        pygame.display.flip()

    def on_cleanup(self):
        """Cleanup the game."""
        pygame.quit()

    def on_execute(self):
        """Execute the game."""
        if self.on_init() == False:
            self._running = False

        while self._running:
            for event in pygame.event.get():
                self.on_event(event)
            self.on_loop()
            self.on_render()
        self.on_cleanup()


class Cell:
    """A cell in the universe."""

    def __init__(self, x: int, y: int, is_alive: bool):
        """Initialize the cell"""
        self.x: int = x
        self.y: int = y
        self.is_alive: bool = is_alive

    def __repr__(self):
        """Get the representation of a cell"""
        return f"Cell({self.x}, {self.y}, {self.is_alive})"

    def __eq__(self, other):
        """Cherck if a celll is equal to another one."""
        return self.x == other.x and self.y == other.y and self.is_alive == other.is_alive


class CellArray:
    """A 2D array of cells."""

    _cells: List[List[Cell]]

    def __init__(self, width, height):
        """Initialize the cell array."""
        self.width = width
        self.height = height
        self._cells = [[Cell(x, y, False) for x in range(width)] for y in range(height)]

    def get(self, x, y):
        """Get a cell at a position."""
        return self._cells[y][x]

    def set(self, x, y, is_alive):
        """Set a cell at a position."""
        self._cells[y][x] = Cell(x, y, is_alive)

    def get_neighbors(self, x, y):
        """Return the neighbors of the cell at x, y."""
        x_plus_1 = (x + 1) % self.width
        x_minus_1 = (x - 1) if x > 1 else self.width - 1
        y_plus_1 = (y + 1) % self.height
        y_minus_1 = (y - 1) if y > 1 else self.height - 1

        return [
            self.get(x_minus_1, y_minus_1),
            self.get(x_minus_1, y),
            self.get(x_minus_1, y_plus_1),
            self.get(x_plus_1, y_minus_1),
            self.get(x_plus_1, y),
            self.get(x_plus_1, y_plus_1),
            self.get(x, y_plus_1),
            self.get(x, y_minus_1),
        ]

    def random_alive(self):
        """Randomly set a cell to alive."""
        x = random.randint(0, self.width - 1)
        y = random.randint(0, self.height - 1)
        self.set(x, y, True)

    def is_alive(self, x, y) -> bool:
        """Return True if the cell at x, y is alive."""
        return self.get(x, y).is_alive

    def set_alive(self, x, y):
        """Set the cell at x, y to alive."""
        self.set(x, y, True)

    def set_dead(self, x, y):
        """Set the cell at x, y to dead."""
        self.set(x, y, False)

    def count_alive_neighbours(self, x, y):
        """Return the number of alive neighbors of the cell at x, y."""
        return sum(1 for neighbor in self.get_neighbors(x, y) if neighbor.is_alive)

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

    def __init__(self, width, height, initial_alive_cells: int = 100):
        """Initialize the game."""
        self.width = width
        self.height = height
        self.cells = CellArray(width, height)
        for _ in range(initial_alive_cells):
            self.cells.random_alive()
        logging.info(f"Initialized with {self.width}×{self.height} - {initial_alive_cells} alive cells.")

    def next_generation(self) -> CellArray:
        """Compute the next generation."""
        next_cells = CellArray(self.width, self.height)
        for x in range(self.width):
            for y in range(self.height):
                alive_neighbors = self.cells.count_alive_neighbours(x, y)
                if not self.cells.is_alive(x, y) and alive_neighbors == 3:
                    next_cells.set_alive(x, y)
                    continue
                if alive_neighbors in (2, 3):
                    if self.cells.is_alive(x, y):
                        next_cells.set_alive(x, y)
                    else:
                        next_cells.set_dead(x, y)
                    continue
        return next_cells

    def update(self):
        """Update the cell array with the next generation."""
        self.cells = self.next_generation()

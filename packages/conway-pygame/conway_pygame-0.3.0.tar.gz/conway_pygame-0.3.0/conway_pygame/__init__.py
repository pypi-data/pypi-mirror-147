"""Conway's game of life."""
import logging
from pathlib import Path
from time import sleep
from typing import Dict, List, Optional, Type

import click
import pygame
from pygame.locals import *  # noqa

from .games import (
    Amoeba,
    Anneal,
    Conway,
    Coral,
    DayAndNight,
    Diamoeba,
    Flakes,
    GameOfLife,
    HighLife,
    IceBall,
    Immigration,
    Maze,
    Morley,
    QuadLife,
    Replicator,
    Seeds,
    SnowLife,
    ThirtyFourLife,
    TwoXTwo,
    WalledCities,
)

__version__ = VERSION = "0.3.0"

CELL_SIZE = 6
ASSETS_DIR = (Path(__file__).parent / "assets").resolve()
DEBUG = False
FRAME_INTERVAL_SEC = 0.1  # Used if DEBUG is True

GAMES: Dict[str, Type[GameOfLife]] = {
    "2x2": TwoXTwo,
    "34life": ThirtyFourLife,
    "amoeba": Amoeba,
    "anneal": Anneal,
    "conway": Conway,
    "coral": Coral,
    "dayandnight": DayAndNight,
    "diamoeba": Diamoeba,
    "flakes": Flakes,
    "highlife": HighLife,
    "iceball": IceBall,
    "immigration": Immigration,
    "maze": Maze,
    "morley": Morley,
    "quadlife": QuadLife,
    "replicator": Replicator,
    "seeds": Seeds,
    "snowlife": SnowLife,
    "walledcities": WalledCities,
}


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
@click.argument(
    "game",
    default="conway",
    type=click.Choice(
        list(GAMES.keys()),
        case_sensitive=False,
    ),
    nargs=1,
)
@click.version_option(version=VERSION, message="conway_pygame %(version)s")
def start_conway(width: int, height: int, initial: int, debug: bool, game: str) -> None:
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
        game=game,
    )
    app.on_execute()


class App:
    """Graphic application to display the game."""

    _images: Optional[List[pygame.Surface]] = None
    _generation: int = 0
    _game: Optional[Type["GameOfLife"]] = None
    _game_of_life: Optional["GameOfLife"] = None

    def __init__(
        self,
        width: int,
        height: int,
        cell_size: int,
        initial_alive_cells: int = 100,
        game: str = "conway",
    ) -> None:
        """Initialize the windowed application."""
        self.width = width
        self.height = height

        self.cell_size = cell_size
        self._display_surf = None
        self._running = True

        self._game = GAMES.get(game)
        if self._game is None:
            raise NotImplementedError(f"Game {game} not implemented.")
        logging.info(f"{self.__class__.__name__}() Using game {self._game.__name__}")
        self._game_of_life = self._game(
            width=self.width,
            height=self.height,
            initial_alive_cells=initial_alive_cells,
        )

    def on_init(self):
        """Initialize the application window."""
        pygame.init()
        pygame.display.set_caption(self._game.__name__)
        self._display_surf = pygame.display.set_mode(
            (self.cell_size * self.width, self.cell_size * self.height),
            pygame.HWSURFACE | pygame.DOUBLEBUF | pygame.HWACCEL,
            16,
        )
        self._images = []
        for state in self._game_of_life.states:
            self._images.append(pygame.image.load(ASSETS_DIR / f"alive_{state}.png").convert())

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
        self._game_of_life.update()
        DEBUG and sleep(FRAME_INTERVAL_SEC)
        self._generation += 1

    def on_render(self):
        """Render the frame."""
        for y in range(self._game_of_life.height):
            for x in range(self._game_of_life.width):
                _state = self._game_of_life.cells.get_state(x, y)
                self._display_surf.blit(self._images[_state], (x * self.cell_size, y * self.cell_size))
        pygame.display.flip()

    def on_cleanup(self):
        """Cleanup the game."""
        pygame.quit()

    def on_execute(self):
        """Execute the game."""
        if self.on_init() is False:
            self._running = False

        while self._running:
            for event in pygame.event.get():
                self.on_event(event)
            self.on_loop()
            self.on_render()
        self.on_cleanup()

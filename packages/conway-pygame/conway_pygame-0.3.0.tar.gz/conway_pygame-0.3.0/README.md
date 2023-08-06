# Conway's game of life

This is an implementation of the Conway's game of life using pygame.

![Immigration Game Of Life](./.images/Immigration.png)

The Universe is circular : left border touch the right one, top border touch the bottom one.

Many games are implemented, the rules come from [https://en.wikipedia.org/wiki/Conway%27s_Game_of_Life](https://en.wikipedia.org/wiki/Conway%27s_Game_of_Life).

I've only implemented "simple" games, using the 8 cells around the current cell.

## Available Games
+ [conway classic](https://en.wikipedia.org/wiki/Conway%27s_Game_of_Life)
+ [HighLife](https://en.wikipedia.org/wiki/Highlife_(cellular_automaton))
+ [Day&Night](https://en.wikipedia.org/wiki/Day_and_Night_(cellular_automaton))
+ [Immigration](https://fr.wikipedia.org/wiki/Immigration_(automate_cellulaire)) (With colors !)
+ [QuadLife](https://fr.wikipedia.org/wiki/QuadLife) (more colors !)
+ [Life without death (Flakes)](https://en.wikipedia.org/wiki/Life_without_Death)
+ 34 Life B34/S34
+ [Seeds](https://en.wikipedia.org/wiki/Seeds_(cellular_automaton))
+ Diamoeba B35678/S5678
+ 2x2 B36/S125
+ Morley B368/S245
+ Anneal B4678/S35678


## Installation

### Using pip

```shell
$ cd /path/to/the/projects
$ mkdir Conway && cd Conway
python3 -m venv ./venv
source ./venv/bin/activate
pip install conway-pygame
```

When installed with pip, you can use the `conway_pygame` command to play a game.

### Installation with git
```shell
$ git clone https://gitlab.com/frague59/conway.git
$ cd conway
$ python3 -m venv ./venv
$ . venv/bin/activate
$ pip install -r ./requirements.txt
```

## Usage

### With GIT install
```shell
$ python3 -m conway_pygame --help
pygame 2.1.2 (SDL 2.0.16, Python 3.9.12)
Hello from the pygame community. https://www.pygame.org/contribute.html
Usage: python -m conway_pygame [OPTIONS] [[conway|highlife|dayandnight|immigra
                               tion|quadlife|replicator|flakes|34life|diamoeba
                               |seeds|2x2|morley|anneal]]

  Conway's game of life using `pygame <https://www.pygame.org/>`_.

Options:
  -w, --width INTEGER    Width of the grid.
  -h, --height INTEGER   Height of the grid.
  -n, --initial INTEGER  Number of living cells at start.
  -d, --debug            DEBUG mode - Slow down the game and write rounds to
                         stdout.
  --version              Show the version and exit.
  --help                 Show this message and exit.
```

### With pip install
```shell
$ conway_pygame --help
```

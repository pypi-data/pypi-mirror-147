import curses

from .pacman import *


def main(stdscr):
    pacman = Pacman(0, 0, 80, 24, D_UP)


def run():
    curses.wrapper(main)

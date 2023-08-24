from graphics import Window
from maze import Maze
import sys

def main():
    sys.setrecursionlimit(10000)

    window = Window(800, 600)
    # see maze.py for constuctor parameters
    maze = Maze(150, 100, 20, 20, 20, 20, window)
    print("maze created")
    is_solveable = maze.solve()
    if not is_solveable:
        print("maze can not be solved!")
    else:
        print("maze solved!")
    window.wait_for_close()


main()
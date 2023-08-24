from graphics import Window, Point, Line
from cell import Cell
import random
import time

class Maze:
    def __init__(self, x1, y1, num_rows, num_cols, cell_size_x, cell_size_y, window=None, seed=None):
        self._x1 = x1
        self._y1 = y1
        self._num_rows = num_rows
        self._num_cols = num_cols
        self._cell_size_x = cell_size_x
        self._cell_size_y = cell_size_y
        self._window = window
        self._cells = []
        self._create_cells()
        random.seed(seed) # if seed is not None, i.e an integer, the same maze will always be generated
        self._break_entrance_and_exit()
        self._break_walls()
        self._reset_cells_visited()
    
    def _create_cells(self):
        self._cells = [[Cell(self._window) for _ in range(self._num_rows)] for _ in range(self._num_cols)]

        for i in range(self._num_cols):
            for j in range(self._num_rows):
                self._draw_cell(i, j)
    
    def _draw_cell(self, i, j):
        if self._window is None:
            return
        cell_x1 = i * self._cell_size_x + self._x1
        cell_y1 = j * self._cell_size_y + self._y1
        cell_x2 = cell_x1 + self._cell_size_x
        cell_y2 = cell_y1 + self._cell_size_y
        p1 = Point(cell_x1, cell_y1)
        p2 = Point(cell_x2, cell_y2)
        self._cells[i][j].draw(p1, p2)
        self._animate()
    
    def _animate(self):
        if self._window is None:
            return
        self._window.redraw()
        time.sleep(0.05)
    
    def _break_entrance_and_exit(self):
        self._cells[0][0].has_top_wall = False
        self._draw_cell(0, 0)
        self._cells[len(self._cells) - 1][len(self._cells[0]) - 1].has_bottom_wall = False
        self._draw_cell(len(self._cells) - 1, len(self._cells[0]) - 1)
    
    
    def __break_walls_r(self, i, j):
        self._cells[i][j].visited = True

        # check all cells directly adjacent to the current cell, if such cell hasn't been visited,
        # include it as a possible cell to move into
        while True:
            poss_direction = []
            if (i - 1 > -1) and (not self._cells[i-1][j].visited):
                poss_direction.append((i - 1, j))
            if (j - 1 > -1) and (not self._cells[i][j-1].visited):
                poss_direction.append((i, j - 1))
            if (i + 1 < self._num_cols) and (not self._cells[i+1][j].visited):
                poss_direction.append((i + 1, j))
            if (j + 1 < self._num_rows) and (not self._cells[i][j+1].visited):
                poss_direction.append((i, j + 1))
            if len(poss_direction) == 0:
                self._draw_cell(i, j)
                return
            
            # randomly choose an adjacent cell
            chosen = random.choice(poss_direction)

            # remove the walls between this cell and the chosen cell in order to move into it
            # if the chosen cell is to the right
            if chosen[0] == i + 1:
                self._cells[i][j].has_right_wall = False
                self._cells[i + 1][j].has_left_wall = False
            # if the chosen cell is to the left
            elif chosen[0] == i - 1:
                self._cells[i][j].has_left_wall = False
                self._cells[i - 1][j].has_right_wall = False
            # if the chosen cell is below
            elif chosen[1] == j + 1:
                self._cells[i][j].has_bottom_wall = False
                self._cells[i][j + 1].has_top_wall = False
            # if the chosen cell is above
            elif chosen[1] == j - 1:
                self._cells[i][j].has_top_wall = False
                self._cells[i][j - 1].has_bottom_wall = False
            
            # move into the chosen the cell
            self.__break_walls_r(chosen[0], chosen[1])
        
    def _break_walls(self):
        self.__break_walls_r(0, 0)
    
    def _reset_cells_visited(self):
        for i in range(self._num_cols):
            for j in range(self._num_rows):
                self._cells[i][j].visited = False
                
    # returns True if this is the end cell or if it leads to the end cell
    # returns False otherwise
    def _solve_r(self, i, j):
        self._animate()
        # mark the current cell as visited
        self._cells[i][j].visited = True

        # if the current cell is the end cell, we're done.
        if i == self._num_cols - 1 and j == self._num_rows - 1:
            return True

        # get the location of the cells directly adjacent to the current cell
        directions = []
        processed = 0
        if i - 1 > -1:
            directions.append((i-1, j))
        if i + 1 < self._num_cols:
            directions.append((i+1, j))
        if j - 1 > -1:
            directions.append((i, j-1))
        if j + 1 < self._num_rows:
            directions.append((i, j+1))
        
        for direction in directions:
            # if direction is left and there are no walls in between the current cell and the cell to its left
            # and that cell hasn't been visited, move left.
            if (direction[0] == i - 1 and (not self._cells[i-1][j].visited) and 
            (not self._cells[i-1][j].has_right_wall) and (not self._cells[i][j].has_left_wall)):
                self._cells[i][j].draw_move(self._cells[i-1][j])
                value = self._solve_r(i - 1, j)
                if value:
                    return True
                else:
                    self._cells[i][j].draw_move(self._cells[i-1][j], True)

            # if direction is right and there are no walls in between the current cell and the cell to its right
            # and that cell hasn't been visited, move right.
            elif (direction[0] == i + 1 and (not self._cells[i+1][j].visited) and 
            (not self._cells[i+1][j].has_left_wall) and (not self._cells[i][j].has_right_wall)):
                self._cells[i][j].draw_move(self._cells[i+1][j])
                value = self._solve_r(i + 1, j)
                if value:
                    return True
                else:
                    self._cells[i][j].draw_move(self._cells[i+1][j], True)

            # if direction is up and there are no walls in between the current cell and the cell above it
            # and that cell hasn't been visited, move up.
            elif (direction[1] == j - 1 and (not self._cells[i][j-1].visited) and 
            (not self._cells[i][j-1].has_bottom_wall) and (not self._cells[i][j].has_top_wall)):
                self._cells[i][j].draw_move(self._cells[i][j-1])
                value = self._solve_r(i, j - 1)
                if value:
                    return True
                else:
                    self._cells[i][j].draw_move(self._cells[i][j-1], True)
            
            # if direction is down and there are no walls in between the current cell and the cell below it
            # and that cell hasn't been visited, move down.
            elif (direction[1] == j + 1 and (not self._cells[i][j+1].visited) and 
            (not self._cells[i][j+1].has_top_wall) and (not self._cells[i][j].has_bottom_wall)):
                self._cells[i][j].draw_move(self._cells[i][j+1])
                value = self._solve_r(i, j + 1)
                if value:
                    return True
                else:
                    self._cells[i][j].draw_move(self._cells[i][j+1], True)
           
            processed += 1

        # if there are no possible directions to move to from the current cell
        if processed == 0:
            return False
    
    # solve the maze using depth-first search
    def solve(self):
        return self._solve_r(0, 0)
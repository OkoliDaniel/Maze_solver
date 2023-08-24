from graphics import Window, Point, Line

class Cell:
    def __init__(self, window=None):
        self.p1 = None
        self.p2 = None
        self.__window = window
        self.has_left_wall = True
        self.has_right_wall = True
        self.has_top_wall = True
        self.has_bottom_wall = True
        self.visited = False
    
    def draw(self, p1, p2):
        if self.__window is None:
            return
        self.p1 = p1
        self.p2 = p2

        right_wall_start = Point(self.p2.x, self.p1.y)
        right_wall_end = self.p2
        right_wall = Line(right_wall_start, right_wall_end)
        left_wall_start = self.p1
        left_wall_end = Point(self.p1.x, self.p2.y)
        left_wall = Line(left_wall_start, left_wall_end)
        top_wall_start = self.p1
        top_wall_end = Point(self.p2.x, self.p1.y)
        top_wall = Line(top_wall_start, top_wall_end)
        bottom_wall_start = Point(self.p1.x, self.p2.y)
        bottom_wall_end = self.p2
        bottom_wall = Line(bottom_wall_start, bottom_wall_end)

        if self.has_right_wall:
            self.__window.draw_line(right_wall, "black")
        else:
            self.__window.draw_line(right_wall, "white")
        if self.has_left_wall:
            self.__window.draw_line(left_wall, "black")
        else:
            self.__window.draw_line(left_wall, "white")
        if self.has_top_wall:
            self.__window.draw_line(top_wall, "black")
        else:
            self.__window.draw_line(top_wall, "white")
        if self.has_bottom_wall:
            self.__window.draw_line(bottom_wall, "black")
        else:
            self.__window.draw_line(bottom_wall, "white")
    
    # draws a move from a cell to another cell by connecting their centers via a line
    def draw_move(self, to_cell, undo=False):
        if self.__window is None:
            return
        fill_colour = "red"
        if undo:
            fill_colour = "gray"
        center_x = (self.p1.x + self.p2.x) / 2
        center_y = (self.p1.y + self.p2.y) / 2
        to_cell_center_x = (to_cell.p1.x + to_cell.p2.x) / 2
        to_cell_center_y = (to_cell.p1.y + to_cell.p2.y) / 2
        cell_center = Point(center_x, center_y)
        to_cell_center = Point(to_cell_center_x, to_cell_center_y)
        center_conn = Line(cell_center, to_cell_center)
        self.__window.draw_line(center_conn, fill_colour)
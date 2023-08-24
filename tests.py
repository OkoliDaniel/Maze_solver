from maze import Maze
import unittest

class Tests(unittest.TestCase):

    maze = Maze(0, 0, 12, 10, 10, 10)

    def test_maze_create_cells(self):
        Tests.maze._break_entrance_and_exit()
        self.assertEqual(
            len(Tests.maze._cells),
            Tests.maze._num_cols,
        )
        self.assertEqual(
            len(Tests.maze._cells[0]),
            Tests.maze._num_rows,
        )
    
    def test_maze_break_entrance_and_exit(self):
        Tests.maze._break_entrance_and_exit()
        self.assertEqual(Tests.maze._cells[0][0].has_top_wall, False)
        self.assertEqual(
            Tests.maze._cells[Tests.maze._num_cols - 1][Tests.maze._num_rows - 1].has_bottom_wall,
            False)
    
    def test_maze_reset_cells_visited(self):
        Tests.maze._break_walls() # Tested through simulation
        Tests.maze._reset_cells_visited()
        for i in range(Tests.maze._num_cols):
            for j in range(Tests.maze._num_rows):
                self.assertEqual(Tests.maze._cells[i][j].visited, False)

if __name__ == "__main__":
    unittest.main()
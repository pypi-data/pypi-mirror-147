from solvers.killer_sudoku.killer_sudoku_solver import KillerSudokuSolver
from solvers.killer_sudoku.grid import Grid


def get_template():
    grid = Grid(6)

    # Define all the sum regions
    # Example taken from: https://www.janko.at/Raetsel/Sudoku/Killer/index.htm
    region = grid.create_sum_region(sum=7)
    region.add_cell(grid.get_cell(0, 0))
    region.add_cell(grid.get_cell(1, 0))
    region.add_cell(grid.get_cell(1, 1))

    region = grid.create_sum_region(sum=8)
    region.add_cell(grid.get_cell(0, 1))
    region.add_cell(grid.get_cell(0, 2))

    region = grid.create_sum_region(sum=5)
    region.add_cell(grid.get_cell(0, 3))
    region.add_cell(grid.get_cell(1, 3))

    region = grid.create_sum_region(sum=12)
    region.add_cell(grid.get_cell(0, 4))
    region.add_cell(grid.get_cell(0, 5))
    region.add_cell(grid.get_cell(1, 4))

    region = grid.create_sum_region(sum=7)
    region.add_cell(grid.get_cell(2, 0))
    region.add_cell(grid.get_cell(2, 1))

    region = grid.create_sum_region(sum=10)
    region.add_cell(grid.get_cell(1, 2))
    region.add_cell(grid.get_cell(2, 2))

    region = grid.create_sum_region(sum=4)
    region.add_cell(grid.get_cell(2, 3))
    region.add_cell(grid.get_cell(2, 4))

    region = grid.create_sum_region(sum=10)
    region.add_cell(grid.get_cell(1, 5))
    region.add_cell(grid.get_cell(2, 5))

    region = grid.create_sum_region(sum=9)
    region.add_cell(grid.get_cell(3, 0))
    region.add_cell(grid.get_cell(4, 0))

    region = grid.create_sum_region(sum=4)
    region.add_cell(grid.get_cell(3, 1))
    region.add_cell(grid.get_cell(3, 2))

    region = grid.create_sum_region(sum=9)
    region.add_cell(grid.get_cell(3, 3))
    region.add_cell(grid.get_cell(4, 3))

    region = grid.create_sum_region(sum=6)
    region.add_cell(grid.get_cell(3, 4))
    region.add_cell(grid.get_cell(3, 5))

    region = grid.create_sum_region(sum=11)
    region.add_cell(grid.get_cell(4, 1))
    region.add_cell(grid.get_cell(5, 0))
    region.add_cell(grid.get_cell(5, 1))

    region = grid.create_sum_region(sum=7)
    region.add_cell(grid.get_cell(4, 2))
    region.add_cell(grid.get_cell(5, 2))

    region = grid.create_sum_region(sum=8)
    region.add_cell(grid.get_cell(5, 3))
    region.add_cell(grid.get_cell(5, 4))

    region = grid.create_sum_region(sum=9)
    region.add_cell(grid.get_cell(4, 4))
    region.add_cell(grid.get_cell(4, 5))
    region.add_cell(grid.get_cell(5, 5))

    # Define all white / gray areas
    # The color doesn't matter.
    # All that matters is that they're separate regions with different constraints.
    region = grid.create_region()
    region.add_cell(grid.get_cell(0, 0))
    region.add_cell(grid.get_cell(0, 1))
    region.add_cell(grid.get_cell(0, 2))
    region.add_cell(grid.get_cell(1, 0))
    region.add_cell(grid.get_cell(1, 1))
    region.add_cell(grid.get_cell(1, 2))

    region = grid.create_region()
    region.add_cell(grid.get_cell(0, 3))
    region.add_cell(grid.get_cell(0, 4))
    region.add_cell(grid.get_cell(0, 5))
    region.add_cell(grid.get_cell(1, 3))
    region.add_cell(grid.get_cell(1, 4))
    region.add_cell(grid.get_cell(1, 5))

    region = grid.create_region()
    region.add_cell(grid.get_cell(2, 0))
    region.add_cell(grid.get_cell(2, 1))
    region.add_cell(grid.get_cell(2, 2))
    region.add_cell(grid.get_cell(3, 0))
    region.add_cell(grid.get_cell(3, 1))
    region.add_cell(grid.get_cell(3, 2))

    region = grid.create_region()
    region.add_cell(grid.get_cell(2, 3))
    region.add_cell(grid.get_cell(2, 4))
    region.add_cell(grid.get_cell(2, 5))
    region.add_cell(grid.get_cell(3, 3))
    region.add_cell(grid.get_cell(3, 4))
    region.add_cell(grid.get_cell(3, 5))

    region = grid.create_region()
    region.add_cell(grid.get_cell(4, 0))
    region.add_cell(grid.get_cell(4, 1))
    region.add_cell(grid.get_cell(4, 2))
    region.add_cell(grid.get_cell(5, 0))
    region.add_cell(grid.get_cell(5, 1))
    region.add_cell(grid.get_cell(5, 2))

    region = grid.create_region()
    region.add_cell(grid.get_cell(4, 3))
    region.add_cell(grid.get_cell(4, 4))
    region.add_cell(grid.get_cell(4, 5))
    region.add_cell(grid.get_cell(5, 3))
    region.add_cell(grid.get_cell(5, 4))
    region.add_cell(grid.get_cell(5, 5))

    return grid


def test_finds_all_solutions():
    solver = KillerSudokuSolver()
    template = get_template()
    solved = solver.solve(template)
    assert solved is not None


def test_solution_is_correct():
    solver = KillerSudokuSolver()
    template = get_template()
    solved = solver.solve(template)
    correct_values = [
        4,
        5,
        3,
        2,
        6,
        1,
        2,
        1,
        6,
        3,
        5,
        4,
        5,
        2,
        4,
        1,
        3,
        6,
        6,
        3,
        1,
        5,
        4,
        2,
        3,
        6,
        2,
        4,
        1,
        5,
        1,
        4,
        5,
        6,
        2,
        3,
    ]
    value_index = 0
    for row in solved.get_rows():
        for cell in row:
            assert cell.value == correct_values[value_index]
            value_index += 1

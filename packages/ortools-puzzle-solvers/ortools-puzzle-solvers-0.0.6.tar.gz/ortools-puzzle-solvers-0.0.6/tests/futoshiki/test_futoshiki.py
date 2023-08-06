from solvers.futoshiki.futoshiki_solver import FutoshikiSolver
from solvers.futoshiki.grid import Grid


def get_template():
    grid = Grid(6)
    # Predefined values
    grid.set_cell_value(0, 2, 5)
    grid.set_cell_value(0, 5, 4)
    grid.set_cell_value(1, 0, 3)
    grid.set_cell_value(1, 5, 1)
    grid.set_cell_value(2, 4, 3)
    grid.set_cell_value(2, 5, 5)
    grid.set_cell_value(3, 3, 2)
    grid.set_cell_value(4, 0, 2)
    grid.set_cell_value(5, 5, 2)
    # Relations
    grid.add_less_than_expr(grid.get_cell(0, 0), grid.get_cell(0, 1))
    grid.add_less_than_expr(grid.get_cell(0, 1), grid.get_cell(1, 1))
    grid.add_less_than_expr(grid.get_cell(2, 1), grid.get_cell(1, 1))
    grid.add_less_than_expr(grid.get_cell(2, 2), grid.get_cell(3, 2))
    grid.add_less_than_expr(grid.get_cell(0, 3), grid.get_cell(1, 3))
    grid.add_less_than_expr(grid.get_cell(2, 5), grid.get_cell(3, 5))
    grid.add_less_than_expr(grid.get_cell(3, 4), grid.get_cell(4, 4))
    grid.add_less_than_expr(grid.get_cell(5, 4), grid.get_cell(5, 5))
    return grid


def test_finds_all_solutions():
    solver = FutoshikiSolver()
    template = get_template()
    solved = solver.solve(template)
    assert solved is not None


def test_solution_is_correct():
    solver = FutoshikiSolver()
    template = get_template()
    solved = solver.solve(template)
    correct_values = [
        1,
        2,
        5,
        3,
        6,
        4,
        3,
        5,
        4,
        6,
        2,
        1,
        6,
        4,
        2,
        1,
        3,
        5,
        5,
        1,
        3,
        2,
        4,
        6,
        2,
        6,
        1,
        4,
        5,
        3,
        4,
        3,
        6,
        5,
        1,
        2,
    ]
    value_index = 0
    for row in solved.get_rows():
        for cell in row:
            assert cell.value == correct_values[value_index]
            value_index += 1

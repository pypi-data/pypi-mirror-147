from ortools.sat.python import cp_model
from solvers.killer_sudoku.grid import Grid


class KillerSudokuSolver:
    def solve(self, grid_template: Grid) -> Grid:
        model = cp_model.CpModel()
        grid_length = grid_template.length
        solver_board = [
            [
                model.NewIntVar(1, grid_length, f"Cell({row},{col})")
                for col in range(grid_length)
            ]
            for row in range(grid_length)
        ]

        for row_index in range(grid_length):
            model.AddAllDifferent(solver_board[row_index])

        for col_index in range(grid_length):
            rows = []
            for row_index in range(grid_length):
                rows.append(solver_board[row_index][col_index])
            model.AddAllDifferent(rows)

        for region in grid_template.get_regions():
            constrained_cells = []
            for cell in region.cells:
                constrained_cells.append(solver_board[cell.row][cell.column])
            model.AddAllDifferent(constrained_cells)

        for sum_region in grid_template.get_sum_regions():
            constrained_cells = []
            for cell in sum_region.cells:
                constrained_cells.append(solver_board[cell.row][cell.column])
            model.AddAllDifferent(constrained_cells)
            summed_cells = sum(constrained_cells)
            model.Add(sum_region.get_sum() == summed_cells)

        solver = cp_model.CpSolver()
        status = solver.Solve(model)
        if status == cp_model.FEASIBLE or status == cp_model.OPTIMAL:
            return self.__to_solved_grid(solver, solver_board)
        else:
            raise Exception(
                f"Killer Sudoku could not be solved. Status = {self.__status_to_message(status)}"
            )

    def __status_to_message(self, status) -> str:
        if status == cp_model.INFEASIBLE:
            return "INFEASIBLE"
        elif status == cp_model.MODEL_INVALID:
            return "MODEL_INVALD"
        else:
            return "UNKNOWN"

    def __to_solved_grid(self, solver, solved_board) -> Grid:
        grid_length = len(solved_board)
        grid = Grid(grid_length)
        for row_index in range(grid_length):
            for column_index in range(grid_length):
                solved_cell_value = solver.Value(solved_board[row_index][column_index])
                cell = grid.get_cell(row_index, column_index)
                cell.set_value(solved_cell_value)
        return grid

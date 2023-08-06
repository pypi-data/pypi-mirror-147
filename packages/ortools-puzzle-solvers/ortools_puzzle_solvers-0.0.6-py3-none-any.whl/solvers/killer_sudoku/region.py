from typing import List
from solvers.killer_sudoku.cell import Cell


class Region:
    def __init__(self) -> None:
        self.cells: List[Cell] = []

    def add_cell(self, cell: Cell) -> None:
        self.cells.append(cell)

    def get_cells(self) -> List[Cell]:
        return self.cells

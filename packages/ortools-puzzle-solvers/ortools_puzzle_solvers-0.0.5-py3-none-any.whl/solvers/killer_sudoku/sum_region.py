from typing import List
from solvers.killer_sudoku.cell import Cell


class SumRegion:
    def __init__(self, sum: int) -> None:
        self.sum = sum
        self.cells: List[Cell] = []

    def add_cell(self, cell: Cell) -> None:
        self.cells.append(cell)

    def get_cells(self) -> List[Cell]:
        return self.cells

    def get_sum(self) -> int:
        return self.sum

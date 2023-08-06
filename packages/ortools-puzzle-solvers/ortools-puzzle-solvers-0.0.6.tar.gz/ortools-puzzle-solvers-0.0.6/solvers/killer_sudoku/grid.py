from typing import List
from solvers.killer_sudoku.cell import Cell
from solvers.killer_sudoku.region import Region
from solvers.killer_sudoku.sum_region import SumRegion


class Grid:
    def __init__(self, length: int) -> None:
        self.length = length
        self.rows: List[List[Cell]] = []
        self.columns: List[List[Cell]] = []
        self.regions: List[Region] = []
        self.sum_regions: List[SumRegion] = []
        self.__init_with_empty_cells()

    def __init_with_empty_cells(self):
        for row in range(self.length):
            new_row = []
            self.rows.append(new_row)
            for column in range(self.length):
                cell = Cell(row, column)
                new_row.append(cell)
        for column in range(self.length):
            new_column = []
            self.columns.append(new_column)
            for row in range(self.length):
                new_column.append(self.rows[row][column])

    def get_cell(self, row: int, column: int) -> Cell:
        return self.rows[row][column]

    def get_rows(self) -> List[List[Cell]]:
        return self.rows

    def get_regions(self) -> List[Region]:
        return self.regions

    def get_sum_regions(self) -> List[SumRegion]:
        return self.sum_regions

    def create_region(self):
        region = Region()
        self.regions.append(region)
        return region

    def create_sum_region(self, sum: int):
        region = SumRegion(sum)
        self.sum_regions.append(region)
        return region

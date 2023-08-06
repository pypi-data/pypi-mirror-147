from typing import Optional


class Cell:
    def __init__(self, row: int, column: int, value: int = None) -> None:
        self.row = row
        self.column = column
        self.value = value

    def set_value(self, new_value: int) -> None:
        self.value = new_value

    def get_value(self) -> Optional[int]:
        return self.value

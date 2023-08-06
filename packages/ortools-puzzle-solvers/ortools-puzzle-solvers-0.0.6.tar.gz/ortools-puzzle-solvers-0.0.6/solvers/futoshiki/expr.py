from solvers.futoshiki.cell import Cell
from solvers.futoshiki.less_than_op import LessThanOp


class Expression:
    def __init__(self, left: Cell, right: Cell, op: LessThanOp) -> None:
        self.left = left
        self.right = right
        self.op = op

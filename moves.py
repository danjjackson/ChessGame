from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum
from typing import Protocol

Position = tuple[int, int]


class Colour(Enum):
    BLANK = -1
    WHITE = 0
    BLACK = 1


@dataclass
class Piece(Protocol):
    colour: Colour
    has_moved: bool


class Board(Protocol):
    def is_empty(self, x: int, y: int) -> bool:
        """Whether the field (x, y) is empty."""
        raise NotImplementedError

    def piece(self, x: int, y: int) -> Piece:
        """Returns the piece at position (x, y)."""
        raise NotImplementedError


class MoveType(ABC):
    def __init__(self, limit: int = 8):
        self.limit = limit

    @abstractmethod
    def get_valid_moves(self, board: Board, x: int, y: int) -> list[Position]:
        pass


class Vertical(MoveType):
    def __init__(self, limit: int = 8, orientation: Colour = Colour.BLANK):
        super().__init__(limit=limit)
        self.orientation = orientation

    def get_valid_moves(self, board: Board, x: int, y: int) -> list[Position]:
        valid_moves: list[Position] = []
        if self.orientation == Colour.WHITE or self.orientation == Colour.BLANK:
            for i in range(1, 8 - x):
                if i > self.limit:
                    break
                if board.is_empty(x + i, y):
                    valid_moves.append((x + i, y))
                elif board.piece(x + i, y).colour != board.piece(x, y).colour:
                    valid_moves.append((x + i, y))
                    break
                else:
                    break

        if self.orientation == Colour.BLACK or self.orientation == Colour.BLANK:
            for i in range(1, x + 1):
                if i > self.limit:
                    break
                if board.is_empty(x - i, y):
                    valid_moves.append((x - i, y))
                elif board.piece(x, y).colour != board.piece(y, x - i).colour:
                    valid_moves.append((x - i, y))
                    break
                else:
                    break
        return valid_moves


class Horizontal(MoveType):
    def get_valid_moves(self, board: Board, x: int, y: int) -> list[Position]:
        valid_moves: list[Position] = []
        for i in range(1, 8 - y):
            if i > self.limit:
                break
            if board.is_empty(x, y + i):
                valid_moves.append((x, y + i))
            elif board.piece(x, y).colour != board.piece(x, y + i).colour:
                valid_moves.append((x, y + i))
                break
            else:
                break

        for i in range(1, y + 1):
            if i > self.limit:
                break
            if board.is_empty(x, y - i):
                valid_moves.append((x, y - i))
            elif board.piece(x, y).colour != board.piece(x, y - i).colour:
                valid_moves.append((x, y - i))
                break
            else:
                break

        return valid_moves


class Diagonal(MoveType):
    def __init__(self, limit: int = 8, orientation: Colour = Colour.BLANK):
        super().__init__(limit=limit)
        self.orientation = orientation

    def get_valid_moves(self, board: Board, x: int, y: int) -> list[Position]:
        valid_moves: list[Position] = []
        for i in range(1, min(8 - x, 8 - y)):
            if i > self.limit:
                break
            if board.is_empty(x + i, y + i):
                valid_moves.append((x + i, y + i))
            elif board.piece(x, y).colour != board.piece(x + i, y + i).colour:
                valid_moves.append((x + i, y + i))
                break
            else:
                break

        for i in range(1, min(x + 1, y + 1)):
            if i > self.limit:
                break
            if board.is_empty(x - i, y - i):
                valid_moves.append((x - i, y - i))
            elif board.piece(x, y).colour != board.piece(y - i, x - i).colour:
                valid_moves.append((x - i, y - i))
                break
            else:
                break

        for i in range(1, min(x + 1, 8 - y)):
            if i > self.limit:
                break
            if board.is_empty(x - i, y + i):
                valid_moves.append((x - i, y + i))
            elif board.piece(x, y).colour != board.piece(x - i, y + i).colour:
                valid_moves.append((x - i, y + i))
                break
            else:
                break

        for i in range(1, min(y + 1, 8 - x)):
            if i > self.limit:
                break
            if board.is_empty(x + 1, y - i):
                valid_moves.append((x + 1, y - i))
            elif board.piece(x, y).colour != board.piece(x + 1, y - i).colour:
                valid_moves.append((x + 1, y - i))
                break
            else:
                break

        return valid_moves


class Knight(MoveType):
    def get_valid_moves(self, board: Board, x: int, y: int) -> list[Position]:
        valid_moves = []
        moves = (
            (x + 1, y + 2),
            (x + 1, y - 2),
            (x - 1, y + 2),
            (x - 1, y - 2),
            (x + 2, y + 1),
            (x + 2, y - 1),
            (x - 2, y + 1),
            (x - 2, y - 1),
        )
        for new_x, new_y in moves:
            if 0 <= new_x <= 7 and 0 <= new_y <= 7:
                if (
                    board.is_empty(x, y)
                    or board.piece(x, y).colour != board.piece(new_x, new_y).colour
                ):
                    valid_moves.append((new_x, new_y))
        return valid_moves


class ShortCastle(MoveType):
    def get_valid_moves(self, board: Board, x: int, y: int) -> list[Position]:
        valid_moves = []

        # print(board.piece(x, y).has_moved)
        if (
            not board.piece(x, y).has_moved
            and not board.piece(x, y + 3).has_moved
            and board.is_empty(x, y + 1)
            and board.is_empty(x, y + 1)
        ):
            valid_moves.append((x, y + 2))

        return valid_moves


class LongCastle(MoveType):
    def get_valid_moves(self, board: Board, x: int, y: int) -> list[Position]:
        valid_moves = []
        if (
            not board.piece(x, y).has_moved
            and not board.piece(x, y - 4).has_moved
            and board.is_empty(x, y - 1)
            and board.is_empty(x, y - 2)
            and board.is_empty(x, y - 2)
        ):
            valid_moves.append((x, y - 2))

        return valid_moves

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum, auto

import pydantic

from pieces import FEN_MAP, Colour, PieceType

Position = tuple[int, int]
notation_map = {"a": 0, "b": 1, "c": 2, "d": 3, "e": 4, "f": 5, "g": 6, "h": 7}


class MoveCategory(StrEnum):
    REGULAR = auto()
    CAPTURE = auto()
    SHORT_CASTLE = auto()
    LONG_CASTLE = auto()


# @dataclass
class Move(pydantic.BaseModel):
    piece: PieceType
    dest: Position
    move_category: MoveCategory


# @staticmethod
def parse_move(player: Colour) -> Move:
    move = input()

    # self.validate_move(move)

    if move[1] == "x":
        move_category = MoveCategory.CAPTURE
    elif move == "0-0":
        return Move(
            PieceType.KING,
            (0, 6) if player == Colour.WHITE else (7, 6),
            MoveCategory.SHORT_CASTLE,
        )
    elif move == "0-0-0":
        return Move(
            PieceType.KING,
            (0, 2) if player == Colour.WHITE else (7, 2),
            MoveCategory.LONG_CASTLE,
        )
    else:
        move_category = MoveCategory.REGULAR

    if move[0].isupper():
        selected_piece_type = FEN_MAP[move[0].lower()]
    else:
        selected_piece_type = FEN_MAP["p"]

    dest = (int(move[-1]) - 1, notation_map[move[-2]])

    return Move(selected_piece_type, dest, move_category)

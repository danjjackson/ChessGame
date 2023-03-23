from enum import Enum, StrEnum, auto
from typing import Literal

notation_map = {"a": 0, "b": 1, "c": 2, "d": 3, "e": 4, "f": 5, "g": 6, "h": 7}

int_str_file_map = {0: "a", 1: "b", 2: "c", 3: "d", 4: "e", 5: "f", 6: "g", 7: "h"}
int_str_rank_map = {0: "1", 1: "2", 2: "3", 3: "4", 4: "5", 5: "6", 6: "7", 7: "8"}
str_int_file_map = {string: integer for integer, string in int_str_file_map.items()}
str_int_rank_map = {string: integer for integer, string in int_str_rank_map.items()}

position_map = {
    (str_file, str_rank): (int_file, int_rank)
    for int_file, str_file in int_str_file_map.items()
    for int_rank, str_rank in int_str_rank_map.items()
}


class MoveCategory(StrEnum):
    REGULAR = auto()
    CAPTURE = auto()
    SHORT_CASTLE = auto()
    LONG_CASTLE = auto()


class Colour(Enum):
    BLANK = -1
    WHITE = 0
    BLACK = 1


def other_colour(
    colour: Literal[Colour.WHITE, Colour.BLACK]
) -> Literal[Colour.WHITE, Colour.BLACK]:
    if colour == Colour.WHITE:
        return Colour.BLACK
    else:
        return Colour.WHITE

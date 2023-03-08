from __future__ import annotations

import pydantic

from chess.board import Board
from chess.exceptions import NotationError
from chess.pieces import FEN_MAP, PieceType
from chess.square import Square
from chess.utils import Colour, MoveCategory

notation_map = {"a": 0, "b": 1, "c": 2, "d": 3, "e": 4, "f": 5, "g": 6, "h": 7}


class Move(pydantic.BaseModel):
    piece_type: PieceType = PieceType.EMPTY
    dest: Square = Square()
    move_category: MoveCategory = MoveCategory.REGULAR
    src_file: str = "abcdefgh"
    src_rank: str = "12345678"
    promote_to: PieceType = PieceType.EMPTY

    @pydantic.validator("src_file")
    @classmethod
    def src_file_valid(cls, value: str) -> str:
        if value not in "abcdefgh":
            raise NotationError(message="invalid file")
        return value

    @pydantic.validator("src_rank")
    @classmethod
    def src_rank_valid(cls, value: str) -> str:
        if value not in "12345678":
            raise NotationError(message="invalid rank")
        return value

    def set_piece(self, piece_str: str) -> None:
        try:
            self.piece_type = FEN_MAP[piece_str.lower()]
        except KeyError:
            raise NotationError(message="That is not a valid symbol for a piece")

    class Config:
        validate_assignment = True


def parse_move(board: Board, player: Colour) -> list[Move]:
    move = input()

    if move == "0-0":
        return [
            Move(
                piece_type=PieceType.KING,
                dest=board.squares[("g", "1")]
                if player == Colour.WHITE
                else board.squares[("g", "8")],
                move_category=MoveCategory.SHORT_CASTLE,
            ),
            Move(
                piece_type=PieceType.ROOK,
                dest=board.squares[("f", "1")]
                if player == Colour.WHITE
                else board.squares[("f", "8")],
                move_category=MoveCategory.SHORT_CASTLE,
                src_file="h",
                src_rank="1" if player == Colour.WHITE else "8",
            ),
        ]
    if move == "0-0-0":
        return [
            Move(
                piece_type=PieceType.KING,
                dest=board.squares[("c", "1")]
                if player == Colour.WHITE
                else board.squares[("c", "8")],
                move_category=MoveCategory.SHORT_CASTLE,
            ),
            Move(
                piece_type=PieceType.ROOK,
                dest=board.squares[("d", "1")]
                if player == Colour.WHITE
                else board.squares[("d", "8")],
                move_category=MoveCategory.SHORT_CASTLE,
                src_file="a",
                src_rank="1" if player == Colour.WHITE else "8",
            ),
        ]
    if len(move) < 7:
        test_move = Move()
        x = move.find("x")
        if x == 1 or x == 2:
            test_move.move_category = MoveCategory.CAPTURE
        elif x == -1:
            test_move.move_category = MoveCategory.REGULAR
        else:
            raise NotationError(message="That is an invalid location for 'x'")

        if move[0].isupper():
            test_move.set_piece(move[0])
            if move[1].isnumeric():
                test_move.src_rank = move[1]
            elif (
                test_move.move_category == MoveCategory.REGULAR
                and not move[2].isnumeric()
            ):
                test_move.src_file = move[1]
            elif (
                test_move.move_category == MoveCategory.CAPTURE
                and not move[3].isnumeric()
            ):
                test_move.src_file = move[1]

        else:
            test_move.set_piece("p")
            if test_move.move_category == MoveCategory.CAPTURE:
                test_move.src_file = move[0]

        if "=" not in move:
            try:
                test_move.dest = board.get_square(move[-2], move[-1])
            except KeyError:
                raise NotationError(message="That square does not exist.")
        else:
            try:
                test_move.dest = board.get_square(move[-4], move[-3])
            except KeyError:
                raise NotationError(message="That square does not exist.")

            test_move.promote_to = FEN_MAP[move[-1]]
    else:
        raise NotationError(message="That is an invalid move!")

    return [test_move]

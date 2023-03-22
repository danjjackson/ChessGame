from __future__ import annotations

from typing import Protocol

import pydantic

from chess.exceptions import Checkmate, IllegalMoveError, NotationError
from chess.pieces import FEN_MAP, Piece, PieceType
from chess.players import Player
from chess.square import Square
from chess.utils import Colour, MoveCategory

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


class Board(Protocol):
    def get_square(self, file: int, rank: int) -> Square:
        """Returns the piece at position (x, y)."""
        return Square(file, rank)

    def king_is_in_check(self, colour: Colour) -> bool:
        return False

    def is_en_passant_legal(self, colour: Colour, destination: Square) -> bool:
        return True

    def check_for_checkmate(self, colour: Colour) -> bool:
        return False


class Move(pydantic.BaseModel):
    player: Player
    piece_type: PieceType = PieceType.EMPTY
    destination: Square = Square()
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

    def validate_move(self, board: Board) -> None:
        if self.destination.piece.colour == self.player.colour:
            raise IllegalMoveError(
                "That square is already occupied by one of your pieces!"
            )

        if self.move_category == MoveCategory.REGULAR:
            if not self.destination.is_empty:
                raise NotationError(
                    "There is an opponents piece on that square! Do you want to capture it?"
                )

        if self.move_category == MoveCategory.CAPTURE:
            if self.destination.is_empty:
                if self.piece_type != PieceType.PAWN or not board.is_en_passant_legal(
                    self.player.colour, self.destination
                ):
                    raise NotationError(
                        "You have specified a capture but there isn't a piece on the target square"
                    )

    def complete_move(
        self,
        board: Board,
        source: Square,
        destination: Square,
        move_category: MoveCategory,
    ) -> None:
        if (
            move_category == MoveCategory.SHORT_CASTLE
            or move_category == MoveCategory.LONG_CASTLE
        ):
            if board.king_is_in_check(self.player.colour):
                raise IllegalMoveError("You cannot castle out of check!")

        captured_piece = Piece()
        en_passant = False
        en_passanted_square = board.get_square(destination.file, source.rank)

        if move_category == MoveCategory.CAPTURE:
            if destination.is_empty:
                en_passant = True
                captured_piece = en_passanted_square.piece
                en_passanted_square.empty()
            else:
                captured_piece = destination.piece

            self.player.pieces_captured.append(captured_piece)

        source.move_piece(destination)
        # print(board.king_is_in_check(self.player.colour))
        # print(board.king_is_in_check(other_colour(self.player.colour)))

        if board.king_is_in_check(self.player.colour):
            destination.move_piece(source, undo=True)
            if move_category == MoveCategory.CAPTURE:
                if en_passant:
                    en_passanted_square.piece = captured_piece
                else:
                    destination.piece = captured_piece
                self.player.pieces_captured.pop()
            raise IllegalMoveError("Your king is in check!")

        if board.king_is_in_check(other_colour(self.player.colour)):
            if board.check_for_checkmate(other_colour(self.player.colour)):
                raise Checkmate("GAME OVER")


def parse_move(board: Board, player: Player) -> list[Move]:
    move = input()

    if move == "0-0":
        return [
            Move(
                player=player,
                piece_type=PieceType.KING,
                destination=board.get_square(*position_map[("g", "1")])
                if player.colour == Colour.WHITE
                else board.get_square(*position_map[("g", "8")]),
                move_category=MoveCategory.SHORT_CASTLE,
            ),
            Move(
                player=player,
                piece_type=PieceType.ROOK,
                destination=board.get_square(*position_map[("f", "1")])
                if player.colour == Colour.WHITE
                else board.get_square(*position_map[("f", "8")]),
                move_category=MoveCategory.SHORT_CASTLE,
                src_file="h",
                src_rank="1" if player == Colour.WHITE else "8",
            ),
        ]
    if move == "0-0-0":
        return [
            Move(
                player=player,
                piece_type=PieceType.KING,
                destination=board.get_square(*position_map[("c", "1")])
                if player.colour == Colour.WHITE
                else board.get_square(*position_map[("c", "8")]),
                move_category=MoveCategory.SHORT_CASTLE,
            ),
            Move(
                player=player,
                piece_type=PieceType.ROOK,
                destination=board.get_square(*position_map[("d", "1")])
                if player.colour == Colour.WHITE
                else board.get_square(*position_map[("d", "8")]),
                move_category=MoveCategory.SHORT_CASTLE,
                src_file="a",
                src_rank="1" if player == Colour.WHITE else "8",
            ),
        ]
    if len(move) < 7:
        test_move = Move(player=player)
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
            test_move.src_file = move[0]

        if "=" not in move:
            try:
                test_move.destination = board.get_square(
                    *position_map[(move[-2], move[-1])]
                )
            except KeyError:
                raise NotationError(message="That square does not exist.")
        else:
            try:
                test_move.destination = board.get_square(
                    *position_map[(move[-4], move[-3])]
                )
            except KeyError:
                raise NotationError(message="That square does not exist.")

            test_move.promote_to = FEN_MAP[move[-1]]
    else:
        raise NotationError(message="That is an invalid move!")

    return [test_move]


def other_colour(colour: Colour) -> Colour:
    if colour == Colour.WHITE:
        return Colour.BLACK
    else:
        return Colour.WHITE

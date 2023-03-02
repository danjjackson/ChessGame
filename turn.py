from board import Board
from move import Move, parse_move
from pieces import PieceType
from square import Square
from utils import Colour, MoveCategory

# from utils import get_moves, king_is_in_check


class IllegalMoveError(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(message)

    def __str__(self):
        return self.message


class Turn:
    def __init__(self, board: Board, player: Colour):
        self.player = player
        self.board = board

    def enter_move(self, player) -> list[Move]:
        return parse_move(self.board, player)

    def find_possible_source_squares(self, move: Move) -> list[Square]:
        possible_squares = self.board.find_squares(
            move.piece_type,
            self.player,
            move.src_file,
            move.src_rank,
        )
        if not len(possible_squares):
            raise IllegalMoveError(
                f"There is no {self.player} {move.piece_type} on the board!"
            )
        return possible_squares

    def find_valid_source_square(
        self, possible_squares: list[Square], move_category: MoveCategory, destination
    ) -> Square:
        valid_squares: list[Square] = [
            source
            for source in possible_squares
            if self.board.is_reachable(source, destination, move_category)
        ]

        if len(valid_squares) == 0:
            raise IllegalMoveError("Invalid move")
        elif len(valid_squares) > 1:
            raise ValueError("Ambiguous move")
        else:
            return valid_squares[0]

    def complete_move(
        self, source: Square, destination: Square, move_category: MoveCategory
    ):
        if (
            move_category == MoveCategory.SHORT_CASTLE
            or move_category == MoveCategory.LONG_CASTLE
        ):
            if self.board.king_is_in_check(self.player):
                raise IllegalMoveError("You cannot castle out of check!")

        source.move_piece(destination)

        if self.board.king_is_in_check(self.player):
            destination.move_piece(source, undo=True)
            raise IllegalMoveError("Your king is in check!")

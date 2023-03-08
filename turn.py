from board import Board
from exceptions import IllegalMoveError
from move import Move, parse_move
from square import Square
from utils import Colour, MoveCategory


class Turn:
    def __init__(self, board: Board, player: Colour) -> None:
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
        self,
        possible_squares: list[Square],
        move_category: MoveCategory,
        destination: Square,
    ) -> Square:
        valid_squares: list[Square] = []

        for source in possible_squares:
            if self.board.is_reachable(source, destination, move_category):
                valid_squares.append(source)

        if len(valid_squares) == 0:
            raise IllegalMoveError("That is not a legal move")
        elif len(valid_squares) > 1:
            raise IllegalMoveError(
                "There is more than one possible option for that move"
            )
        else:
            return valid_squares[0]

    def complete_move(
        self, source: Square, destination: Square, move_category: MoveCategory
    ) -> None:
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

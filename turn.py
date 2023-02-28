from typing import Tuple

from board import Board, Position
from move import Move, MoveCategory
from pieces import FEN_MAP, Colour, Piece, PieceType
from square import Square
from utils import get_moves, king_is_in_check


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

    def enter_move(self, player) -> Move:
        return Move.parse_move(self.board, player)

    def find_possible_squares(self, selected_piece_type: PieceType) -> list[Square]:
        possible_squares = self.board.find_pieces(selected_piece_type, self.player)
        if not len(possible_squares):
            raise IllegalMoveError(
                f"There is no {self.player} {selected_piece_type} on the board!"
            )
        return possible_squares

    def find_valid_square(
        self, possible_pieces: list[Square], move_category: MoveCategory, destination
    ) -> Square:
        valid_pieces: list[Square] = []

        for square in possible_pieces:
            valid_moves = get_moves(self.board, square.piece, move_category)

            if destination in valid_moves:
                valid_pieces.append(square)

        if len(valid_pieces) == 0:
            raise IllegalMoveError("Invalid move")
        elif len(valid_pieces) > 1:
            raise ValueError("Ambiguous move")
        else:
            return valid_pieces[0]

    def complete_move(
        self, source: Square, destination: Square, move_category: MoveCategory
    ):
        if (
            move_category == MoveCategory.SHORT_CASTLE
            or move_category == MoveCategory.LONG_CASTLE
        ):
            if king_is_in_check(self.board, self.player):
                raise IllegalMoveError("You cannot castle out of check!")

            if move_category == MoveCategory.SHORT_CASTLE:
                rook = self.board.piece(piece.x, piece.y + 3)
                rook.move_to(piece.x, piece.y + 1)
                self.board.place(rook)
                self.board.empty(piece.x, piece.y + 3)
                self.board.place(rook)

            else:
                rook = self.board.piece(piece.x, piece.y - 4)
                rook.move_to(piece.x, piece.y - 1)
                self.board.place(rook)
                self.board.empty(piece.x, piece.y - 4)

        source.move_piece(destination)

        # self.board.empty(piece.x, piece.y)
        # piece.move_to(*destination)
        # self.board.place(piece)

        if king_is_in_check(self.board, self.player):
            # self.board.empty(piece.x, piece.y)
            # piece.move_to(*source)
            # self.board.place(piece)
            destination.move_piece(source, undo=True)
            raise IllegalMoveError("Your king is in check!")

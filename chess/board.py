from __future__ import annotations

from dataclasses import dataclass, field
from typing import Literal

from chess.exceptions import AmbiguousMoveError, IllegalMoveError, OutOfBoundsError
from chess.move import int_str_file_map, int_str_rank_map, position_map
from chess.moves import (
    get_knight_squares,
    get_neighbour_function,
    is_long_castle_valid,
    is_short_castle_valid,
)
from chess.pieces import Piece, PieceType
from chess.square import Square
from chess.utils import Colour, MoveCategory, other_colour

Position = tuple[int, int]
Grid = dict[Position, Square]


def empty_board() -> Grid:
    grid: Grid = {}
    for file in range(8):
        for rank in range(8):
            grid[(file, rank)] = Square(file, rank)
    return grid


@dataclass
class Board:
    squares: Grid = field(default_factory=empty_board)

    @staticmethod
    def from_fen(fen: str) -> Board:
        board = Board()
        fenlist = fen.split("/")

        for ind_rank, rank in enumerate(fenlist):
            column = 0
            for char in rank:
                if char.isnumeric():
                    column += int(char)
                    continue
                board.place(column, ind_rank, Piece.from_fen(char))
                column += 1
            if column != 8:
                raise ValueError("Invalid FEN string")
            column = 0
        return board

    def get_square(self, file: int, rank: int) -> Square:
        try:
            square = self.squares[(file, rank)]
        except KeyError:
            raise OutOfBoundsError(
                f"The square {file}{rank} does not exist on the chess board"
            )
        return square

    def place(self, file: int, rank: int, piece: Piece) -> None:
        self.squares[(file, rank)].piece = piece

    def piece(self, file: int, rank: int) -> Piece:
        return self.squares[(file, rank)].piece

    def empty(self, file: int, rank: int) -> None:
        self.squares[(file, rank)] = Square(file, rank)

    def is_empty(self, file: int, rank: int) -> bool:
        return self.squares[(file, rank)].is_empty

    def find_king(self, colour: Colour) -> Square:
        return self.find_squares(PieceType.KING, colour)[0]

    def find_squares(
        self,
        piece_type: PieceType,
        colour: Colour,
        possible_file: str = "abcdefgh",
        possible_rank: str = "12345678",
    ) -> list[Square]:
        return [
            square
            for square in self.squares.values()
            if (
                square.piece.type == piece_type
                and square.piece.colour == colour
                and int_str_file_map[square.file] in possible_file
                and int_str_rank_map[square.rank] in possible_rank
            )
        ]

    def set_last_moved(self, destination: Square) -> None:
        for square in self.squares.values():
            if square == destination:
                square.piece.last_moved = True
            else:
                square.piece.last_moved = False

    def board_string(self, orientation: Colour) -> str:
        board_repr = ""

        if orientation == Colour.WHITE:
            for rank in "87654321":
                for file in "abcdefgh":
                    piece_str = self.squares[position_map[(file, rank)]].piece
                    board_repr = board_repr + f"| {str(piece_str)} "
                board_repr = board_repr + "|\n  _   _   _   _   _   _   _   _\n"
        else:
            for rank in "12345678":
                for file in "hgfedcba":
                    piece_str = self.squares[position_map[(file, rank)]].piece
                    board_repr = board_repr + f"| {str(piece_str)} "
                board_repr = board_repr + "|\n  _   _   _   _   _   _   _   _\n"
        return board_repr[:-1]

    def find_origin_squares(
        self,
        piece_type: PieceType,
        destination: Square,
        move_category: MoveCategory,
        colour: Literal[Colour.WHITE, Colour.BLACK],
    ) -> list[Square]:
        possible_origin_squares: list[Square] = []

        if move_category == MoveCategory.SHORT_CASTLE:
            if piece_type == PieceType.KING:
                king_square = self.find_king(colour)
                if is_short_castle_valid(self, king_square):
                    possible_origin_squares.append(king_square)
            elif piece_type == PieceType.ROOK:
                rook_square = self.get_square(destination.file + 2, destination.rank)
                possible_origin_squares.append(rook_square)
            return possible_origin_squares

        if move_category == MoveCategory.LONG_CASTLE:
            if piece_type == PieceType.KING:
                king_square = self.find_king(colour)
                if is_long_castle_valid(self, king_square):
                    possible_origin_squares.append(king_square)
            elif piece_type == PieceType.ROOK:
                rook_square = self.get_square(destination.file - 3, destination.rank)
                possible_origin_squares.append(rook_square)
            return possible_origin_squares

        if piece_type == PieceType.KNIGHT:
            knight_squares = get_knight_squares(self, destination)
            for square in knight_squares:
                if self.valid_move(square, piece_type, colour, move_category):
                    possible_origin_squares.append(square)
            return possible_origin_squares

        neighbour_funcs = get_neighbour_function(piece_type, colour, move_category)
        for neighbour_func in neighbour_funcs:
            source = destination
            move_distance = 1
            while True:
                try:
                    neighbour = neighbour_func(self, source)
                except OutOfBoundsError:
                    break
                if neighbour.piece.type == PieceType.EMPTY:
                    source = neighbour
                    move_distance += 1
                    continue
                elif self.valid_move(
                    neighbour,
                    piece_type,
                    colour,
                    move_category,
                    move_distance,
                ):
                    possible_origin_squares.append(neighbour)
                    break
                else:
                    break
        return possible_origin_squares

    def validate_origin_squares(
        self,
        squares: list[Square],
        origin_file: str = "abcdefgh",
        origin_rank: str = "12345678",
    ) -> Square:
        # If there's only one possible origin square, then just return that square
        if len(squares) == 1:
            return squares[0]

        # If there are multiple origin squares, check each one to see if it matches the
        # extra info given in the move class
        valid_squares: list[Square] = [
            x
            for x in squares
            if int_str_file_map[x.file] in origin_file
            and int_str_rank_map[x.rank] in origin_rank
        ]

        if not valid_squares:
            raise IllegalMoveError("That is not a valid move!")

        if len(valid_squares) > 1:
            print(origin_file)
            print(origin_rank)
            exit()
            raise AmbiguousMoveError(
                f"There is more than one possible move! The valid origin squares are {[str(square) for square in valid_squares]} Please clarify."
            )

        return valid_squares[0]

    def valid_move(
        self,
        possible_source: Square,
        target_piece_type: PieceType,
        target_colour: Colour,
        move_category: MoveCategory,
        move_distance: int = 0,
    ) -> bool:
        return (
            possible_source.piece.type == target_piece_type
            and possible_source.piece.colour == target_colour
            and possible_source.piece.move_limit[move_category] >= move_distance
        )

    def king_is_in_check(self, colour: Literal[Colour.WHITE, Colour.BLACK]) -> bool:
        king_square = self.find_king(colour)

        for piece_type in PieceType:
            if piece_type == PieceType.EMPTY:
                continue
            squares = self.find_origin_squares(
                piece_type, king_square, MoveCategory.CAPTURE, other_colour(colour)
            )
            try:
                self.validate_origin_squares(squares)
                return True
            except IllegalMoveError:
                continue
            except AmbiguousMoveError:
                return True

        return False

    def is_en_passant_legal(self, colour: Colour, destination: Square) -> bool:
        if int_str_rank_map[destination.rank] == "6" and colour == Colour.WHITE:
            square = self.get_square(destination.file, destination.rank - 1)
        elif int_str_rank_map[destination.rank] == "3" and colour == Colour.BLACK:
            square = self.get_square(destination.file, destination.rank + 1)
        else:
            return False

        if (
            square.piece.type == PieceType.PAWN
            and square.piece.moves_made == 1
            and square.piece.last_moved == True
        ):
            return True
        return False

    def check_for_checkmate(self, colour: Literal[Colour.WHITE, Colour.BLACK]) -> bool:
        checkmate = True
        for square in self.squares.values():
            for piece_type in PieceType:
                if piece_type != PieceType.EMPTY:
                    for move_category in [MoveCategory.REGULAR, MoveCategory.CAPTURE]:
                        squares = self.find_origin_squares(
                            piece_type, square, move_category, colour
                        )
                        try:
                            self.validate_origin_squares(squares)
                        except IllegalMoveError:
                            continue
                        if not self.king_is_in_check(colour):
                            checkmate = False

        return checkmate

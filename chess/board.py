from __future__ import annotations

from dataclasses import dataclass, field

from chess.exceptions import IllegalMoveError, NotationError, OutOfBoundsError
from chess.moves import MOVEMENT_MAP, is_short_castle_valid, is_valid_knight_move
from chess.pieces import Piece, PieceType
from chess.players import Player
from chess.square import Square
from chess.utils import Colour, MoveCategory

Position = tuple[int, int]
Grid = dict[Position, Square]

int_str_file_map = {0: "a", 1: "b", 2: "c", 3: "d", 4: "e", 5: "f", 6: "g", 7: "h"}
int_str_rank_map = {0: "1", 1: "2", 2: "3", 3: "4", 4: "5", 5: "6", 6: "7", 7: "8"}
str_int_file_map = {string: integer for integer, string in int_str_file_map.items()}
str_int_rank_map = {string: integer for integer, string in int_str_rank_map.items()}

position_map = {
    (str_file, str_rank): (int_file, int_rank)
    for int_file, str_file in int_str_file_map.items()
    for int_rank, str_rank in int_str_rank_map.items()
}


def empty_board() -> Grid:
    grid: Grid = {}
    for file in range(8):
        for rank in range(8):
            grid[(file, rank)] = Square(file, rank)
    return grid


@dataclass
class Board:
    orientation: Colour
    squares: Grid = field(default_factory=empty_board)

    @staticmethod
    def from_fen(
        fen: str = "rnbqk2r/pppppppp/8/8/8/8/PPPPPPPP/RNBQK2R",
        turn: Colour = Colour.WHITE,
    ) -> Board:
        board = Board(orientation=turn)
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

    def __str__(self) -> str:
        board_repr = ""
        if self.orientation == Colour.WHITE:
            for rank in "87654321":
                for file in "abcdefgh":
                    board_repr = (
                        board_repr
                        + f"| {str(self.squares[position_map[(file, rank)]].piece)} "
                    )
                board_repr = board_repr + "|\n  _   _   _   _   _   _   _   _\n"
        else:
            for rank in "12345678":
                for file in "hgfedcba":
                    board_repr = (
                        board_repr
                        + f"| {str(self.squares[position_map[(file, rank)]].piece)} "
                    )
                board_repr = board_repr + "|\n  _   _   _   _   _   _   _   _\n"
        return board_repr[:-1]

    def is_reachable(
        self,
        source: Square,
        destination: Square,
        move_category: MoveCategory,
    ) -> bool:
        if source.piece.type == PieceType.KNIGHT:
            return is_valid_knight_move(self, source, destination, move_category)

        if move_category == MoveCategory.SHORT_CASTLE:
            if source.piece.type == PieceType.KING:
                return is_short_castle_valid(self, source)
            elif source.piece.type == PieceType.ROOK:
                return True
            else:
                return False

        neighbour_funcs = MOVEMENT_MAP[source.piece.type][move_category]

        for neighbour_func in neighbour_funcs:
            for orientation in source.piece.orientation:
                temp = source
                move_distance = 0
                movement_limit = (
                    source.piece.move_limit
                    if move_category == MoveCategory.REGULAR
                    else source.piece.capture_limit
                )
                while move_distance < movement_limit:
                    move_distance += 1
                    try:
                        neighbour = neighbour_func(self, temp, orientation)
                    except OutOfBoundsError:
                        break
                    if neighbour == destination:
                        if neighbour.piece.colour == source.piece.colour:
                            raise IllegalMoveError(
                                "That square is already occupied by one of your pieces!"
                            )
                        if move_category == MoveCategory.REGULAR:
                            if neighbour.is_empty:
                                return True
                            else:
                                raise NotationError(
                                    "There is an opponents piece on that square! Do you want to capture it?"
                                )
                        if move_category == MoveCategory.CAPTURE:
                            if neighbour.is_empty:
                                if self.is_en_passant_legal(source, destination):
                                    return True
                                raise NotationError(
                                    "You have specified a capture but there isn't a piece on the target square"
                                )
                            else:
                                return True
                    elif neighbour.is_empty:
                        temp = neighbour
                        continue
                    else:
                        break

        return False

    def is_en_passant_legal(self, source: Square, destination: Square) -> bool:
        if source.piece.type == PieceType.PAWN:
            square = self.get_square(destination.file, source.rank)
            neighbour_piece = square.piece
            if (
                neighbour_piece.type == PieceType.PAWN
                and neighbour_piece.moves_made == 1
                and neighbour_piece.last_moved == True
            ):
                if source.piece.colour == Colour.WHITE and source.rank == "5":
                    return True
                elif source.piece.colour == Colour.BLACK and source.rank == "4":
                    return True
        return False

    def king_is_in_check(self, colour: Colour) -> bool:
        king_square = self.find_king(colour)

        is_in_check = False

        for square in self.squares.values():
            if square.piece.colour != colour and square.piece.type != PieceType.EMPTY:
                if self.is_reachable(square, king_square, MoveCategory.CAPTURE):
                    is_in_check = True

        return is_in_check


if __name__ == "__main__":
    board = Board.from_fen()
    # print(board)

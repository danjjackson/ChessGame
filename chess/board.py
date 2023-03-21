from __future__ import annotations

from dataclasses import dataclass, field

from chess.exceptions import (
    AmbiguousMoveError,
    IllegalMoveError,
    NotationError,
    OutOfBoundsError,
)
from chess.move import int_str_file_map, int_str_rank_map, position_map
from chess.moves import (
    MOVEMENT_MAP,
    get_knight_squares,
    is_long_castle_valid,
    is_short_castle_valid,
)
from chess.pieces import Piece, PieceType
from chess.square import Square
from chess.utils import Colour, MoveCategory

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

    def find_source_square(
        self,
        piece_type: PieceType,
        destination: Square,
        move_category: MoveCategory,
        colour: Colour,
        src_file: str = "abcdefgh",
        src_rank: str = "12345678",
    ) -> Square:
        possible_source_squares: list[Square] = []

        if move_category == MoveCategory.SHORT_CASTLE:
            if piece_type == PieceType.KING:
                king_square = self.find_king(colour)
                if is_short_castle_valid(self, king_square):
                    possible_source_squares.append(king_square)
            elif piece_type == PieceType.ROOK:
                rook_square = self.get_square(destination.file + 2, destination.rank)
                possible_source_squares.append(rook_square)

        elif move_category == MoveCategory.LONG_CASTLE:
            if piece_type == PieceType.KING:
                king_square = self.find_king(colour)
                if is_long_castle_valid(self, king_square):
                    possible_source_squares.append(king_square)
            elif piece_type == PieceType.ROOK:
                rook_square = self.get_square(destination.file - 3, destination.rank)
                possible_source_squares.append(rook_square)

        elif piece_type == PieceType.KNIGHT:
            knight_squares = get_knight_squares(self, destination)
            for square in knight_squares:
                if self.valid_move(square, colour, piece_type, src_file, src_rank):
                    possible_source_squares.append(square)

        else:
            move_funcs = MOVEMENT_MAP[piece_type][move_category]
            for orientation in [Colour.WHITE, Colour.BLACK]:
                for move_func in move_funcs:
                    source = destination
                    move_distance = 0
                    while move_distance < 7:
                        try:
                            neighbour = move_func(self, source, orientation)
                        except OutOfBoundsError:
                            break
                        if neighbour.piece.type == PieceType.EMPTY:
                            source = neighbour
                            move_distance += 1
                            continue
                        elif self.valid_move(
                            neighbour,
                            colour,
                            piece_type,
                            src_file,
                            src_rank,
                        ):
                            possible_source_squares.append(neighbour)
                            break
                        else:
                            break

        if not len(possible_source_squares):
            raise IllegalMoveError(
                f"{str(destination)} is not reachable by a {colour} {piece_type.value}"
            )
        elif len(possible_source_squares) > 1:
            raise AmbiguousMoveError(
                f"There is more than one possible move! Please clarify."
            )
        return possible_source_squares[0]

    def valid_move(
        self,
        destination: Square,
        colour: Colour,
        piece_type: PieceType,
        source_file: str,
        source_rank: str,
    ) -> bool:
        return (
            destination.piece.type == piece_type
            and destination.piece.colour == colour
            and int_str_file_map[destination.file] in source_file
            and int_str_rank_map[destination.rank] in source_rank
        )

    def is_reachable(
        self,
        source: Square,
        target_destination: Square,
        legal_squares: list[Square],
        move_category: MoveCategory,
    ) -> bool:
        for square in legal_squares:
            if square == target_destination:
                if square.piece.colour == source.piece.colour:
                    raise IllegalMoveError(
                        "That square is already occupied by one of your pieces!"
                    )

                if move_category == MoveCategory.REGULAR:
                    if square.is_empty:
                        return True
                    else:
                        raise NotationError(
                            "There is an opponents piece on that square! Do you want to capture it?"
                        )

                if move_category == MoveCategory.CAPTURE:
                    if square.is_empty:
                        if self.is_en_passant_legal(source, target_destination):
                            return True
                        raise NotationError(
                            "You have specified a capture but there isn't a piece on the target square"
                        )
                    else:
                        return True

            else:
                if not square.is_empty:
                    return False

        return False

    def king_is_in_check(self, colour: Colour) -> bool:
        king_square = self.find_king(colour)

        def other_colour(colour: Colour) -> Colour:
            if colour == Colour.WHITE:
                return Colour.BLACK
            else:
                return Colour.WHITE

        for piece_type in PieceType:
            if piece_type == PieceType.EMPTY:
                continue
            try:
                self.find_source_square(
                    piece_type, king_square, MoveCategory.CAPTURE, other_colour(colour)
                )
            except IllegalMoveError:
                return False
            except AmbiguousMoveError:
                return False

        return True

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


if __name__ == "__main__":
    board = Board.from_fen()
    # print(board)

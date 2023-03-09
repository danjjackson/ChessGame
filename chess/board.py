from __future__ import annotations

from dataclasses import dataclass, field

from chess.exceptions import IllegalMoveError, NotationError, OutOfBoundsError
from chess.moves import MOVEMENT_MAP, is_short_castle_valid, is_valid_knight_move
from chess.pieces import Piece, PieceType
from chess.square import Square
from chess.utils import Colour, MoveCategory

Position = tuple[str, str]
Grid = dict[Position, Square]

notation_map = {0: "a", 1: "b", 2: "c", 3: "d", 4: "e", 5: "f", 6: "g", 7: "h"}


def empty_board() -> Grid:
    grid: Grid = {}
    for file in "abcdefgh":
        for rank in "12345678":
            grid[(file, rank)] = Square(file, rank)
    return grid


@dataclass
class Board:
    squares: Grid = field(default_factory=empty_board)
    orientation: Colour = Colour.WHITE

    @staticmethod
    def from_fen(
        fen: str = "rnbqk2r/pppppppp/8/8/8/8/PPPPPPPP/RNBQK2R",
        turn: Colour = Colour.WHITE,
    ) -> Board:
        board = Board(orientation=turn)
        fenlist = fen.split("/")

        for ind_rank, rank in enumerate(fenlist):
            column = 0
            for ind_file, char in enumerate(rank):
                if char.isnumeric():
                    column += int(char) - 1
                    continue
                board.place(
                    notation_map[ind_file + column],
                    str(ind_rank + 1),
                    Piece.from_fen(char),
                )
            # if column + ind_file != 7:
            #     raise ValueError("Invalid FEN string")
            column = 0
        return board

    def get_square(self, file: str, rank: str) -> Square:
        try:
            square = self.squares[(file, rank)]
        except KeyError:
            raise OutOfBoundsError(
                f"The square {file}{rank} does not exist on the chess board"
            )
        return square

    def place(self, file: str, rank: str, piece: Piece) -> None:
        self.squares[(file, rank)].piece = piece

    def piece(self, file: str, rank: str) -> Piece:
        return self.squares[(file, rank)].piece

    def empty(self, file: str, rank: str) -> None:
        self.squares[(file, rank)] = Square(file, rank)

    def is_empty(self, file: str, rank: str) -> bool:
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
                and square.file in possible_file
                and square.rank in possible_rank
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
            board_repr = board_repr + "Player 2"
            for rank in "87654321":
                for file in "abcdefgh":
                    board_repr = (
                        board_repr + f"| {str(self.squares[(file, rank)].piece)} "
                    )
                board_repr = board_repr + "|\n  _   _   _   _   _   _   _   _\n"
            board_repr = board_repr + "Player 1"
        else:
            for rank in "12345678":
                for file in "hgfedcba":
                    board_repr = (
                        board_repr + f"| {str(self.squares[(file, rank)].piece)} "
                    )
                board_repr = board_repr + "|\n  _   _   _   _   _   _   _   _\n"

        return board_repr

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
            temp = source
            for orientation in source.piece.orientation:
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
    print(board)

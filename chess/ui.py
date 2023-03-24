from typing import Literal

from chess.board import Board
from chess.exceptions import NotationError, OutOfBoundsError
from chess.move import Move, MoveCategory
from chess.pieces import FEN_MAP, PieceType
from chess.players import Player
from chess.utils import Colour, position_map


class CLI:
    @staticmethod
    def make_player(colour: Literal[Colour.WHITE, Colour.BLACK]) -> Player:
        first_name = input("Enter your first name: ")
        last_name = input("Enter your last name: ")
        rating = int(input("Enter your rating: "))

        return Player(first_name, last_name, rating, colour)

    @staticmethod
    def parse_move(move: str, board: Board, player: Player) -> Move:
        if len(move) > 7:
            raise NotationError(message="That is an invalid move!")

        if move == "0-0":
            return Move(
                player=player,
                piece_type=PieceType.KING,
                destination=board.get_square(*position_map[("g", "1")])
                if player.colour == Colour.WHITE
                else board.get_square(*position_map[("g", "8")]),
                move_category=MoveCategory.SHORT_CASTLE,
                castle_rook_origin=board.get_square(*position_map[("h", "1")])
                if player.colour == Colour.WHITE
                else board.get_square(*position_map[("h", "8")]),
                castle_rook_destination=board.get_square(*position_map[("f", "1")])
                if player.colour == Colour.WHITE
                else board.get_square(*position_map[("f", "8")]),
            )
        if move == "0-0-0":
            return Move(
                player=player,
                piece_type=PieceType.KING,
                destination=board.get_square(*position_map[("c", "1")])
                if player.colour == Colour.WHITE
                else board.get_square(*position_map[("c", "8")]),
                move_category=MoveCategory.SHORT_CASTLE,
                castle_rook_origin=board.get_square(*position_map[("a", "1")])
                if player.colour == Colour.WHITE
                else board.get_square(*position_map[("a", "8")]),
                castle_rook_destination=board.get_square(*position_map[("d", "1")])
                if player.colour == Colour.WHITE
                else board.get_square(*position_map[("d", "8")]),
            )

        x = move.find("x")
        if x == 1 or x == 2:
            move_category = MoveCategory.CAPTURE
        elif x == -1:
            move_category = MoveCategory.REGULAR
        else:
            raise NotationError(message="That is an invalid location for 'x'")

        src_file = "abcdefgh"
        src_rank = "12345678"
        if move[0].isupper():
            try:
                piece_type = FEN_MAP[move[0].lower()]
            except KeyError:
                raise NotationError(message="That is not a valid symbol for a piece")
            if move[1].isnumeric():
                src_rank = move[1]
            elif move_category == MoveCategory.REGULAR and not move[2].isnumeric():
                src_file = move[1]
            elif move_category == MoveCategory.CAPTURE and not move[3].isnumeric():
                src_file = move[1]

        else:
            piece_type = PieceType.PAWN
            src_file = move[0]

        if "=" not in move:
            try:
                destination = board.get_square(*position_map[(move[-2], move[-1])])
            except OutOfBoundsError:
                raise NotationError(message="That is not a valid square.")
            return Move(
                player=player,
                piece_type=piece_type,
                destination=destination,
                move_category=move_category,
                src_file=src_file,
                src_rank=src_rank,
            )
        else:
            try:
                destination = board.get_square(*position_map[(move[-4], move[-3])])
            except OutOfBoundsError:
                raise NotationError(message="That is not a valid sqaure.")

            promote_to = FEN_MAP[move[-1]]

            return Move(
                player=player,
                piece_type=piece_type,
                destination=destination,
                move_category=move_category,
                src_file=src_file,
                src_rank=src_rank,
                promote_to=promote_to,
            )

    def move_prompt(self, colour):
        move = input(f"{colour} player: Please enter a move: ")
        return move

    def show_board(
        self,
        board: Board,
        white_player: Player,
        black_player: Player,
        orientation: Colour,
    ):
        print(black_player) if orientation == Colour.WHITE else print(white_player)
        print(board.board_string(orientation))
        print(white_player) if orientation == Colour.WHITE else print(black_player)

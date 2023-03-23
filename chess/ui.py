from typing import Literal

from chess.board import Board
from chess.exceptions import NotationError
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
    def parse_move(move: str, board: Board, player: Player) -> list[Move]:
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

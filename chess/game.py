from chess.board import Board
from chess.exceptions import Checkmate, IllegalMoveError, NotationError
from chess.pieces import Colour
from chess.players import Player
from chess.ui import CLI


def alternate_players(white_player, black_player, start: Colour = Colour.WHITE):
    if start == Colour.WHITE:
        while True:
            yield white_player
            yield black_player
    else:
        while True:
            yield black_player
            yield white_player


class ChessGame:
    def __init__(
        self, white_player: Player, black_player: Player, board: Board, ui: CLI
    ):
        self.white_player = white_player
        self.black_player = black_player
        self.ui = ui
        self.board = board

        self.player_alternator = alternate_players(
            self.white_player, self.black_player, Colour.WHITE
        )
        self.player = next(self.player_alternator)

    def play(self) -> None:
        game_over = False
        self.ui.show_board(
            self.board, self.white_player, self.black_player, self.player.colour
        )
        while not game_over:
            move = self.ui.move_prompt(self.player.colour)
            try:
                moves = self.ui.parse_move(move, self.board, self.player)
            except NotationError as e:
                print(e.message)
                continue
            for move in moves:
                try:
                    move.validate_move(self.board)
                except IllegalMoveError as e:
                    print(e.message)
                    break
                except NotationError as e:
                    print(e.message)
                    break

                try:
                    source_square = self.board.find_source_square(
                        move.piece_type,
                        move.destination,
                        move.move_category,
                        self.player.colour,
                        move.src_file,
                        move.src_rank,
                    )
                except IllegalMoveError as e:
                    print(e.message)
                    break
                try:
                    move.complete_move(
                        self.board, source_square, move.destination, move.move_category
                    )
                except IllegalMoveError as e:
                    print(e.message)
                    break
                except Checkmate as e:
                    print(e.message)
                    game_over = True
                    break
            else:
                self.board.set_last_moved(moves[0].destination)
                self.player = next(self.player_alternator)
                self.ui.show_board(
                    self.board, self.white_player, self.black_player, self.player.colour
                )

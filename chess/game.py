from chess.board import Board
from chess.exceptions import IllegalMoveError, NotationError
from chess.move import parse_move
from chess.pieces import Colour
from chess.players import Player


def alternate_players(white_player, black_player, start: Colour = Colour.WHITE):
    if start == Colour.WHITE:
        while True:
            yield white_player
            yield black_player
    else:
        while True:
            yield black_player
            yield white_player


class Game:
    def __init__(self, fen_string: str = "rnbqk2r/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR"):
        self.white_player = Player("Daniel", "Jackson", 2200, Colour.WHITE)
        self.black_player = Player("Caitlin", "Duschenes", 1100, Colour.BLACK)
        self.player_alternator = alternate_players(
            self.white_player, self.black_player, Colour.WHITE
        )
        self.player = next(self.player_alternator)
        self.board = Board.from_fen(fen_string, self.player.colour)

        self.play()

    def play(self) -> None:
        self.show_board()
        while True:
            print(f"{self.player.colour} player: Please enter a move!")
            try:
                moves = parse_move(self.board, self.player)
            except NotationError as e:
                print(e.message)
                continue
            for move in moves:
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

                self.board.set_last_moved(moves[0].destination)
                self.player = next(self.player_alternator)
                self.board.orientation = self.player.colour
                self.show_board()

    def show_board(self):
        print(self.black_player) if self.player.colour == Colour.WHITE else print(
            self.white_player
        )
        print(self.board)
        print(self.white_player) if self.player.colour == Colour.WHITE else print(
            self.black_player
        )

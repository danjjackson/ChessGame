from chess.board import Board
from chess.move import NotationError
from chess.pieces import Colour
from chess.players import Player
from chess.turn import IllegalMoveError, Turn


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
    def __init__(self, fen_string: str = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR"):
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
            turn = Turn(self.board, self.player)
            print(f"{turn.player.colour} player: Please enter a move!")
            try:
                moves = turn.enter_move(turn.player)
            except NotationError as e:
                print(e.message)
                continue
            for move in moves:
                try:
                    possible_squares = turn.find_possible_source_squares(move)
                except IllegalMoveError as e:
                    print(e.message)
                    break
                try:
                    source_square = turn.find_valid_source_square(
                        possible_squares, move.move_category, move.dest
                    )
                except IllegalMoveError as e:
                    print(e.message)
                    break
                except NotationError as e:
                    print(e.message)
                    break

                try:
                    captured_piece = turn.complete_move(
                        source_square, move.dest, move.move_category
                    )
                except IllegalMoveError as e:
                    print(e.message)
                    break

            else:
                if self.player == Colour.WHITE:
                    self.white_player.pieces_captured.append(captured_piece)
                else:
                    self.black_player.pieces_captured.append(captured_piece)

                self.board.set_last_moved(moves[0].dest)

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

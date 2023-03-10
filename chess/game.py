from chess.board import Board
from chess.move import NotationError
from chess.pieces import Colour
from chess.turn import IllegalMoveError, Turn


def alternate_players(start: Colour = Colour.WHITE):
    if start == Colour.WHITE:
        while True:
            yield Colour.WHITE
            yield Colour.BLACK
    else:
        while True:
            yield Colour.BLACK
            yield Colour.WHITE


class Game:
    def __init__(self, fen_string: str = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR"):
        self.colour_alternator = alternate_players(Colour.WHITE)
        self.player = next(self.colour_alternator)
        self.board = Board.from_fen(fen_string, self.player)

        self.play()

    def play(self) -> None:
        print(self.board)
        turn = Turn(self.board, self.player)
        while True:
            print(f"{turn.player} player: Please enter a move!")
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
                    turn.complete_move(source_square, move.dest, move.move_category)
                except IllegalMoveError as e:
                    print(e.message)
                    break

            else:
                self.board.set_last_moved(moves[0].dest)
                self.player = next(self.colour_alternator)

                self.board.orientation = self.player
                print(self.board)

                turn = Turn(self.board, self.player)

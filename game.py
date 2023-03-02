from board import Board
from move import NotationError
from pieces import Colour
from turn import IllegalMoveError, Turn


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

    def play(self):
        print(self.board)
        turn = Turn(self.board, self.player)
        while True:
            print(f"{turn.player} player: Please enter a move!")
            try:
                moves = turn.enter_move(turn.player)
            except NotationError as e:
                print(e.message)
                continue
            # print(move.move_category.value)
            for move in moves:
                try:
                    possible_squares = turn.find_possible_source_squares(move)
                except IllegalMoveError as e:
                    print(e.message)
                    break
                # print(possible_squares)
                try:
                    source_square = turn.find_valid_source_square(
                        possible_squares, move.move_category, move.dest
                    )
                    # print(source_square.piece)
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
                self.player = next(self.colour_alternator)

                self.board.orientation = self.player
                print(self.board)

                turn = Turn(self.board, self.player)


if __name__ == "__main__":
    game = Game()

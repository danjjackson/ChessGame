from board import Board
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
    def __init__(self, fen_string: str = "rnbqk2r/pppppppp/8/8/8/8/PPPPPPPP/RNBQK2R"):
        self.colour_alternator = alternate_players(Colour.WHITE)
        self.player = next(self.colour_alternator)
        self.board = Board.from_fen(fen_string, self.player)

        self.play()

    def play(self):
        print(self.board)
        turn = Turn(self.board, self.player)
        while True:
            print(f"{turn.player} player: Please enter a move!")
            move = turn.enter_move(turn.player)
            print(move.move_category.value)

            try:
                possible_pieces = turn.find_possible_pieces(move.piece)
            except IllegalMoveError:
                print("There are no pieces of that colour on the board")
                continue
            print(possible_pieces)
            try:
                selected_piece = turn.find_valid_piece(
                    possible_pieces, move.move_category, move.dest
                )
                print(selected_piece)
            except IllegalMoveError:
                print("Invalid move")
                continue

            try:
                turn.complete_move(selected_piece, move.dest, move.move_category)
            except IllegalMoveError:
                print("You cannot castle out of check!")
                continue

            self.player = next(self.colour_alternator)

            self.board.orientation = self.player
            print(self.board)

            turn = Turn(self.board, self.player)


if __name__ == "__main__":
    game = Game()

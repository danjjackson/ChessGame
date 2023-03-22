from chess.board import Board
from chess.game import ChessGame
from chess.players import Player
from chess.utils import Colour


def main() -> None:
    fen_str = "4K3/7q/4k3/8/8/8/8/8"
    white_player = Player.make_player(Colour.WHITE)
    black_player = Player.make_player(Colour.BLACK)
    board = Board.from_fen(fen_str)
    chess = ChessGame(white_player, black_player, board)
    chess.play()


if __name__ == "__main__":
    main()

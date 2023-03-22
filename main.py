from chess.game import ChessGame


def main() -> None:
    test = "4K3/7q/4k3/8/8/8/8/8"
    chess = ChessGame(test)
    chess.play()


if __name__ == "__main__":
    main()

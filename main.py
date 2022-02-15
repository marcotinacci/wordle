
if __name__ == "__main__":
    import logging
    import sys
    from pathlib import Path
    from wordle.game import Wordle
    from wordle.strategy.euristic import EuristicPlayer

    logging.basicConfig(stream=sys.stdout, level=logging.INFO)

    game = Wordle(None, Path(__file__).parent / "data/words_cfreshman.txt")
    player = EuristicPlayer(game)
    player.play()

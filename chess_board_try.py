import sys

import chess
from chess import engine


def play_move(board, move, chess_pc):

    board.push_uci(move)
    print(chess_pc.play(board, chess.engine.Limit(time=0.1)).move)
    print(list(board.legal_moves))
    return True, False


def main():
    board = chess.Board()
    chess_pc = chess.engine.SimpleEngine.popen_uci(r"C:\Users\dariu\Downloads\stockfish_15_win_x64_avx2\stockfish_15_win_x64_avx2\stockfish_15_x64_avx2.exe")
    while True:
        move = input('Give move')
        valid, winner = play_move(board, move, chess_pc)
        if valid:
            if winner:
                print(winner)
                break
        else:
            print('Non valid move')
        print(board)
    return 0


if __name__ == '__main__':
    sys.exit(main())

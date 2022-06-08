from kivy.app import App
from kivy.lang.builder import Builder
from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button


KV = """
FloatLayout:
    BoxLayout:
        id: chess_board
        orientation: "vertical"
"""

CHAR_DIC = {
    0: 'A',
    1: 'B',
    2: 'C',
    3: 'D',
    4: 'E',
    5: 'F',
    6: 'G',
    7: 'H'
}

START_POS = {
    'A_8': 'TowerBlack',
    'B_8': 'HorseBlack',
    'C_8': 'BishopBlack',
    'D_8': 'QueenBlack',
    'E_8': 'KingBlack',
    'H_8': 'TowerBlack',
    'G_8': 'HorseBlack',
    'F_8': 'BishopBlack',
    'A_7': 'PawnBlack',
    'B_7': 'PawnBlack',
    'C_7': 'PawnBlack',
    'D_7': 'PawnBlack',
    'E_7': 'PawnBlack',
    'H_7': 'PawnBlack',
    'G_7': 'PawnBlack',
    'F_7': 'PawnBlack',
    'A_1': 'Tower',
    'B_1': 'Horse',
    'C_1': 'Bishop',
    'D_1': 'Queen',
    'E_1': 'King',
    'H_1': 'Tower',
    'G_1': 'Horse',
    'F_1': 'Bishop',
    'A_2': 'Pawn',
    'B_2': 'Pawn',
    'C_2': 'Pawn',
    'D_2': 'Pawn',
    'E_2': 'Pawn',
    'H_2': 'Pawn',
    'G_2': 'Pawn',
    'F_2': 'Pawn',
}


class ChessApp(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.board = None

    def build(self):
        Window.size = [800, 800]
        return Builder.load_string(KV)

    def on_start(self):
        self.board = self.root.ids.chess_board
        for i in range(8):
            board_row = BoxLayout(orientation='horizontal')
            for j in range(8):
                row_num = 8 - i
                col_char = CHAR_DIC[j]
                square = Button(background_normal="", background_color=self.get_color(i, j))
                board_row.add_widget(square)
                self.root.ids['{}_{}'.format(col_char, row_num)] = square
            self.board.add_widget(board_row)
        self.reset_board()
        return

    def reset_board(self):
        for id in self.root.ids:
            if id != 'chess_board':
                square = self.root.ids[id]
                if id in START_POS:
                    col = square.background_color
                    if col == [1, 1, 1, 1]:
                        square.background_normal = "pictures\\{}.png".format(START_POS[id])
                    else:
                        square.background_color = [1, 1, 1, 1]
                        square.background_normal = "pictures\\{}BackBlack.png".format(START_POS[id])
        return

    def get_color(self, i, j):
        is_light_square = (i + j) % 2 != 0
        if is_light_square:
            return [1, 1, 1, 1]
        else:
            return [0, 0, 0, 1]


if __name__ == '__main__':
    app = ChessApp()
    app.run()
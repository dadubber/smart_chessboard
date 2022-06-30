import asyncio
import sys

import chess
from kivy.app import App
from kivy.lang.builder import Builder
from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
import numpy as np
from kivy.uix.togglebutton import ToggleButton
from bleak import BleakClient

KV = """
FloatLayout:
    BoxLayout:
        id: chess_board
        orientation: "vertical"
"""

ADDRESS = "D0:3A:1C:27:B8:7D"
WRITE_UUID = "6e400003-b5a3-f393-e0a9-e50e24dcca9e"

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

demo_dict = {
    0: 'A_1',
    1: 'B_1',
    2: 'A_2',
    3: 'B_2'
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


class Square(Button):
    def __init__(self, colour, **kwargs):
        self.colour = colour
        super().__init__(**kwargs)
        return


class ChessApp(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.board = None
        self.help = False
        self.memory_board = chess.Board()
        self.num_of_rows = 2
        self.board_positions = np.array([0, 0, 0, 0])

    def build(self):
        Window.size = [800, 800]
        return Builder.load_string(KV)

    def on_star1t(self):
        self.board = self.root.ids.chess_board
        for i in range(self.num_of_rows):
            board_row = BoxLayout(orientation='horizontal')
            for j in range(self.num_of_rows):
                row_num = 8 - i
                col_char = CHAR_DIC[j]
                color_code, color = self.get_color(i, j)
                square = Square(background_normal="", background_color=color_code, colour=color)
                board_row.add_widget(square)
                self.root.ids['{}_{}'.format(col_char, row_num)] = square
            self.board.add_widget(board_row)
        # self.reset_board()
        # Add button to turn help on
        help_button = ToggleButton(text='Turn on help')
        help_button.bind(on_press=self.turn_on_help)
        help_button.bind(on_release=self.turn_off_help)
        self.board.add_widget(help_button)
        # Add reset button
        reset_button = Button(text='Reset')
        reset_button.bind(on_press=self.reset_board)
        self.board.add_widget(reset_button)
        return

    def reset_board(self, _=None):
        for id in self.root.ids:
            if id != 'chess_board':
                square = self.root.ids[id]
                if id in START_POS:
                    if square.colour == 'White':
                        square.background_normal = "pictures\\{}.png".format(START_POS[id])
                    else:
                        square.background_color = [1, 1, 1, 1]
                        square.background_normal = "pictures\\{}BackBlack.png".format(START_POS[id])
                else:
                    square.background_normal = ""
                    if square.colour == 'Black':
                        square.background_color = [0, 0, 0, 1]
        return

    def on_start(self):
        self.board = self.root.ids.chess_board
        for i in range(self.num_of_rows):
            board_row = BoxLayout(orientation='horizontal')
            for j in range(self.num_of_rows):
                row_num = self.num_of_rows - i
                col_char = CHAR_DIC[j]
                color_code, color = self.get_color(i, j)
                square = Square(background_normal="", background_color=color_code, colour=color)
                board_row.add_widget(square)
                self.root.ids['{}_{}'.format(col_char, row_num)] = square
            self.board.add_widget(board_row)
        # Add button to turn help on
        help_button = ToggleButton(text='Turn on')
        help_button.bind(on_press=self.turn_on)
        help_button.bind(on_release=self.turn_off)
        self.board.add_widget(help_button)
        # Add reset button
        reset_button = Button(text='Reset')
        reset_button.bind(on_press=self.reset_board_demo)
        self.board.add_widget(reset_button)

    def reset_board_demo(self, _):
        for id in self.root.ids:
            if id != 'chess_board':
                square = self.root.ids[id]
                square.background_normal = ""
        return

    def turn_on(self, _):
        while True:
            loop = asyncio.get_event_loop()
            loop.run_until_complete(self.get_board_positions())

    def turn_off(self, _):
        sys.exit()

    def get_color(self, i, j):
        is_light_square = (i + j) % 2 != 0
        if is_light_square:
            return [1, 1, 1, 1], 'White'
        else:
            return [0, 0, 0, 1], 'Black'

    async def get_board_positions(self):
        async with BleakClient(ADDRESS) as client:
            model_number = await client.read_gatt_char(WRITE_UUID)
            board_positions = np.array([int(pos) for pos in model_number.decode('utf-8')])
            if np.array_equal(self.board_positions, board_positions):
                self.board_positions = board_positions
                self.update_board()

    def update_board(self):
        positves = [demo_dict[positive] for positive in np.where(self.board_positions == 1)]
        for id in self.root.ids:
            square = self.root.ids[id]
            if id in positves:
                if len(positves) == 1:
                    if square.colour == "White":
                        square.background_normal = "pictures\\Pawn.png"
                    else:
                        square.background_normal = "pictures\\PawnBackBlack.png"
                elif not square.background_normal:
                    if square.colour == "White":
                        square.background_normal = "pictures\\PawnBlack.png"
                    else:
                        square.background_normal = "pictures\\PawnBlackBackBlack.png"
            elif id != "chess_board":
                square.background_normal = ''


if __name__ == '__main__':
    app = ChessApp()
    app.run()

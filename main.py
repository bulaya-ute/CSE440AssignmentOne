import os

os.environ["KIVY_GL_BACKEND"] = "angle_sdl2"
from kivy.graphics import Color, Line
from kivymd.uix.card import MDCard

from kivymd.tools.hotreload.app import MDApp

from layout import BackgroundWidget, Subject, Dataset


def pair_exists(pairs: list[tuple], target_pair: tuple) -> bool:
    return any(set(pair) == set(target_pair) for pair in pairs)


class ChineseWallApp(MDApp):
    DEBUG = True
    AUTORELOADER_PATHS = [
        (".", {"recursive": False}),
    ]
    KV_FILES = ["layout.kv"]

    def __init__(self, **kwargs):
        super().__init__()
        self.background = None
        self.selected_cards = []
        self.lines = []
        self.all_cards = set()
        self.joins = []

    def build_app(self, first=False):
        self.background = BackgroundWidget()
        return self.background

    def deselect_all_cards(self):

        for card in self.all_cards:
            card.is_selected = False
        self.selected_cards.clear()

    def toggle_card_selection(self, card):
        self.all_cards.add(card)
        card.is_selected = not card.is_selected  # Highlight as selected

        if card in self.selected_cards:
            self.selected_cards.remove(card)
        else:
            self.selected_cards.append(card)

        print(len(self.selected_cards))

        if len(self.selected_cards) >= 2:
            print(type(self.selected_cards[0]), type(self.selected_cards[1]))
            if pair_exists(self.joins, (self.selected_cards[0], self.selected_cards[1])) or \
                    self.selected_cards[0].role == self.selected_cards[1].role:
                self.deselect_all_cards()
                return
            self.joins.append((self.selected_cards[0], self.selected_cards[1]))
            self.draw_line()

    def draw_line(self):
        card1, card2 = self.selected_cards
        with self.root.canvas:
            Color(0.0, 0.0, 0.0, 1)  # Grey color for the line
            line = Line(points=[
                card1.center_x, card1.center_y,
                card2.center_x, card2.center_y
            ], width=2)
            self.lines.append(line)
        self.deselect_all_cards()
        self.selected_cards.clear()

    def remove_line(self, line=None):
        if line:
            self.root.canvas.remove(line)
            self.line = None

    def clear_lines(self):
        for line in self.lines:
            self.root.canvas.remove(line)
        self.joins.clear()


if __name__ == "__main__":
    ChineseWallApp().run()

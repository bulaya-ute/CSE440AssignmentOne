import os
from typing import List, Tuple

from kivy.core.window import Window
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
        self.lines = []  # Store tuples of (line, card1, card2)
        self.all_cards = set()
        self.joins = []

    def build_app(self, first=False):
        self.background = BackgroundWidget()
        Window.bind(on_resize=self.update_lines)  # Bind the resize event
        return self.background

    def deselect_all_cards(self):

        for card in self.all_cards:
            card.is_selected = False
        self.selected_cards.clear()

    def toggle_card_selection(self, card, validate_access=True):
        self.all_cards.add(card)
        card.is_selected = not card.is_selected  # Highlight as selected

        if card in self.selected_cards:
            self.selected_cards.remove(card)
        else:
            self.selected_cards.append(card)

        if len(self.selected_cards) >= 2:
            if self.selected_cards[0].role == self.selected_cards[1].role:
                self.deselect_all_cards()
                return

            if self.selected_cards[1].role == "subject":
                self.selected_cards.reverse()

            if validate_access:
                read_access, read_access_description = self.validate_access(self.selected_cards[0], self.selected_cards[1])
                write_access, write_access_description = self.validate_write_access(self.selected_cards[0],
                                                                                self.selected_cards[1])
                self.update_info( read_access, read_access_description,
                                 write_access, write_access_description)

                if not read_access:
                    self.deselect_all_cards()
                    return

            if not pair_exists(self.joins, (self.selected_cards[0], self.selected_cards[1])):
                self.joins.append((self.selected_cards[0], self.selected_cards[1]))
                self.draw_line()

            self.deselect_all_cards()

    def draw_line(self, validate=False):
        card1, card2 = self.selected_cards
        with self.root.canvas:
            Color(0.0, 0.0, 0.0, 1)  # Grey color for the line
            line = Line(points=[
                card1.center_x, card1.center_y,
                card2.center_x, card2.center_y
            ], width=2)
            self.lines.append([line, card1, card2])
        self.deselect_all_cards()
        self.selected_cards.clear()

    def update_lines(self, *args):
        """Update line positions when window is resized."""
        for i, (line, card1, card2) in enumerate(self.lines):
            line.points = [
                card1.center_x, card1.center_y,
                card2.center_x, card2.center_y
            ]



    def remove_line(self, line=None):
        if line:
            self.root.canvas.remove(line)
            self.line = None

    def clear_lines(self):
        for line, card1, card2 in self.lines:
            self.root.canvas.remove(line)
        self.joins.clear()

    def update_info(self,
                    read_access: bool, read_access_desc: str,
                    write_access: bool, write_access_desc: str):

        read_access_label = self.background.ids.read_access_label
        write_access_label = self.background.ids.write_access_label

        print(f"- {read_access_desc}\n- {write_access_desc}\n")
        if read_access:
            read_access_label.text_color = "green"
        else:
            read_access_label.text_color = "red"
        read_access_label.text = read_access_desc

        if write_access:
            write_access_label.text_color = "green"
        else:
            write_access_label.text_color = "red"
        write_access_label.text = write_access_desc


    def get_accessed_datasets(self, subject: Subject):
        existing_pairs = [(subj, dataset) for subj, dataset in self.joins]
        return [dataset for subj, dataset in existing_pairs if subj == subject]

    def validate_access(self, subject, target_dataset: Dataset
    ) -> Tuple[bool, str]:
        existing_pairs = [(subj, dataset) for subj, dataset in self.joins]
        print(f"Existing pairs: {len(existing_pairs)}")

        # Find all datasets the subject already has access to
        accessed_datasets = self.get_accessed_datasets(subject)
        print(f"accessed datasets: {len(accessed_datasets)} - {[dataset.text for dataset in accessed_datasets]}")


        # Collect all COIs the subject has access to
        accessed_cois = {dataset.conflict_of_interest for dataset in accessed_datasets}

        # --- READ ACCESS CHECK ---
        if len(accessed_cois) == 0:
            return True, f"Read access granted: {subject.text} has no prior dataset access."

        if target_dataset.conflict_of_interest in accessed_cois:
            return False, f"Read access denied: {subject.text} already has access to this COI, and may leak information to a competitor"

        return True, "Read access granted: Access to an unrelated dataset may be performed"

    def validate_write_access(
            self,
            subject,
            target_dataset: Dataset
    ) -> Tuple[bool, str]:
        existing_pairs = [(subj.text, dataset) for subj, dataset in self.joins]
        accessed_datasets = self.get_accessed_datasets(subject)
        accessed_cois = {dataset.conflict_of_interest for dataset in accessed_datasets}

        read_access = self.validate_access(subject, target_dataset)[0]

        if not read_access:
            return False, f"Write access denied: {subject.text} does not currently have read access to {target_dataset.text}"

        if len(accessed_cois) > 1:
            for coi in accessed_cois:
                accessed_datasets_here = [dataset for dataset in accessed_datasets if dataset.conflict_of_interest == coi]
                if len(accessed_datasets_here) > 1:
                    return False, f"Write access denied. {subject.text} has previously accessed data from conflicting datasets"

        return True, f"Write access granted: {subject.text}'s access is confined to a single COI."


if __name__ == "__main__":
    ChineseWallApp().run()

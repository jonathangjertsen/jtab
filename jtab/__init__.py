from collections import namedtuple
from typing import List

TabGrid = namedtuple("TabGrid", "n_bars n_steps_per_bar")
TabNote = namedtuple("TabNote", "bar step string number")
RelativeNote = namedtuple("RelativeNote", "offset tab_note")
Tuning = namedtuple("Tuning", "name offsets")

CHAR_EMPTY = "-"
CHAR_PIPE = "|"
CHAR_NEWLINE = "\n"

class ParseError(Exception):
    pass

def get_empty_grid_string(tab_grid: TabGrid, tuning: Tuning) -> str:
    return CHAR_NEWLINE.join(
        (CHAR_PIPE + CHAR_EMPTY * tab_grid.n_steps_per_bar) * tab_grid.n_bars
        for _ in range(len(tuning.offsets) + 1)
    )

def get_tab_grid(line: str) -> TabGrid:
    n_bars = line.count(CHAR_PIPE)
    first_pipe_i = line.find(CHAR_PIPE)
    for i, char in enumerate(line[first_pipe_i+1:]):
        if char == CHAR_PIPE:
            n_steps_per_bar = i
            return TabGrid(n_bars, n_steps_per_bar)
    raise ParseError(line)


def get_notes(tab: str) -> List[TabNote]:
    tab = tab.strip()
    strings = [string.strip() for string in reversed(tab.split(CHAR_NEWLINE))]
    tab_grid = get_tab_grid(strings[0])
    notes = []
    for bar in range(tab_grid.n_bars):
        for step in range(1, tab_grid.n_steps_per_bar, 2):
            char_index = bar * (tab_grid.n_steps_per_bar + 1) + step
            for string_index, string in enumerate(strings):
                if string[char_index] != CHAR_EMPTY:
                    if string[char_index+1] == CHAR_EMPTY:
                        number = int(string[char_index])
                    else:
                        number = int(string[char_index] + string[char_index + 1])
                    notes.append(TabNote(bar=bar, step=step-1, number=number, string=string_index))
    return notes


def get_absolute_offsets(tuning: Tuning):
    offsets = [0]
    abs_offset = 0
    for offset in tuning.offsets:
        abs_offset += offset
        offsets.append(abs_offset)
    return offsets


def get_relative_note(tab_note: TabNote, tuning: Tuning):
    absolute_offsets = get_absolute_offsets(tuning)
    return RelativeNote(offset=absolute_offsets[tab_note.string] + tab_note.number, tab_note=tab_note)

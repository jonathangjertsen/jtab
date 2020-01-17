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

class NotGridlike(ParseError):
    pass

class InconsistentBarWidth(ParseError):
    pass

def get_standard_tuning() -> Tuning:
    return Tuning(name="E standard", offsets=[5, 5, 5, 4, 5])

def get_empty_grid_string(tab_grid: TabGrid, tuning: Tuning) -> str:
    return CHAR_NEWLINE.join(
        (CHAR_PIPE + CHAR_EMPTY * tab_grid.n_steps_per_bar) * tab_grid.n_bars
        for _ in range(len(tuning.offsets) + 1)
    )

def get_tab_grid(line: str) -> TabGrid:
    line = line.strip()

    if not line:
        raise NotGridlike("Empty line: {}".format(line))

    if line[0] != CHAR_PIPE:
        raise NotGridlike("Line does not start with a pipe: {}".format(line))

    if line[-1] == CHAR_PIPE:
        line = line[:-1]

    n_bars = line.count(CHAR_PIPE)
    for i, char in enumerate(line[1:]):
        if char == CHAR_PIPE:
            n_steps_per_bar = i
            candidate = TabGrid(n_bars, n_steps_per_bar)
            break
    else:
        raise NotGridlike("No pipes in {}".format(line))

    for i, char in enumerate(line):
        if i % (candidate.n_steps_per_bar + 1) == 0 and char != CHAR_PIPE:
            raise InconsistentBarWidth("Character at index {} is not a pipe in {}".format(i, line))

    return candidate


def get_notes(tab: str) -> List[TabNote]:
    tab = tab.strip()
    strings = [string.strip() for string in reversed(tab.split(CHAR_NEWLINE))]
    tab_grid = get_tab_grid(strings[0])
    notes = []
    for bar in range(tab_grid.n_bars):
        for step in range(1, tab_grid.n_steps_per_bar, 2):
            char_index = bar * (tab_grid.n_steps_per_bar + 1) + step
            for string_index, string in enumerate(strings):
                try:
                    number = int(string[char_index] + string[char_index + 1])
                except ValueError:
                    try:
                        number = int(string[char_index])
                    except ValueError:
                        number = None
                if number is not None:
                    note = TabNote(bar=bar, step=step-1, number=number, string=string_index)
                    notes.append(note)
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

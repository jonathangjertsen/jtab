import pytest

import jtab
from jtab import TabNote, RelativeNote

@pytest.fixture
def example():
    return """
|--------0-------|--------0-------|--------0-------|--------0-------
|------3---3-----|------3---3-----|------3---3-----|------3---3-----
|----4-------4---|----6-----------|----4-------4---|----6-----------
|--4-----------4-|--4-------------|--4-----------4-|--4-------------
|2---------------|2---------------|2---------------|2---------------
|----------------|------------2-5-|----------------|------------5-4-
"""

def test_get_empty_grid_string():
    assert jtab.get_empty_grid_string(jtab.TabGrid(n_bars=4, n_steps_per_bar=8), jtab.get_standard_tuning()) == """
|--------|--------|--------|--------
|--------|--------|--------|--------
|--------|--------|--------|--------
|--------|--------|--------|--------
|--------|--------|--------|--------
|--------|--------|--------|--------""".strip()

    assert jtab.get_empty_grid_string(jtab.TabGrid(n_bars=4, n_steps_per_bar=16), jtab.get_standard_tuning()) == """
|----------------|----------------|----------------|----------------
|----------------|----------------|----------------|----------------
|----------------|----------------|----------------|----------------
|----------------|----------------|----------------|----------------
|----------------|----------------|----------------|----------------
|----------------|----------------|----------------|----------------""".strip()

    assert jtab.get_empty_grid_string(jtab.TabGrid(n_bars=2, n_steps_per_bar=16), jtab.get_standard_tuning()) == """
|----------------|----------------
|----------------|----------------
|----------------|----------------
|----------------|----------------
|----------------|----------------
|----------------|----------------""".strip()

    assert jtab.get_empty_grid_string(jtab.TabGrid(n_bars=2, n_steps_per_bar=16), jtab.Tuning(name="dummy", root=40, offsets=[1, 2])) == """
|----------------|----------------
|----------------|----------------
|----------------|----------------""".strip()

def test_get_tab_grid_good():
    assert jtab.get_tab_grid("|------|------") == jtab.TabGrid(n_bars=2, n_steps_per_bar=6)
    assert jtab.get_tab_grid("|- - - |------") == jtab.TabGrid(n_bars=2, n_steps_per_bar=6)
    assert jtab.get_tab_grid("|- - - |------|") == jtab.TabGrid(n_bars=2, n_steps_per_bar=6)
    assert jtab.get_tab_grid("|abcd|defg|asdf") == jtab.TabGrid(n_bars=3, n_steps_per_bar=4)
    assert jtab.get_tab_grid("|abcd|defg|asdf|") == jtab.TabGrid(n_bars=3, n_steps_per_bar=4)

def test_get_tab_grid_inconsistent_width():
    with pytest.raises(jtab.InconsistentBarWidth):
        jtab.get_tab_grid("||-|--|---|")

def test_get_tab_grid_empty():
    with pytest.raises(jtab.NotGridlike):
        jtab.get_tab_grid("")

def test_get_tab_single_pipe():
    with pytest.raises(jtab.NotGridlike):
        jtab.get_tab_grid("|------")

def test_get_tab_grid_garbage():
    with pytest.raises(jtab.NotGridlike):
        jtab.get_tab_grid("asdf0candf18")

    with pytest.raises(jtab.NotGridlike):
        jtab.get_tab_grid("asdf0ca|ndf18")

def test_get_notes(example):
    tab_notes = jtab.get_notes(example)
    assert tab_notes == [
        TabNote(bar=0, step=0, string=1, number=2),
        TabNote(bar=0, step=2, string=2, number=4),
        TabNote(bar=0, step=4, string=3, number=4),
        TabNote(bar=0, step=6, string=4, number=3),
        TabNote(bar=0, step=8, string=5, number=0),
        TabNote(bar=0, step=10, string=4, number=3),
        TabNote(bar=0, step=12, string=3, number=4),
        TabNote(bar=0, step=14, string=2, number=4),
        TabNote(bar=1, step=0, string=1, number=2),
        TabNote(bar=1, step=2, string=2, number=4),
        TabNote(bar=1, step=4, string=3, number=6),
        TabNote(bar=1, step=6, string=4, number=3),
        TabNote(bar=1, step=8, string=5, number=0),
        TabNote(bar=1, step=10, string=4, number=3),
        TabNote(bar=1, step=12, string=0, number=2),
        TabNote(bar=1, step=14, string=0, number=5),
        TabNote(bar=2, step=0, string=1, number=2),
        TabNote(bar=2, step=2, string=2, number=4),
        TabNote(bar=2, step=4, string=3, number=4),
        TabNote(bar=2, step=6, string=4, number=3),
        TabNote(bar=2, step=8, string=5, number=0),
        TabNote(bar=2, step=10, string=4, number=3),
        TabNote(bar=2, step=12, string=3, number=4),
        TabNote(bar=2, step=14, string=2, number=4),
        TabNote(bar=3, step=0, string=1, number=2),
        TabNote(bar=3, step=2, string=2, number=4),
        TabNote(bar=3, step=4, string=3, number=6),
        TabNote(bar=3, step=6, string=4, number=3),
        TabNote(bar=3, step=8, string=5, number=0),
        TabNote(bar=3, step=10, string=4, number=3),
        TabNote(bar=3, step=12, string=0, number=5),
        TabNote(bar=3, step=14, string=0, number=4),
    ]

def test_get_absolute_offsets():
    assert jtab.get_absolute_offsets(jtab.get_standard_tuning()) == [0, 5, 10, 15, 19, 24]

def test_get_relative_note():
    tab_note = TabNote(bar=10, step=13, string=1, number=9)
    note = jtab.get_relative_note(tab_note, jtab.get_standard_tuning())
    assert note == jtab.RelativeNote(offset=14, tab_note=tab_note)

def test_get_relative_notes(example):
    relative_notes = jtab.get_relative_notes(jtab.get_notes(example), jtab.get_standard_tuning())

    assert relative_notes == [
         RelativeNote(offset=7, tab_note=TabNote(bar=0, step=0, string=1, number=2)),
         RelativeNote(offset=14, tab_note=TabNote(bar=0, step=2, string=2, number=4)),
         RelativeNote(offset=19, tab_note=TabNote(bar=0, step=4, string=3, number=4)),
         RelativeNote(offset=22, tab_note=TabNote(bar=0, step=6, string=4, number=3)),
         RelativeNote(offset=24, tab_note=TabNote(bar=0, step=8, string=5, number=0)),
         RelativeNote(offset=22, tab_note=TabNote(bar=0, step=10, string=4, number=3)),
         RelativeNote(offset=19, tab_note=TabNote(bar=0, step=12, string=3, number=4)),
         RelativeNote(offset=14, tab_note=TabNote(bar=0, step=14, string=2, number=4)),
         RelativeNote(offset=7, tab_note=TabNote(bar=1, step=0, string=1, number=2)),
         RelativeNote(offset=14, tab_note=TabNote(bar=1, step=2, string=2, number=4)),
         RelativeNote(offset=21, tab_note=TabNote(bar=1, step=4, string=3, number=6)),
         RelativeNote(offset=22, tab_note=TabNote(bar=1, step=6, string=4, number=3)),
         RelativeNote(offset=24, tab_note=TabNote(bar=1, step=8, string=5, number=0)),
         RelativeNote(offset=22, tab_note=TabNote(bar=1, step=10, string=4, number=3)),
         RelativeNote(offset=2, tab_note=TabNote(bar=1, step=12, string=0, number=2)),
         RelativeNote(offset=5, tab_note=TabNote(bar=1, step=14, string=0, number=5)),
         RelativeNote(offset=7, tab_note=TabNote(bar=2, step=0, string=1, number=2)),
         RelativeNote(offset=14, tab_note=TabNote(bar=2, step=2, string=2, number=4)),
         RelativeNote(offset=19, tab_note=TabNote(bar=2, step=4, string=3, number=4)),
         RelativeNote(offset=22, tab_note=TabNote(bar=2, step=6, string=4, number=3)),
         RelativeNote(offset=24, tab_note=TabNote(bar=2, step=8, string=5, number=0)),
         RelativeNote(offset=22, tab_note=TabNote(bar=2, step=10, string=4, number=3)),
         RelativeNote(offset=19, tab_note=TabNote(bar=2, step=12, string=3, number=4)),
         RelativeNote(offset=14, tab_note=TabNote(bar=2, step=14, string=2, number=4)),
         RelativeNote(offset=7, tab_note=TabNote(bar=3, step=0, string=1, number=2)),
         RelativeNote(offset=14, tab_note=TabNote(bar=3, step=2, string=2, number=4)),
         RelativeNote(offset=21, tab_note=TabNote(bar=3, step=4, string=3, number=6)),
         RelativeNote(offset=22, tab_note=TabNote(bar=3, step=6, string=4, number=3)),
         RelativeNote(offset=24, tab_note=TabNote(bar=3, step=8, string=5, number=0)),
         RelativeNote(offset=22, tab_note=TabNote(bar=3, step=10, string=4, number=3)),
         RelativeNote(offset=5, tab_note=TabNote(bar=3, step=12, string=0, number=5)),
         RelativeNote(offset=4, tab_note=TabNote(bar=3, step=14, string=0, number=4))
    ]

def test_get_midi():
    tab_note = TabNote(bar=10, step=14, string=1, number=9)
    note = jtab.get_relative_note(tab_note, jtab.get_standard_tuning())
    assert jtab.get_midi(note, jtab.get_standard_tuning()) == 54

def test_get_midis(example):
    relative_notes = jtab.get_relative_notes(jtab.get_notes(example), jtab.get_standard_tuning())
    midis = jtab.get_midis(relative_notes, jtab.get_standard_tuning())
    assert midis == [47, 54, 59, 62, 64, 62, 59, 54, 47, 54, 61, 62, 64, 62, 42, 45, 47, 54, 59, 62, 64, 62, 59, 54, 47, 54, 61, 62, 64, 62, 45, 44]

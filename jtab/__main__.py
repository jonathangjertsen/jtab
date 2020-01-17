from jtab import (
    get_empty_grid_string,
    get_notes,
    get_relative_note,
    get_standard_tuning,
    TabGrid,
)

if __name__ == "__main__":
    tuning = get_standard_tuning()
    example = """
    |--------0-------|--------0-------|--------0-------|--------0-------
    |------3---3-----|------3---3-----|------3---3-----|------3---3-----
    |----4-------4---|----6-----------|----4-------4---|----6-----------
    |--4-----------4-|--4-------------|--4-----------4-|--4-------------
    |2---------------|2---------------|2---------------|2---------------
    |----------------|------------2-5-|----------------|------------5-4-
    """

    print(get_empty_grid_string(TabGrid(n_bars=8, n_steps_per_bar=16), tuning=tuning))
    for tab_note in get_notes(example):
        print(get_relative_note(tab_note, tuning))

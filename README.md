# jtab
Python library for working with tabs

Status: exploratory

Motivation:

* Existing tab notation software is bloated and bad

Goals:

* Provide an intermediate representation
    * Import from text to IR should be flexible and tolerant, should do a relatively good job on existing material
    * Export should be predictable, entirely determined by config
* MIDI
    * Should make a decent guess when importing
    * Exporting should be perfect
    * Idempotent when importing what it has exported
* Simple text-based editor
* Minimal support for certain techniques (primaily slides) that can not adequately be described in text

Non-goals

* Musical notation
* Advanced editor features (WYSIWYG, playback, etc)
* Support for advanced techniques
* Hooks for plugins (at the moment)

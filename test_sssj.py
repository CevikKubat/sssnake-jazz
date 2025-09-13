# test_sssj.py
"""
Basic tests for sssj.py
Uses pytest + pytest-qt.
"""

import os
from pathlib import Path

import pytest
from PIL import Image
from sssj import KnobWithLabel, MainWindow


def test_knob_value(qtbot):
    """Knob should report the dial's current value."""
    knob = KnobWithLabel("Test", 0, 10, 5)
    qtbot.addWidget(knob)

    assert knob.value() == 5
    knob.dial.setValue(7)
    assert knob.value() == 7


def test_convert_to_audio(tmp_path: Path, qtbot):
    """
    Convert a tiny in-memory image to audio
    and ensure both .wav and .jpg are written.
    """
    win = MainWindow()
    qtbot.addWidget(win)

    # Provide a synthetic image and filename
    win.img = Image.new("RGB", (10, 10), color="red")
    win.file_name = "testimg"

    # Redirect output into an isolated temp directory
    outdir = tmp_path / "output"
    outdir.mkdir()
    cwd_before = Path.cwd()
    os.chdir(tmp_path)
    try:
        win.convert_to_audio()
    finally:
        os.chdir(cwd_before)

    wav = outdir / "testimg-sss.wav"
    jpg = outdir / "testimg-sss.jpg"

    assert wav.is_file()
    assert jpg.is_file()
    assert wav.stat().st_size > 0

"""Test Instrument class."""

import nose.tools

import sound_evolution as se

def test_create_empty():
    """Should create an empty instrument."""
    i = se.instrument.Instrument()
    assert(type(i) == se.instrument.Instrument)

def test_create_from_json():
    """Should create an instrument from JSON."""
    i = se.instrument.Instrument("{'root': {}}")

@nose.tools.raises(ValueError)
def test_create_from_json_fails():
    """Shouldn't create an instrument from invalid JSON."""
    i = se.instrument.Instrument("{'root': {}")

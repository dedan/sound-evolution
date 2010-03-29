"""Test Instrument class."""

import os
import nose.tools

import sound_evolution as se

def setup():
    global simple_json, invalid_json
    simple_json = open(
        os.path.join(os.path.dirname(__file__),
                     "fixtures", "simple_instrument.json")).read()
    invalid_json = open(
        os.path.join(os.path.dirname(__file__),
                     "fixtures", "invalid.json")).read()

def test_create_empty():
    """Should create an empty instrument."""
    i = se.instrument.Instrument()
    assert(type(i) == se.instrument.Instrument)

def test_create_from_json():
    """Should create an instrument from JSON."""
    global valid_json
    i = se.instrument.Instrument(simple_json)
    assert(type(i) == se.instrument.Instrument)

@nose.tools.raises(ValueError)
def test_create_from_json_fails():
    """Shouldn't create an instrument from invalid JSON."""
    global invalid_json
    i = se.instrument.Instrument(invalid_json)

def test_create_rand_instr():
    """Should create a random tree-instrument."""
    i = se.instrument.Instrument.random(0.7, 4)
    assert(type(i) == se.instrument.Instrument)
    assert i.instrument_tree != None
    
    

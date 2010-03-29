"""Test Instrument class."""

import os
import nose.tools

import sound_evolution as se

def setup():
    global simple_json, invalid_json, complex_json
    simple_json = open(
        os.path.join(os.path.dirname(__file__),
                     "fixtures", "simple_instrument.json")).read()
    invalid_json = open(
        os.path.join(os.path.dirname(__file__),
                     "fixtures", "invalid.json")).read()
    complex_json = open(
        os.path.join(os.path.dirname(__file__),
                     "fixtures", "complex_instrument.json")).read()


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
    assert(type(i)!=se.instrument.Instrument)
    
def test_create_to_json():
    """The JSON we create is in valid JSON format"""
    global simple_json
    i = se.instrument.Instrument(simple_json)
    assert ('{"root": {}}' == i.to_json())
    
def test_mutation():
    """The mutation produces something different from the original thing"""
    global simple_json
    i = se.instrument.Instrument(simple_json)
    n = i.mutate()
    assert (n.to_json != i_to_json)
    assert(type(n) == se.instrument.Instrument)
    
def test_ficken():
    """The crossover of two instruments creates a new instrument not equal to either of the originals"""
    global simple_json, complex_json
    i = se.instrument.Instrument(simple_json)
    j = se.instrument.Instrument(complex_json)
    k = i.ficken(j)
    assert k != i & k != j 
    assert(type(k) == se.instrument.Instrument)
    
    
    
    
    
        
    

"""Test Instrument class."""

import os
import nose.tools

import sound_evolution as se

def setUp():
    global empty_json, invalid_json, tone_json, tone_orc, complex_json, \
        render_err_json, render_err_orc
    empty_json = open(
        os.path.join(os.path.dirname(__file__),
                     "fixtures", "empty.json")).read()
    invalid_json = open(
        os.path.join(os.path.dirname(__file__),
                     "fixtures", "invalid.json")).read()
    tone_json = open(
        os.path.join(os.path.dirname(__file__),
                     "fixtures", "20kHz_tone.json")).read()
    tone_orc = open(
        os.path.join(os.path.dirname(__file__),
                  "fixtures", "20kHz_tone.orc")).read()
    render_err_json = open(
        os.path.join(os.path.dirname(__file__),
                  "fixtures", "render_error.json")).read()
    render_err_orc = open(
        os.path.join(os.path.dirname(__file__),
                  "fixtures", "render_error.orc")).read()
    complex_json = open(
      os.path.join(os.path.dirname(__file__),
                   "fixtures", "complex.json")).read()

def test_create_empty():
    """Should create an empty instrument."""
    i = se.instrument.Instrument()
    assert type(i) == se.instrument.Instrument

def test_create_from_json():
    """Should create an instrument from JSON."""
    global valid_json
    i = se.instrument.Instrument(empty_json)
    assert type(i) == se.instrument.Instrument

@nose.tools.raises(ValueError)
def test_create_from_json_fails():
    """Shouldn't create an instrument from invalid JSON."""
    global invalid_json
    i = se.instrument.Instrument(invalid_json)
    assert type(i) != se.instrument.Instrument

def test_create_rand_instr_default():
    """Should create a random instrument with default params."""
    i = se.instrument.Instrument.random()
    assert type(i) == se.instrument.Instrument
    assert i.instrument_tree != None

def test_create_rand_instr_params():
    """Should create a random instrument with params."""
    i = se.instrument.Instrument.random(
        const_prob=0.8, max_children=2)
    assert type(i) == se.instrument.Instrument
    assert i.instrument_tree != None

def test_create_to_json():
    """The JSON we create is in valid JSON format"""
    global empty_json
    i = se.instrument.Instrument(empty_json)
    assert '{"root": {}}' == i.to_json()

def test_mutation():
    """The mutation produces something different from the original thing"""
    global tone_json
    i = se.instrument.Instrument(tone_json)
    old_json = i.to_json()
    i.mutate()
    assert old_json != i.to_json

def test_ficken():
    """The crossover of two instruments creates a new instrument not equal to either of the originals"""
    global tone_json, complex_json
    i = se.instrument.Instrument(complex_json)
    j = se.instrument.Instrument(tone_json)
    j1 = se.instrument.Instrument(tone_json)
    j.ficken(i)
    assert j1.to_json() != j.to_json()
    assert i.to_json() != j.to_json()
    assert type(j) == se.instrument.Instrument
    assert type(i) == se.instrument.Instrument

def test_to_instr():
    """test if a simple instrument produces the valid csound code that we wrote by hand"""
    global tone_json, tone_orc
    i = se.instrument.Instrument(tone_json)
    assert i.to_instr() == tone_orc

def test_population():
    """Should create a Population object containing a list of instruments with length == size"""
    size = 3
    params = {"const_prob": 0.7, "max_children": 4}
    pop = se.genetics.Population(size, se.instrument.Instrument, params)
    assert type(pop) == se.genetics.Population
    assert type(pop.individuals[1]) == se.instrument.Instrument
    assert len(pop.individuals) == size

def test_next_generation():
    """The next generation should be member of class Population"""
    size = 3
    params = {"const_prob": 0.7, "max_children": 4}
    pop = se.genetics.Population(size, se.instrument.Instrument, params)
    pop_2 = pop.next_generation()
    assert type(pop_2) == se.genetics.Population

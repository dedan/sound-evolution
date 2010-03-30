"""Test Instrument class."""

import os
import nose.tools

import sound_evolution as se

def setup():
    global simple_json, invalid_json, complex_json, complex_orc
    simple_json = open(
        os.path.join(os.path.dirname(__file__),
                     "fixtures", "simple_instrument.json")).read()
    invalid_json = open(
        os.path.join(os.path.dirname(__file__),
                     "fixtures", "invalid.json")).read()
    complex_json = open(
        os.path.join(os.path.dirname(__file__),
                     "fixtures", "complex_instrument.json")).read()
    complex_orc = open(
        os.path.join(os.path.dirname(__file__),
                  "fixtures", "complex_instrument.orc")).read()


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

def test_create_rand_instr():
    """Should create a random tree-instrument."""
    params = {"const_prob": 0.7, "max_children": 4}
    i = se.instrument.Instrument.random(params)
    assert(type(i) == se.instrument.Instrument)
    assert i.instrument_tree != None

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
    assert(type(n) == se.instrument.Instrument)
    assert (n.to_json != i.to_json)

def test_ficken():
    """The crossover of two instruments creates a new instrument not equal to either of the originals"""
    global simple_json, complex_json
    i = se.instrument.Instrument(simple_json)
    j = se.instrument.Instrument(complex_json)
    k = i.ficken(j)
    assert (k != i and k != j)
    assert(type(k) == se.instrument.Instrument)
    

    

def test_to_instr():
    """docstring for test_to_instr"""
    global complex_json, complex_orc
    i = se.instrument.Instrument(complex_json)
    assert(i.to_instr() == complex_orc)

def test_population():
    """Should create a Population object containing a list of instruments with length == size"""
    size = 3
    params = {"const_prob": 0.7, "max_children": 4}
    pop = se.genetics.Population(size, se.instrument.Instrument, params)
    assert(type(pop) == se.genetics.Population)
    assert(type(pop.individuals[1]) == se.instrument.Instrument)
    assert(len(pop.individuals) == size)

def test_next_generation():
    """The next generation should be member of class Population"""
    size = 3
    params = {"const_prob": 0.7, "max_children": 4}
    pop = se.genetics.Population(size, se.instrument.Instrument, params)
    pop_2 = pop.next_generation()
    assert(type(pop_2) == se.genetics.Population)

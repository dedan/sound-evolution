"""test mutation functionality class"""

import sound_evolution as se
import random
import os


def setUp():
    global Mutate_Population, Ficken_Population, No_Iterations, Larger_Population
    Mutate_Population = se.genetics.Population(4, se.instrument.Instrument, {'const_prob':0.7, 'max_children':3})
    Ficken_Population = se.genetics.Population(0, se.instrument.Instrument, {'const_prob':0.7, 'max_children':3})
    Larger_Population = se.genetics.Population(10, se.instrument.Instrument, {'const_prob':0.7, 'max_children':3})
    tone_json = open(
        os.path.join(os.path.dirname(__file__),
                     "fixtures", "20kHz_tone.json")).read()
    complex_json = open(
      os.path.join(os.path.dirname(__file__),
                   "fixtures", "complex.json")).read()
    pa = se.instrument.Instrument(complex_json)
    ma = se.instrument.Instrument(tone_json)
    Ficken_Population.append_individual(pa)
    Ficken_Population.append_individual(ma)
    No_Iterations = 10

def test_one_breeding():
    """a population of size two should have size three after
        breeding 50 percent of them
    """
    P = Ficken_Population
    P.next_generation(0.0, 0.5)
    assert P.size == 3
    
def test_one_mutate():
    """test population size after mutation"""
    P = Ficken_Population
    P.next_generation(0.5, 0.0)
    print P.size
    assert P.size == 3
    
def test_selection_number_diff():
    """test natural selection n_surviving argument
    
        this is the test for the situation when all of the individuals
        have a different value for the fitness
    """
    P = Larger_Population
    for i in range(P.size):
        P.individuals[i].Fitness = i
    P.natural_selection(no_surviving=5)
    assert P.size == 5

def test_selection_number_same():
    """test natural selection n_surviving argument

        this is the test for the situation when more individuals have the same
        high score than we want to choose with no_surviving
    """
    P = Larger_Population
    for i in range(P.size):
        P.individuals[i].Fitness = 8
    P.natural_selection(no_surviving=5)
    assert P.size == 10

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
    pop_2 = pop.next_generation(1, 0.5)
    assert type(pop_2) == se.genetics.Population


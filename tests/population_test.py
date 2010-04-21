"""test mutation functionality class"""

import sound_evolution as se
import random
import os


def setUp():
    global Mutate_Population, Ficken_Population, No_Iterations
    Mutate_Population = se.genetics.Population(4, se.instrument.Instrument, {'const_prob':0.7, 'max_children':3})
    Ficken_Population = se.genetics.Population(0, se.instrument.Instrument, {'const_prob':0.7, 'max_children':3})
    tone_json = open(
        os.path.join(os.path.dirname(__file__),
                     "fixtures", "20kHz_tone.json")).read()
    complex_json = open(
      os.path.join(os.path.dirname(__file__),
                   "fixtures", "complex.json")).read()
    pa = se.instrument.Instrument(complex_json)
    ma = se.instrument.Instrument(tone_json)
    Ficken_Population.individuals.append(pa)
    Ficken_Population.individuals.append(ma)
    No_Iterations = 10

    
def test_mutate():
    """csound shouldn't crash after imposing numerous mutations"""
    errors = 0
    P = Mutate_Population
    for b in range(No_Iterations):
         for i in P.individuals:
             try:
                 csd = se.csound_adapter.CSD()
                 csd.orchestra(i)
                 csd.score('i 1 0 0')
                 csd.output_aif()
             except OSError:
                 print 'skipping this iteration:- Csound crashed'
                 errors += 1
         choice = random.choice(P.individuals)    
         choice.Fitness = 1
         P.natural_selection(no_surviving=1) 
         P.next_generation(1.0, 0.0)
         P.next_generation(1.0, 0.0)
         for i in P.individuals:
             i.Fitness = 0
    assert errors == 0

def test_one_breeding():
    """a population of size two should have size three after
        breeding 50 percent of them
    """
    P = Ficken_Population
    P.next_generation(0.0, 0.5)
    assert len(P.individuals) == 3

def test_ficken():
    """multiple fickens are sucessful"""
    errors = 0
    P = Ficken_Population
    P.next_generation(0.0, 0.5)
    for b in range(No_Iterations): 
        for i in P.individuals:
             try:
                 csd = se.csound_adapter.CSD()
                 csd.orchestra(i)
                 csd.score('i 1 0 0')
                 csd.play()
                 print i.to_instr()
             except OSError:
                 print 'skipping this iteration:- Csound crashed'
                 errors = errors + 1
        c = random.sample([0,1,2],2)
        try:   
            P.individuals[c[0]].Fitness = 1
            P.individuals[c[1]].Fitness = 1
        except IndexError:
            print 'no. of individuals isn\'t 3'
        P.natural_selection(no_surviving=2) 
        P.next_generation(0.0, 0.5)            
        for i in P.individuals:
            i.Fitness = 0
    assert errors == 0

         

    

"""test mutation functionality class"""

from instrument import *
from genetics import Individual 
from genetics import Population
import random



def setUp():
    pass 
    
def test_mutate():
    """csound shouldn't crash after imposing numerous mutations"""
    errors = 0
  
    P = Population(4, Instrument, {'const_prob':0.7, 'max_children':3})
    for b in range(100): 
         for i in P.individuals:
             try:
                 csd = csound_adapter.CSD()
                 csd.orchestra(i)
                 csd.score('i 1 0 2')
                 csd.play()
                 print i.to_json()
                 print i.to_instr()
             except OSError:
                 print 'skipping this iteration:- Csound crashed'
                 errors = errors + 1
         choice = random.randint(0,3)    
         P.individuals[choice].Fitness = 1
         P.natural_selection(no_surviving=1) 
         P.next_generation(1.0, 0.0)
         P.next_generation(1.0, 0.0)
         for i in P.individuals:
             i.Fitness = 0
    assert errors == 0
    
def test_ficken():
    """multiple fickens are sucessful"""
    errors = 0
  
    P = Population(3, Instrument, {'const_prob':0.7, 'max_children':3})
    for b in range(100): 
         for i in P.individuals:
             try:
                 csd = csound_adapter.CSD()
                 csd.orchestra(i)
                 csd.score('i 1 0 2')
                 csd.play()
                 print i.to_json()
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

    
             
test_ficken()         

    

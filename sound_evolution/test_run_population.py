from instrument import *
from genetics import Individual 
from genetics import Population


P = Population(4, Instrument, {'const_prob':0.7, 'max_children':3})

iterations = 0
while not raw_input('press return to continue or x to quit:-  '):
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
    n = int(raw_input('which did you like best: 1,2,3 or 4?:- '))-1    
    P.individuals[n].Fitness = 1
    P.natural_selection(no_surviving=1) 
    P.next_generation(1.0, 0.0)
    P.next_generation(1.0, 0.0)
    iterations = iterations+1
    for i in P.individuals:
        i.Fitness = 0
    print 'This is iteration number',iterations
    
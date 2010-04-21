from instrument import *
from genetics import Individual 
from genetics import Population




iterations = 0

a = int(raw_input('to try mutations press 1, to try ficken press 0:- '))

if a:
    P = Population(4, Instrument, {'const_prob':0.7, 'max_children':3})
    while not raw_input('press return to continue or x to quit mutate:-  '):
        for i in P.individuals:
            #try:
                csd = csound_adapter.CSD()
                csd.orchestra(i)
                csd.score('i 1 0 2')
                csd.play()
                print i.to_json()
                print i.to_instr()
         #   except OSError as (errno, strerror):
          #      print "O/S error({0}): {1}".format(errno, strerror)
           #     print 'skipping this iteration:- Csound crashed'
        n = int(raw_input('which did you like best: 1,2,3 or 4?:- '))-1    
        P.individuals[n].Fitness = 1
        P.natural_selection(no_surviving=1) 
        P.next_generation(1.0, 0.0)
        P.next_generation(1.0, 0.0)
        iterations = iterations+1
        for i in P.individuals:
            i.Fitness = 0
        print 'This is iteration number',iterations

else:
    P = Population(3, Instrument, {'const_prob':0.7, 'max_children':3})
    while not raw_input('press return to continue or x to quit ficken:-  '):
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
        n = int(raw_input('which did you like best: 1,2 or 3?:- '))-1   
        m = int(raw_input('which did you like 2nd best: 1,2 or 3?:- '))-1  
        print n, m, len(P.individuals)
        P.individuals[n].Fitness = 1
        P.individuals[m].Fitness = 1
        print "updated fitnesses"
        P.natural_selection(no_surviving=2) 
        print "kill"
        P.next_generation(0.0, 0.5)
        print "next gen"
        iterations = iterations+1
        print "updating iterations"
        for i in P.individuals:
            i.Fitness = 0
            print "assigning fitnesses"
        print 'This is iteration number',iterations,'length is',len(P.individuals)

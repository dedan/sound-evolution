from instrument import *
from genetics import Individual 
from genetics import Population
import os

IMAGE_VIEWER = "open"
graph_filename = "graph.jpg"
iterations = 0

a = int(raw_input('To run a population press 2, to try mutations press 1, to try ficken press 0:- '))


if a==0:
    P = Population(4, Instrument, {'const_prob':0.7, 'max_children':3})
    while not raw_input('press return to continue or x to quit ficken:-  '):
        for i in P.individuals:
            try:
                print i.to_instr()
                i.to_graph(graph_filename)
                os.system("%s %s" % (IMAGE_VIEWER, graph_filename))
                csd = csound_adapter.CSD()
                csd.orchestra(i)
                csd.score('i 1 0 2')
                csd.play()
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

elif a==1:
    P = Population(4, Instrument, {'const_prob':0.7, 'max_children':3})
    while not raw_input('press return to continue or x to quit mutate:-  '):
        for i in P.individuals:
            i.to_graph(graph_filename)
            os.system("%s %s" % (IMAGE_VIEWER, graph_filename))
            print i.to_instr()
            csd = csound_adapter.CSD()
            csd.orchestra(i)
            csd.score('i 1 0 2')
            csd.play()
        n = int(raw_input('which did you like best: 1,2,3 or 4?:- '))-1    
        P.individuals[n].Fitness = 1
        P.natural_selection(no_surviving=1) 
        P.next_generation(1.0, 0.0)
        P.next_generation(1.0, 0.0)
        iterations = iterations+1
        for i in P.individuals:
            i.Fitness = 0
        print 'This is iteration number',iterations

elif a==2: 
    P = Population(4, Instrument, {'const_prob':0.7, 'max_children':3})
    while not raw_input('press return to continue or x to quit Population run:-  '):
        for i in P.individuals:
            try:
                i.to_graph(graph_filename)
                os.system("%s %s" % (IMAGE_VIEWER, graph_filename))
                print i.to_instr()
                csd = csound_adapter.CSD()
                csd.orchestra(i)
                csd.score('i 1 0 5')
                csd.play()
            except OSError:
                print 'skipping this iteration:- Csound crashed'
        n = int(raw_input('which did you like best: 1,2,3 or 4?:- '))-1   
        m = int(raw_input('which did you like 2nd best: 1,2,3 or 4?:- '))-1
        P.individuals[n].Fitness = 1
        P.individuals[m].Fitness = 1
        a = P.individuals[n]
        c = P.individuals[m]
        
        print "updated fitnesses"
        P.natural_selection(no_surviving=2) 
        print "kill shitty 2" 
        try:
            d = a.ficken(c)
        except:
            d = a.mutate()
        P.append_individual(d)
        print "There is lovin' goin' on"
        print "There are now"+str((P.size))+" individuals"
        b = a.mutate()
        P.append_individual(b)
        print "The fittest has mutated"
        print "There are now" + str(P.size)+" individuals"
        iterations = iterations+1
        print "updating iterations"
        for i in P.individuals:
            i.Fitness = 0
            print "assigning fitnesses"
        print 'This is iteration number',iterations,'length is',len(P.individuals)

else:
    print "option unknown"
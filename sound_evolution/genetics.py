import abc
import random as rd

class Individual(object):
    """A class representing an individual."""
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def mutate(self):
        """Mutate an individual."""
        return 
        
    @abc.abstractmethod
    def ficken(self, individual=None):
        """Cross an individual with another one."""
        return 
        
    @abc.abstractmethod
    def fitness(self):
        """Score of the individual."""
        return 

    @abc.abstractmethod
    def random(params):
        """Generate a random individual."""
        return 

class Population(object):        

    def __init__(self, size, cls, params):
        self.size = size
        self.individual_cls = cls
        self.params = params
        self.individuals = [cls.random() for i in range(size)]
        
    def __kill(self, index):
        """kill index'th element off from the population"""
        del self.individuals[index] 

    def next_generation(self, frac_mutate, half_frac_breed):
        """Create the next generation from the current population.
        frac_mutate is less than 1 and half_frac_breed is <= 0.5"""
        mutations = rd.sample(self.individuals, int(self.size*frac_mutate))
        for i in mutations:
            x = i.mutate()
            self.individuals = self.individuals.append(x)
        breeders = rd.sample(self.individuals, 2*int(self.size*half_frac_breed))
        for i in range(len(breeders)-1):
            x = breeders[i].ficken(breeders[i+1])    #or something similar:- there are many mating schemes as we know living in the 21st century
            self.individuals = self.individuals.append(x)
               
    def find_fittest(self, no_fit):
        """find a collection of the fittest individuals of size equal to or more than no_fit"""
        ranked = self.individuals
        ranked.sort(cmp = lambda x,y: cmp(x.fitness(), y.fitness()), reverse=True)
        a = ranked[no_fit-1]
        lowest_fitness = a.fitness()
        chosen = []
        ratings = [x.fitness() for x in ranked]
        for i in self.individuals:
            if i.Fitness >= lowest_fitness:
                chosen.append(i)
            else:
                pass
        return chosen
        
                
    def natural_selection(self, no_surviving=None, percentage=None):
        """filter out the least fit individuals in the population - percentage optional argument between 0 and 100; no_surviving optional 
            argument denoting desired no_ of surviving individuals"""
        if no_surviving:
            self.individuals = self.find_fittest(no_surviving)
        if percentage:
            number = int(((100 -percentage)/100.0)*len(self.individuals))
            self.individuals = self.find_fittest(number)
        else:
            pass
        
        
     
        
        
        
        
        
        
        
    
        
        
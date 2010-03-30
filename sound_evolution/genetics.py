import abc

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
            self.individuals = [cls.random(params) for i in range(size)]

    def next_generation(self):
            """Create the next generation from current population."""
            pass

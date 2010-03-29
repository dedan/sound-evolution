"""A single csound instrument."""

import os
import abc
import simplejson as json
import random
from collections import deque
from genetics import Individual

class Instrument(object):
    """A class representing the genome tree."""
    
    def __init__(self, instrument_tree=None):
        """ Create a new Instrument from a json string """
        if type(instrument_tree) is str:
            self.instrument_tree = json.loads(instrument_tree)
        else:
            self.instrument_tree = instrument_tree

    
    def to_ocr(self):
        """Generate csound ocr code."""
        csound_code = ""
        data = []
        for child in n.children:
            (code, data) = child.to_csound
            csound_code += code
            data += data
        return n.render(data)
        
    def to_json(self):
        """Serialize instrument to JSON."""
        return json.dumps(self.instrument_tree)

    def mutate(self):
        """Mutate an instrument."""
        return

    def ficken(self, individual=None):
		"""Cross a tree-instrument with another one."""
		return

    def fitness(self):
        """Score of the instrument."""
        return
            
    @staticmethod
    def random(params):
        """create a random instrument"""

        const_probability = params.get("const_prob")
        max_children = params.get("max_children")	    
    
        def get_only_type(the_type, opcodes):
        	"""get only opcodes the have output of the_type"""
        	return [op for op in opcodes if op["outtype"] == the_type]
        
        
        # get list of available opcodes from json file_
        opcodes = json.loads(file(os.path.join(os.path.dirname(__file__), "opcodes.json")).read())

        # select random root element 
        # TODO maybe this has to be constrained to outtype="a" type
        root = Instrument.__make_node(random.choice(opcodes))
        todo = deque([root])
        
        # TODO this number has to be replaced by the may value of the opcode with 
        # which it is used
        max_rand_const = 100

        while todo:
            tmp_tree = todo.popleft()

            # if it is a math operator
            if tmp_tree["code"]["type"] == "math":
                
                n_children = random.randint(2, max_children)
                for i in range(n_children):
                    if random.random() > const_probability:
                        random_node = Instrument.__make_node(random.choice(opcodes))
                        todo.append(random_node)
                    else:
                        const_code = {"name": "const", "value": random.random() * max_rand_const}
                        random_node = Instrument.__make_node(const_code)

                    tmp_tree["children"].append(random_node)
                    
            else:
                for param in tmp_tree["code"]["params"]:
                    if random.random() > const_probability:
                        filtered = get_only_type(param["type"], opcodes)
                        random_node = Instrument.__make_node(random.choice(opcodes))
                        todo.append(random_node)
                    else:
                        const_code = {"name": "const", "value": random.random() * max_rand_const}
                        random_node = Instrument.__make_node(const_code)

                    tmp_tree["children"].append(random_node)
        
        inst = Instrument()
        inst.instrument_tree = root
        return inst
                
    @staticmethod        
    def __make_node(code):
        """Make a node with no children."""
        return { "code": code, "children": []}    

   
Individual.register(Instrument)
      
if __name__ == '__main__':
    i = Instrument.random(0.7, 4)
    print i.to_json()

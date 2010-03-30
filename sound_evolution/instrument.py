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
        """ Create a new Instrument from a json string or from a tree of python objects """
        if type(instrument_tree) is str:
            self.instrument_tree = json.loads(instrument_tree)
        else:
            self.instrument_tree = instrument_tree


    def to_instr(self):
        """Generate csound ocr code."""
        n = 0
        (code, data, n) = self.__class__.__to_instr(self.instrument_tree, n, "a")
        return code + "out\ta%d" % (n-1)


    @staticmethod
    def __to_instr(node, n, out_type):
        csound_code = ""
        data = []
        for i, child in enumerate(node["children"]):
            if node["code"]["type"] == "math":
                inttype = "k"
            else:
                inttype = node["code"]["params"][i]["type"]
            (code, d, n) = Instrument.__to_instr(child, n, inttype)
            csound_code += code
            data += (d,)
        (c, d, n) = Instrument.__render(node, data, n, out_type)
        return (csound_code + c, d, n)


    @staticmethod
    def __render(node, data, n, out_type):
        """render the code for a node"""
        
        if out_type == "x":
            out_type = random.choice(["a", "k"])
            
        code = ""
        var = "%s%d" % (out_type, n)
        if node["code"]["type"] == "code":
            code = "%s\t%s\t%s" % (var, node["code"]["symbol"], ", ".join(data))
        elif node["code"]["type"] == "math":
            code = "%s\t=\t%s" % (var, node["code"]["symbol"].join(data))
        elif node["code"]["type"] == "const":
            val = str(node["code"]["value"])
            return ("", val, n)
        return (code +"\n", var, n+1)


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
            if the_type == "x":
                types = ["a", "k"]
            else:
                types = [the_type]
            return [op for op in opcodes if op["outtype"] in types]


        # get list of available opcodes from json file_
        opcodes = json.loads(file(os.path.join(os.path.dirname(__file__), "opcodes.json")).read())

        # select random root element
        only_a_type = get_only_type("a", opcodes)
        root = Instrument.__make_node(random.choice(only_a_type))
        todo = deque([root])

        # TODO this number has to be replaced by the max value of the opcode with
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
                        const_code = Instrument.__make_const_code(random.random() * max_rand_const)
                        random_node = Instrument.__make_node(const_code)

                    tmp_tree["children"].append(random_node)

            else:
                for param in tmp_tree["code"]["params"]:
                    
                    # if param type is t alwys plug in a constant
                    if param["type"] == "t":
                        if param["max"] == param["min"]:
                            random_const = param["max"]
                        else:
                            random_const = random.randrange(param["min"], param["max"], 1)
                        const_code = Instrument.__make_const_code(random_const)
                        random_node = Instrument.__make_node(const_code)

                    # if it is below constant probability also plug in constant
                    elif random.random() < const_probability:
                        # choose random constant according to input range and type
                        random_const = (random.random() * (param["max"]-param["min"])) + param["min"]
                        const_code = Instrument.__make_const_code(random_const)
                        random_node = Instrument.__make_node(const_code)

                    # when above the constant probability plug in another opcode
                    else:
                        filtered = get_only_type(param["type"], opcodes)
                        random_node = Instrument.__make_node(random.choice(opcodes))
                        todo.append(random_node)

                    tmp_tree["children"].append(random_node)

        inst = Instrument()
        inst.instrument_tree = root
        return inst

    @staticmethod
    def __make_node(code):
        """Make a node with no children."""
        return { "code": code, "children": []}

    @staticmethod
    def __make_const_code(val):
        """make a new constant"""
        return {"name": "const", "type": "const", "value": str(val)}

    def mutate(self):
        """Mutate an instrument."""
        return

    def ficken(self, individual=None):
        """Cross a tree-instrument with another one."""
        return

    def fitness(self):
        """Score of the instrument."""
        return

Individual.register(Instrument)


if __name__ == '__main__':
    comp = open("../tests/fixtures/complex_instrument.json").read()
    i = Instrument(comp)
    # random_params = {"const_prob": 0.7, "max_children": 5}
    # i = Instrument.random(random_params)
    print i.to_instr()
#    print i.to_json()

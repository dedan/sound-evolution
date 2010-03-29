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

    def to_instr(self):
        """Generate csound ocr code."""
        n = 0
        (c, d, n) = self.__class__.__to_instr(self.instrument_tree, n)
        return c + "\n" + "out\ta%d" % n

    @staticmethod
    def __to_instr(node, n):
        csound_code = ""
        data = []
        tmp_n = n
        for child in node["children"]:
            (code, d, n) = Instrument.__to_instr(child, tmp_n)
            csound_code += code
            data += (d,)
            tmp_n += n
        (c, d, n) = Instrument.__render(node, data, tmp_n)
        return (csound_code + "\n" + c, d, n)

    @staticmethod
    def __render(node, data, n):
        """render the code for a node"""
        code = ""
        var = "a%d" % n
        if node["code"]["type"] == "code":
            code = "a%d\t%s\t%s" % (n, node["code"]["symbol"], ", ".join(data))
        elif node["code"]["type"] == "math":
            code = "a%d\t=\t%s" % (n, node["code"]["symbol"].join(data))
        elif node["code"]["type"] == "const":
            val = str(node["code"]["value"])
            return ("", val, n)
        return (code, "a%d" % n, n+1)

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
                        const_code = Instrument.__make_const_code(random.random() * max_rand_const)
                        random_node = Instrument.__make_node(const_code)

                    tmp_tree["children"].append(random_node)

            else:
                for param in tmp_tree["code"]["params"]:
                    if random.random() > const_probability:
                        filtered = get_only_type(param["type"], opcodes)
                        random_node = Instrument.__make_node(random.choice(opcodes))
                        todo.append(random_node)
                    else:
                        const_code = Instrument.__make_const_code(random.random() * max_rand_const)
                        random_node = Instrument.__make_node(const_code)

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
    print i.to_instr()
    print i.to_json()

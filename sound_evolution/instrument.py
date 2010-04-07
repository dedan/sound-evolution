"""A single csound instrument."""

import os, abc, random, copy
import simplejson as json
from collections import deque
import csound_adapter
from gvgen import *
from genetics import Individual

class Instrument(object):
    """A class representing the genome tree."""

    __CONST_PROB = 0.7
    __MAX_CHILDREN = 4
    __OPCODES_FILE = "opcodes_extended.json"
    __MAX_FICKEN = 10

    def __init__(self, instrument_tree=None):
        """Create a new Instrument
        
        The new Instrument can be created from a json string 
        or from a tree of python objects (e.g. instrument_tree of another
        instrument)
        
        """
        if type(instrument_tree) is str:
            self.instrument_tree = json.loads(instrument_tree)
        else:
            self.instrument_tree = instrument_tree

    def __eq__(self, other):
        """equality comparison of two instruments
        
        comparison is done by comparing the json representation of 
        two instrument objects
        
        """
        if isinstance(other, Instrument):
            return self.to_json() == other.to_json()
        return NotImplemented
        
    def __ne__(self, other):
        """not equal comparison of two instruments
        
        uses the eq operator and therefore also the json representation of
        an instrument for comparison
        
        """
        r = self.__eq__(other)
        if r is NotImplemented:
            return r
        return not r

    def to_instr(self):
        """Generate csound ocr code."""
        n = 0
        (code, data, n) = Instrument.__to_instr(self.instrument_tree, n, "a")
        return code \
            + "a%d\tclip\ta%d, 0, 1\n" % (n, n-1) \
            + "out\ta%d" % n

    @staticmethod
    def __to_instr(node, n, out_type):

        csound_code = ""
        data = []
        for i, child in enumerate(node["children"]):
            intype = child["code"]["outtype"]
            (code, d, n) = Instrument.__to_instr(child, n, intype)
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

    def to_graph(self, filename='graph.jpg'):
        """Generates a jpg-file displaying the instrument tree."""

        self.graph_filename = filename

        if self.graph_filename.endswith('.jpg'):
            dot_filename = self.graph_filename[:-4] + '.dot'
            jpg_filename = self.graph_filename
        else:
            dot_filename = self.graph_filename + '.dot'
            jpg_filename = self.graph_filename + '.jpg'

        graph = GvGen()
        graph.styleDefaultAppend("color","red")
        graph.styleDefaultAppend("style", "filled")
        graph.styleDefaultAppend("fontcolor", "white")

        stack = []
        new_parents = []
        stack.append(self.instrument_tree)

        root = True
        while (len(stack) > 0):
            if root:
                sub_tree = stack.pop()
                node = graph.newItem(sub_tree["code"]["symbol"])
                root = False
            else:
                sub_tree = stack.pop()
                node = new_parents.pop()

            if len(sub_tree["children"]) > 0:
                for i, child in enumerate(sub_tree["children"]):

                    if child["code"]["name"] == "const":
                        const_value = round(float(child["code"]["value"]), 2)
                        child_node = graph.newItem(const_value)
                        graph.styleAppend("const", "shape", "rectangle")
                        graph.styleAppend("const", "color", "black")
                        graph.styleAppend("const", "style", "filled")
                        graph.styleApply("const", child_node)

                    else:
                        child_node = graph.newItem(child["code"]["symbol"])
                        stack.append(child)
                        new_parents.append(child_node)

                    curr_link = graph.newLink(node, child_node)


                    if sub_tree["code"]["type"] == "code":
                        graph.propertyAppend(curr_link, "label", sub_tree["code"]["params"][i]["name"])

        f = open(dot_filename,'w')
        graph.dot(f)
        f.close()
        os.system('dot -Tjpg %(dot)s -o %(jpg)s' %{"dot": dot_filename, "jpg": jpg_filename})
        print "Graph was generated in file '%s'." %jpg_filename

    @classmethod
    def random(cls, **keywords):
        """create a random instrument"""

        const_prob = keywords.get("const_prob") or cls.__CONST_PROB
        max_children = keywords.get("max_children") or cls.__MAX_CHILDREN
        opcodes_file = keywords.get("opcodes_file") or cls.__OPCODES_FILE
        root_type = keywords.get("root_type")

        def get_only_type(the_type, opcodes):
            """get only opcodes the have output of the_type"""
            if the_type == "x":
                types = ["a", "k", "x"]
            else:
                types = [the_type]
            return [op for op in opcodes if op["outtype"] in types]

        def get_only_not_type(the_type, opcodes):
            """get only opcodes that don't have a certain type"""
            return [op for op in opcodes if op["outtype"] != the_type]

        # get list of available opcodes from json file_
        opcodes = json.loads(file(os.path.join(os.path.dirname(__file__), opcodes_file)).read())

        # this only_math avoids creation of constant instruments
        only_math = True
        while only_math:
            # select random root element
            if root_type and root_type == "t":
                # TODO this 1 here has to be changed to a randint when we have more
                # than 1 table in the score
                root = Instrument.__make_node(Instrument.__make_const_code("t", 1))
                inst = Instrument(root)
                return inst
            elif root_type:
                filtered = get_only_type(root_type, opcodes)
            else:
                filtered = get_only_not_type("k", opcodes)
            root = Instrument.__make_node(random.choice(filtered))
            todo = deque([root])
            if root["code"]["type"] != "math":
                only_math = False

            # TODO this number has to be replaced by the max value of the opcode with
            # which it is used
            max_rand_const = 100

            while todo:
                tmp_tree = todo.popleft()

                # if it is a math operator
                if tmp_tree["code"]["type"] == "math":

                    n_children = random.randint(2, max_children)
                    for i in range(n_children):
                        if random.random() > const_prob:
                            filtered = get_only_type(tmp_tree["code"]["intype"], opcodes)
                            filtered = [f for f in filtered if f["type"] == "code"]
                            random_node = Instrument.__make_node(random.choice(filtered))
                            todo.append(random_node)
                        else:
                            const_code = Instrument.__make_const_code("x", random.random() * max_rand_const)
                            random_node = Instrument.__make_node(const_code)

                        tmp_tree["children"].append(random_node)

                # if it is an opcode
                else:
                    for param in tmp_tree["code"]["params"]:

                        # if param type is t alwys plug in a constant
                        if param["type"] == "t":
                            if param["max"] == param["min"]:
                                random_const = param["max"]
                            else:
                                random_const = (random.random() * (param["max"]-param["min"])) + param["min"]
                            const_code = Instrument.__make_const_code("t", random_const)
                            random_node = Instrument.__make_node(const_code)

                        # if it is below constant probability also plug in constant
                        elif param["type"] != "a" and random.random() < const_prob:
                            # choose random constant according to input range and type
                            random_const = (random.random() * (param["max"]-param["min"])) + param["min"]
                            const_code = Instrument.__make_const_code("x", random_const)
                            random_node = Instrument.__make_node(const_code)

                        # when above the constant probability plug in another opcode
                        else:
                            only_math = False
                            filtered = get_only_type(param["type"], opcodes)
                            randop = random.choice(filtered)
                            random_node = Instrument.__make_node(randop)
                            todo.append(random_node)

                        tmp_tree["children"].append(random_node)

            inst = Instrument(root)
            return inst

    def mutate(self):
        """Mutate an instrument.

        This method will return a mutated clone while itself remains
        unchanged. Mutation works by replacing an arbitrary subtree by
        a random tree structure.

        """
        mutant = copy.deepcopy(self)
        flat = Instrument.traverse(mutant.instrument_tree)
        winner = random.randint(0, len(flat) - 1)
        random_tree = Instrument.random(
            root_type = flat[winner]["code"]["outtype"]).instrument_tree
        flat[winner]["code"] = random_tree["code"]
        flat[winner]["children"] = random_tree["children"]
        return mutant

    def ficken(self, other):
        """Cross a tree-instrument with another one."""
        a = copy.deepcopy(self)
        b = copy.deepcopy(other)
        flata = Instrument.traverse(a.instrument_tree)
        flatb = Instrument.traverse(b.instrument_tree)
        candidates = []
        i = 0
        while i < Instrument.__MAX_FICKEN:
            while not candidates:
                winner = random.randint(0, len(flata) - 1)
                crosstype = flata[winner]["code"]["outtype"]
                candidates = [cand for cand in flatb \
                                  if cand["code"]["outtype"] == crosstype]
            winner2 = random.randint(0, len(candidates) - 1)
            flata[winner]["code"] = candidates[winner2]["code"]
            flata[winner]["children"] = candidates[winner2]["children"]
            if a.to_json() != b.to_json():
                return a
        raise Exception("ficken was not successfull")

    @staticmethod
    def traverse(node):
        flat = []
        for child in node["children"]:
            if child["code"]["type"] == "const":
                flat.append(child)
            else:
                flat.extend(Instrument.traverse(child))
        flat.append(node)
        return flat

    def fitness(self):
        """Score of the instrument."""
        return

    @staticmethod
    def __make_node(code):
        """Make a node with no children."""
        return { "code": code, "children": []}

    @staticmethod
    def __make_const_code(outtype, val):
        """make a new constant"""
        return {"name": "const", "type": "const", "outtype": outtype, "value": str(val)}

Individual.register(Instrument)


if __name__ == '__main__':
    i = Instrument.random(const_prob=0.7, max_children=4)
    csd = csound_adapter.CSD()
    csd.orchestra(i)
    csd.score('i 1 0 2')
    csd.play()
    print i.to_json()
    print i.to_instr()

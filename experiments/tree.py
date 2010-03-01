
# simple example with only oscilators and math

import simplejson as json
import random
from collections import deque



# some parameters of the tree
max_sons = 5
constant_prob = 0.7
max_rand_const = 100




# create tree function.
# -start from the root
# -choose an opcode
# -fill its parameters with 
# if max_modules not reached
# => modules
# => else constant
#==> iterate over subtrees

# as long as
# -max number of modules not reached
# -


# what we need to describe the opcodes
# -amount of necessary paremeters
# -type of parameters

# addition and multiplication can always be used

class Tree:
	"""a class for representing the genome tree"""
	
	def __init__(self, code):
		self.code = code
		self.sons = []
		
	def only_const(self):
		"""all sons are constant values?"""
		res = True
		for son in self.sons:
			if son.code["name"] != "const":
				res = False
		return res
		
		
def get_only_type(the_type, opcodes):
	"""get only opcodes the have output of the_type"""
	return [op for op in opcodes if op["outtype"] == the_type]
	
	
	
if __name__ == '__main__':
	
	# get list of available opcodes from json file
	opcodes = json.loads(file("opcodes.json").read())
	
	# select random root element 
	# TODO maybe this has to be constrained to outtype="a" type
	root 			= Tree(random.choice(opcodes))
	
	todo = deque([root])
	
	while todo:
		tmp_tree = todo.popleft()
		
		print tmp_tree.code["name"]
		
		# if it is a math operator
		if tmp_tree.code["type"] == "math":
			n_sons = random.randint(2, max_sons)
			for i in range(n_sons):
				if random.random() > constant_prob:
					random_opcode = Tree(random.choice(opcodes))
					tmp_tree.sons.append(random_opcode)
					todo.append(random_opcode)
				else:
					bla = {"name": "const", "value": random.random() * max_rand_const}
					root.sons.append(Tree(bla))
		else:
			for param in tmp_tree.code["params"]:
				if random.random() > constant_prob:
					filtered = get_only_type(param["type"], opcodes)
					random_opcode = Tree(random.choice(opcodes))
					tmp_tree.sons.append(random_opcode)
					todo.append(random_opcode)
				else:
					bla = {"name": "const", "value": random.random() * max_rand_const}
					root.sons.append(Tree(bla))
					
					
	# tree to code
	

	# out = []
	# queu = deque([root])
	# 
	# while queu:
	# 	tmp = queu.popleft()
	# 	out.append(tmp.code["name"])
	# 	queu.extend(tmp.sons)
	# 	
	# print out
			
	
					
						
		
		
		
		
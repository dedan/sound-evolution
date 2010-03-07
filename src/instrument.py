

class instrument_tree(object):
	"""docstring for instrument_tree"""
	def __init__(self, code):
		"""Constructor
			code describes an opcode 
		"""
		self.code = code
		self.sons = []

		
		
class Instrument(object):
	"""a class for representing the genome tree"""

	def __init__(self, instrument_tree=Null):
		self.instrument_tree = instrument_tree		

	def to_ocr(self):
		"""tree to csound compilation"""
		csound_code = ""
		data 		= []
		for son in n.sons:
			(code, data) 	= son.to_csound
			csound_code 	+= code
			data 			+= data
		return n.render(data)
		
		
	def to_json(self):
		"""generate a json file for a python tree object"""
		pass
		
	def from_json(self):
		"""create a python tree object from a json document"""
		pass

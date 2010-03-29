"""A single csound instrument."""


class Instrument(object):
        """A class representing the genome tree."""

        def __init__(self, instrument_tree=None):
                """"""
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
                pass

        def from_json(self):
                """Deserialize instrument from JSON."""
                pass


class Tree(object):
        """a"""

        def __init__(self, code):
                """"""
                self.code = code
                self.children = []

"""Module that generates csound csd files and calls csound to create
audio files and play in real-time.

"""

import subprocess as sp
import string, sys, os

class CSD(object):
    """This class represents a csd file for csound."""

    def __init__(self):
        self.__instruments = []
        self.__note_list = ''
        self.output_csd_filename = 'default.csd'
        self.output_filename = None
        self.csound_binary = 'csound'
        self.last_run_output = None

    def __del__(self):
        for f in (self.output_csd_filename, self.output_filename):
            if not f is None and os.path.exists(f):
                os.unlink(f)

    def orchestra(self, *args):
        self.__instruments += args

    def orchestra_definition(self):
        result = 'sr = 44100\nkr = 4410\nnchnls = 1\n0dbfs = 1\n'
        for n, inst in enumerate(self.__instruments):
            result += "\ninstr %d\n%s\nendin\n" % (n+1, inst.to_instr())
        return string.rstrip(result)

    def tables(self):
        return "f 1 0 4096 10 1"

    def score(self, *args):
        self.__note_list += string.join(args, '\n') + '\n'

    def score_definition(self):
        return string.rstrip(self.tables() + '\n' + self.__note_list)

    def tagify(self, tag_name, s, newlines=1):
        return '\n<%s>\n%s\n</%s>\n' % (tag_name, s, tag_name)

    def __run_csound(self, output="soundcard", **keywords):
        """Generate a csd file and run csound binary.

        Keyword arguments:
        output -- output mode can be "soundcard" (default) or "aif"
        output_filename -- where to write aif file (defaults to "csd_filename.aif")

        """
        if output == "soundcard":
            self.__options = '-+rtaudio=portaudio -iadc -odac --env:CSNOSTOP=yes -d'
        elif output == "aif":
            self.output_filename = ""
            if "output_filename" in keywords:
                self.output_filename = keywords['output_filename']
            else:
                if self.output_csd_filename.endswith('.csd'):
                    self.output_filename = self.output_csd_filename[:-4] + '.aif'
                else:
                    self.output_filename = self.output_csd_filename + '.aif'
            self.__options = '-A -d -o ' + self.output_filename
        else:
            raise ValueError("Argument 'output' must be either 'soundcard' or 'aif'")
        fp = open(self.output_csd_filename, 'w')
        fp.write('; CSD file created from %s\n' % (sys.argv[0]))
        fp.write(self.tagify(
                'CsoundSynthesizer',
                self.tagify('CsOptions', self.__options) +
                self.tagify('CsInstruments', self.orchestra_definition()) +
                self.tagify('CsScore', self.score_definition()), 0))
        fp.close()
        args = [self.csound_binary, self.output_csd_filename]
        p = sp.Popen(args, stdout=sp.PIPE, stderr=sp.PIPE)
        (stdout, self.last_run_output) = p.communicate()
        if p.returncode != 0:
            raise OSError("Csound execution failed!")

    def play(self):
        """Play a csd object to an audio device using csound."""
        self.__run_csound()

    def output_aif(self, *args):
        if len(args) > 0:
            self.__run_csound(output="aif", output_filename=args[0])
        else:
            self.__run_csound(output="aif")

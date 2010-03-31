"""Generates a sound from a tree-instrument."""

import string, os, sys

class CSD(object):
    
    def __init__(self, output_csd_filename='default.csd', render_sound=0):
        self.set_filenames(output_csd_filename)
        self.render_sound = render_sound
        self.instruments = []
        self.note_list = ''
        print 'Creating CSD file "%s"' % (self.output_csd_filename)
        if render_sound:
            self.options = '-A -d -o %s' % (self.output_sound_filename)            
            print ';rendering to file "%s"' % (self.output_sound_filename)
        else:
            self.options = '-+rtaudio=portaudio -iadc -odac --env:CSNOSTOP=yes -d %s' % (self.output_sound_filename)

    def set_filenames(self, output_csd_filename):
        self.output_csd_filename = output_csd_filename
        if output_csd_filename.endswith('.csd'):
            self.output_sound_filename = output_csd_filename[:-4] + '.aif'
        else:
            self.output_sound_filename = output_csd_filename + '.aif'

    def orchestra(self, *args):
        self.instruments += args

    def orchestra_definition(self):
        result = ''
        n = 1
        for inst in self.instruments:
            result += "sr = 44100\nkr = 4410\nnchnls = 1\n0dbfs = 1\n\ninstr %d\n%s\nendin\n" % (n, inst.to_instr())
            n += 1
        return string.rstrip(result)

    def tables(self):
        return "f 1 0 4096 10 1"

    def score(self, *args):
        self.note_list += string.join(args, '\n') + '\n'

    def score_definition(self):
        return string.rstrip(self.tables() + '\n' + self.note_list)

    def tagify(self, tag_name, s, newlines=1):
        return '\n<%s>\n%s\n</%s>\n' % (tag_name, s, tag_name)

    def output(self, output_csd_filename = None):
        if output_csd_filename:
            self.set_filenames(output_csd_filename)
        fp = open(self.output_csd_filename, 'w')
        fp.write('; CSD file created from %s\n' % (sys.argv[0]))
        fp.write(self.tagify('CsoundSynthesizer',
                             self.tagify('CsOptions', self.options) +
                             self.tagify('CsInstruments', self.orchestra_definition()) +
                             self.tagify('CsScore', self.score_definition()), 0))
        fp.close()
        
        os.system('csound %s' % (self.output_csd_filename))

     

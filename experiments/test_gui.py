import sys
sys.path.append("/home/raf/sound-evolution")

from Tkinter import *
import sound_evolution as se
import os, sys

root = Tk()
f = Frame(root, width = 300, height = 100)
f.pack_propagate(0)
f.pack()

def callback():

    i = se.instrument.Instrument.random(const_prob=0.7, max_children=4)
    csd = se.csound_adapter.CSD()
    csd.orchestra(i)
    csd.score('i 1 0 2')
    csd.play()

b = Button(f, command=callback)
b["text"] = "> Create Sound <"
b["background"] = "green"
b.pack(fill=BOTH, expand=0.8)

root.mainloop()

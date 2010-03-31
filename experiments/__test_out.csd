; CSD file created from test_gui.py

<CsoundSynthesizer>

<CsOptions>
-+rtaudio=portaudio -iadc -odac --env:CSNOSTOP=yes -d __test_out.aif
</CsOptions>

<CsInstruments>
sr = 44100
kr = 4410
nchnls = 1
0dbfs = 1

instr 1
k0	=	89.5606513521/85.1961008726/26.9882174411/20.0001425226
a1	oscil	k0, 2652.5272903, 1
out	a1
endin
</CsInstruments>

<CsScore>
f 1 0 4096 10 1
i 1 0 2
</CsScore>

</CsoundSynthesizer>

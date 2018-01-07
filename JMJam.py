# JMJam.py
#
# Generate music by having user approve or reject random mutations
#
# David Thomsen @D_J_T_

from music import *
from random import *
from time import sleep

pitches = [C5, D5, E5, F5, G5, A5, B5]

pitches1 = []
durations1 = [SN, SN, SN, SN, SN, SN, SN, SN]

for x in range(8):
    pitches1.append(pitches[randint(0, 6)])

theme = Phrase()
theme.addNoteList(pitches1, durations1)

# Will play smoother on my laptop if I pause for a moment before playing.
# I guess even computers need to get mentally prepared.
sleep(1)

Play.midi(theme)

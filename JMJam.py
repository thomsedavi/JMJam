# JMJam.py
#
# Generate music by having user approve or reject random mutations
#
# David Thomsen @D_J_T_

from music import *
from random import *
from time import sleep

pitches = [[C5, E5], [D5, F5], [E5, G5], [F5, A5], [G5, B5], [A5, C6], [B5, D6], [REST]]

pitches1 = []
durations1 = [SN, SN, DSN, TN, TN, DSN, SN, SN]

for x in range(8):
    pitches1.append(pitches[randint(0, 7)])

theme = Phrase()
theme.addNoteList(pitches1, durations1)

# Will play smoother on my laptop if I pause for a moment before playing.
# I guess even computers need to get mentally prepared.
# Note: My laptop is now dead anyway so this probably isn't a problem any more?
sleep(1)

Play.midi(theme)

while (True):
   theme = Phrase()
   pitches1[randint(0, 7)] = pitches[randint(0, 7)]
   theme.addNoteList(pitches1, durations1)
   sleep(2)
   Play.midi(theme)


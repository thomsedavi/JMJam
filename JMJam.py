# JMJam.py
#
# Generate music by having user approve or reject random mutations
# I have this cool keytar with a looping pedal so going to design with that setup in mind.
# Please note that my level of music theory is Minimum Necessary and I'm working with that
#
# David Thomsen @D_J_T_

from music import *
from random import *
from time import sleep

scale = [REST, 0, 2, 4, 5, 7, 9, 11]

# Need to work on randomly generated durations that equal a whole note or whatever
def generateRandomPart(instrument, channel, durations, offset):
   pitches = []
   for x in range(len(durations)):
      pitch = scale[randint(0, 7)]
      pitches.append(pitch if pitch == REST else pitch + offset)
   phrase = Phrase(0.0)
   phrase.addNoteList(pitches, durations)
   part = Part(instrument, channel)
   part.addPhrase(phrase)
   return part

score = Score("Score", 120.0)

score.addPart(generateRandomPart(ELECTRIC_BASS, 1, [QN, QN, QN, QN], 24))
score.addPart(generateRandomPart(ELECTRIC_GRAND, 1, [EN, EN, EN, EN, EN, EN, EN, EN], 48))

# Will play smoother on my laptop if I pause for a moment before playing.
# I guess even computers need to get mentally prepared.
# Note: My laptop is now dead anyway so this probably isn't a problem any more?
sleep(1)

Play.midi(score)

#while (True):
#   theme = Phrase()
#   pitches1[randint(0, 7)] = pitches[randint(0, 7)]
#   theme.addNoteList(pitches1, durations1)
#   sleep(2)
#   Play.midi(theme)


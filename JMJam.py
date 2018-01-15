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

scale = [REST, 0, 2, 4, 5, 7, 9, 11, 12, 14, 16, 17, 19, 21, 23]

class Duration:
   def __init__(self, position, duration):
      self.position = position
      self.duration = duration

class PartDefinition:
   def __init__(self, durationsLength, pitchesLength):
      self.durationIndex = randint(0, durationsLength - 1)
      self.pitchIndex = randint(0, pitchesLength - 1)

class Channel:
   def __init__(self, instrument, channel, offset):
      self.instrument = instrument
      self.channel = channel
      self.offset = offset
      self.durationLists = [[Duration(0, 0.5), Duration(2, 0.5), Duration(4, 0.25), Duration(5, 0.25), Duration(6, 0.5), Duration(8, 1.0), Duration(12, 0.5), Duration(14, 0.5)], [Duration(0, 1.0), Duration(4, 1.0), Duration(8, 1.0), Duration(12, 0.5)]] # will probably need to randomly generate these as well I guess
      self.pitchLists = []
      self.parts = []

      for x in range(2):
         pitches = []
         for x in range(16):
            pitches.append(randint(0, 2))
         self.pitchLists.append(pitches)

      self.parts.append(PartDefinition(len(self.durationLists), len(self.pitchLists)))
      self.parts.append(PartDefinition(len(self.durationLists), len(self.pitchLists)))

   def generatePart(self):
      pitchesList = []
      durationsList = []
      for part in self.parts:
         durations = self.durationLists[part.durationIndex]
         for duration in durations:
            durationsList.append(duration.duration)
            pitch = scale[self.pitchLists[part.pitchIndex][duration.position]]
            pitchesList.append(pitch if pitch == REST else pitch + self.offset)
      phrase = Phrase(0.0)
      phrase.addNoteList(pitchesList, durationsList)
      part = Part(self.instrument, self.channel)
      part.addPhrase(phrase)
      return part

channels = []

channels.append(Channel(ELECTRIC_BASS, 0, 24))
channels.append(Channel(ELECTRIC_GRAND, 1, 48))

score = Score("Score", 120.0)

for channel in channels:
   score.addPart(channel.generatePart())

# Will play smoother on my laptop if I pause for a moment before playing.
# I guess even computers need to get mentally prepared.
# Note: My laptop is now dead anyway so this probably isn't a problem any more?
sleep(1)

Play.midi(score)

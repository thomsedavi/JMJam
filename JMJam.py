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
import copy

# hard coding this in for now
noteDurationSplits = {0.5: [[0.25, 0.25]], 0.75: [[0.25, 0.5], [0.5, 0.25]], 1.0: [[0.25, 0.75], [0.5, 0.5], [0.75, 0.25]]}

class ScaleDefinition:
   def __init__(self, scalePattern, offset):
      scale = []
      note = 0
      index = 0
      while note <= 127:
         scale.append(note)
         note += scalePattern[index]
         index += 1
         index %= 7

      self.scale = scale
      self.offset = offset

   def getPitch(self, pitch):
      return [self.scale[pitch + self.offset]]

class Channel:
   def __init__(self, instrument, channel, scale, offset):
      self.instrument = instrument
      self.channel = channel
      self.scale = ScaleDefinition(scale, offset)
      self.pitches = []
      self.durations = []

   def mutate(self):
      if len(self.pitches) == 0 or randint(0, 2) == 0: # add a new one!
         self.pitches.append(randint(-4, 4))
         self.durations.append(1.0)

      elif len(self.pitches) == 1 or (randint(0, 1) == 0 and any(duration > 0.25 for duration in self.durations)): # split one into two!
         index = randint(0, len(self.pitches) - 1)
         while self.durations[index] == 0.25:
            index = randint(0, len(self.pitches) - 1)

         durationsList = noteDurationSplits[self.durations[index]]
         newDurations = durationsList[randint(0, len(durationsList) - 1)]

         self.durations[index] = newDurations[0]
         self.durations.insert(index + 1, newDurations[1])
         self.pitches.insert(index + 1, self.pitches[index])

      else: # randomly mutate a note
         index = randint(0, len(self.pitches) - 1)
         pitch = self.pitches[index]
         newPitch = randint(-4, 4)

         while newPitch == pitch:
            newPitch = randint(-4, 4)

         self.pitches[index] = newPitch

      #else: join two notes together

   def generatePart(self):
      pitches = []
      for pitch in self.pitches:
         pitches.append(self.scale.getPitch(pitch))
      phrase = Phrase(0.0)
      print pitches
      print self.durations
      phrase.addNoteList(pitches, self.durations)
      part = Part(self.instrument, self.channel)
      part.addPhrase(phrase)
      return part

channels = []

channels.append(Channel(ELECTRIC_GRAND, 0, [2, 2, 1, 2, 2, 2, 1], 36))

while (True):
   score = Score("Score", 120.0)

   mutantChannels = copy.deepcopy(channels)

   for channel in mutantChannels:
      channel.mutate()
      score.addPart(channel.generatePart())

   # Will play smoother on my laptop if I pause for a moment before playing.
   # I guess even computers need to get mentally prepared.
   # Note: My laptop is now dead anyway so this probably isn't a problem any more?
   sleep(1)

   Play.midi(score)
   response = raw_input("Accept mutation")

   if response == 'y':
      channels = mutantChannels

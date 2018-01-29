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

noteDurations = [0.25, 0.5, 1.0, 2.0]

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
      if len(self.pitches) == 0 or randint(0, 1) == 0:
         self.pitches.append(randint(-4, 4))
         self.durations.append(noteDurations[randint(0, len(noteDurations) - 1)])
      else:
         randomNumber = randint(0, 2)
         randomIndex = randint(0, len(self.pitches) - 1)
         if randomNumber <= 1:
            self.pitches[randomIndex] = randint(-4, 4)
         if randomNumber >= 1:
            self.durations[randomIndex] = noteDurations[randint(0, len(noteDurations) - 1)]

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

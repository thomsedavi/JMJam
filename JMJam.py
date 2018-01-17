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

class NoteDefinition:
   def __init__(self, position, duration):
      self.position = position
      self.duration = duration

class PartDefinition:
   def __init__(self, durationsLength, pitchesLength):
      self.durationIndex = randint(0, durationsLength - 1)
      self.pitchIndexes = []
      for x in range(pitchesLength):
         self.pitchIndexes.append(randint(0, 1))

class Channel:
   def __init__(self, instrument, channel, scale, offset):
      self.instrument = instrument
      self.channel = channel
      self.offset = offset
      self.noteLists = [[NoteDefinition(0, 0.5), NoteDefinition(2, 0.5), NoteDefinition(4, 0.25), NoteDefinition(5, 0.25), NoteDefinition(6, 0.5), NoteDefinition(8, 1.0), NoteDefinition(12, 0.5), NoteDefinition(14, 0.5)], [NoteDefinition(0, 1.0), NoteDefinition(4, 1.0), NoteDefinition(8, 1.0), NoteDefinition(12, 0.5)], [NoteDefinition(0, 0.25), NoteDefinition(1, 0.25), NoteDefinition(2, 0.5), NoteDefinition(4, 0.5), NoteDefinition(6, 0.5), NoteDefinition(8, 0.25), NoteDefinition(9, 0.25), NoteDefinition(10, 0.5), NoteDefinition(12, 0.5), NoteDefinition(14, 0.5)]] # will probably need to randomly generate these as well I guess
      self.pitchLists = []
      self.parts = []
      self.scale = ScaleDefinition(scale, offset)

      # any kind of simple pattern is more musical than pure randomness to start with
      for x in range(3):
         pitches = []
         pitch1 = randint(-1, 1)
         pitch2 = randint(-1, 1)
         for x in range(8):
            y = randint(-2, 2)
            pitches.append(pitch1 + y)
            pitches.append(pitch2 + y)
         self.pitchLists.append(pitches)

      self.parts.append(PartDefinition(len(self.noteLists), len(self.pitchLists)))
      self.parts.append(PartDefinition(len(self.noteLists), len(self.pitchLists)))

   def generatePart(self):
      pitchesList = []
      durationsList = []
      for part in self.parts:
         notes = self.noteLists[part.durationIndex]
         for note in notes:
            durationsList.append(note.duration)
            pitch = 0
            for x in range(len(self.pitchLists)):
               if part.pitchIndexes[x] == 1:
                   pitch += self.pitchLists[x][note.position]
      
            pitchesList.append(self.scale.getPitch(pitch))
      phrase = Phrase(0.0)
      phrase.addNoteList(pitchesList, durationsList)
      part = Part(self.instrument, self.channel)
      part.addPhrase(phrase)
      return part

channels = []

channels.append(Channel(ELECTRIC_BASS, 0, [2, 2, 1, 2, 2, 2, 1], 24))
channels.append(Channel(ELECTRIC_GRAND, 1, [2, 2, 1, 2, 2, 2, 1], 36))

score = Score("Score", 120.0)

for channel in channels:
   score.addPart(channel.generatePart())

# Will play smoother on my laptop if I pause for a moment before playing.
# I guess even computers need to get mentally prepared.
# Note: My laptop is now dead anyway so this probably isn't a problem any more?
sleep(1)

Play.midi(score)

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
         self.pitchIndexes.append(True if randint(0, 1) == 1 else False)

# any kind of simple pattern is more musical than pure randomness to start with
def generatePitches():
   pitches = []
   pitch1 = randint(-1, 1)
   pitch2 = randint(-1, 1)
   for x in range(8):
      y = randint(-2, 2)
      pitches.append(pitch1 + y)
      pitches.append(pitch2 + y)
   return pitches

class Channel:
   def __init__(self, instrument, channel, scale, offset):
      self.instrument = instrument
      self.channel = channel
      self.offset = offset
      self.noteLists = [
      [NoteDefinition(0, 0.5), NoteDefinition(2, 0.5), NoteDefinition(4, 0.5), NoteDefinition(6, 0.5), NoteDefinition(8, 0.5), NoteDefinition(10, 0.5), NoteDefinition(12, 0.5), NoteDefinition(14, 0.5)],
      [NoteDefinition(0, 0.25), NoteDefinition(1, 0.25), NoteDefinition(2, 0.5), NoteDefinition(4, 0.25), NoteDefinition(5, 0.25), NoteDefinition(6, 0.5), NoteDefinition(8, 0.25), NoteDefinition(9, 0.25), NoteDefinition(10, 0.5), NoteDefinition(12, 0.25), NoteDefinition(13, 0.25), NoteDefinition(14, 0.5)],
      [NoteDefinition(0, 0.5), NoteDefinition(2, 0.25), NoteDefinition(3, 0.25), NoteDefinition(4, 0.5), NoteDefinition(6, 0.25), NoteDefinition(7, 0.25), NoteDefinition(8, 0.5), NoteDefinition(10, 0.25), NoteDefinition(11, 0.25), NoteDefinition(12, 0.5), NoteDefinition(14, 0.25), NoteDefinition(15, 0.25)]
      ] # will probably need to randomly generate these as well I guess
      self.pitchLists = []
      self.parts = []
      self.scale = ScaleDefinition(scale, offset)

      for x in range(3):
         self.pitchLists.append(generatePitches())

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
               if x == len(part.pitchIndexes):
                  part.pitchIndexes.append(False)
               else:
                  if part.pitchIndexes[x] == True:
                      pitch += self.pitchLists[x][note.position]

            pitchesList.append(self.scale.getPitch(pitch))
      phrase = Phrase(0.0)
      phrase.addNoteList(pitchesList, durationsList)
      part = Part(self.instrument, self.channel)
      part.addPhrase(phrase)
      return part

   def mutate(self):
      change = randint(0, 1)
      if change == 0:
         part = self.parts[randint(0, len(self.parts) - 1)]
         durationIndex = randint(0, len(self.noteLists) - 1)
         while durationIndex == part.durationIndex:
            durationIndex = randint(0, len(self.noteLists) - 1)
         part.durationIndex = durationIndex
      if change == 1:
         part = self.parts[randint(0, len(self.parts) - 1)]
         pitchIndex = randint(0, len(part.pitchIndexes))
         if pitchIndex < len(part.pitchIndexes):
            part.pitchIndexes[pitchIndex] = not part.pitchIndexes[pitchIndex]
         else:
            self.pitchLists.append(generatePitches())
            part.pitchIndexes.append(True)

channels = []

channels.append(Channel(ELECTRIC_GRAND, 1, [2, 2, 1, 2, 2, 2, 1], 36))

score = Score("Score", 120.0)

for channel in channels:
   score.addPart(channel.generatePart())

# Will play smoother on my laptop if I pause for a moment before playing.
# I guess even computers need to get mentally prepared.
# Note: My laptop is now dead anyway so this probably isn't a problem any more?
sleep(1)

Play.midi(score)

while(True):
   sleep(4)

   score = Score("newScore", 120.0)

   for channel in channels:
      channel.mutate()
      score.addPart(channel.generatePart())

   sleep(1)

   Play.midi(score)
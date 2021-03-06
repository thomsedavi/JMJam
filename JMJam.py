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
# infuriatingly neither pickle nor tkinter seem to be working for me so I'm doing workarounds just to get this actually working
# import pickle
# import tkinter

# hard coding this in for now
noteDurationSplits = {0.5: [[0.25, 0.25]], 0.75: [[0.25, 0.5], [0.5, 0.25]], 1.0: [[0.25, 0.75], [0.5, 0.5], [0.75, 0.25]]}
noteDurationJoins = [0.5, 0.75, 1.0, 1.5, 2.0, 3.0, 4.0]
chords = [[], [1, 3], [1, 4], [2], [2, 3], [2, 4]]

def canMergeNotes(durations):
   for index in range(0, len(durations) - 1):
      if durations[index] + durations[index + 1] in noteDurationJoins:
         return True
      return False

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

   def getPitch(self, pitch, chordIndex):
      chord = [self.scale[pitch + self.offset]]
      if chordIndex:
         thang = chords[chordIndex]
         for thing in thang: #I have no idea what the correct music terminology for this would be
            chord.append(self.scale[pitch + self.offset + thing])
      return chord

class Channel:
   def __init__(self, instrument, channel, scalePattern, offset, pitches, durations, chordIndexes):
      self.instrument = instrument
      self.channel = channel
      self.scalePattern = scalePattern
      self.offset = offset
      self.scale = ScaleDefinition(scalePattern, offset)
      self.pitches = pitches
      self.durations = durations
      self.chordIndexes = chordIndexes

   def mutate(self):
      mutated = False

      while not mutated:
         diceRoll = randint(0, 5)
         print diceRoll

         if len(self.pitches) == 0 or diceRoll == 0: # add a new one!
            self.pitches.append(randint(-4, 4))
            self.durations.append(1.0)
            self.chordIndexes.append(0 if randint(0, 1) == 0 else self.chordIndexes[len(self.chordIndexes) - 1] if len(self.chordIndexes) > 0 and randint(0, 1) == 0 else randint(1, len(chords) - 1))
            mutated = True

         elif len(self.pitches) > 0 and (diceRoll == 1 and any(duration >= 0.5 and duration <= 1.0 for duration in self.durations)): # split one into two!
            index = randint(0, len(self.pitches) - 1)
            while self.durations[index] == 0.25:
               index = randint(0, len(self.pitches) - 1)

            durationsList = noteDurationSplits[self.durations[index]]
            newDurations = durationsList[randint(0, len(durationsList) - 1)]

            self.durations[index] = newDurations[0]
            self.durations.insert(index + 1, newDurations[1])
            self.pitches.insert(index + 1, self.pitches[index])
            self.chordIndexes.insert(index + 1, self.chordIndexes[index])
            mutated = True

         elif canMergeNotes(self.durations) and diceRoll == 2: # merge two into one
            merged = False

            while not merged:
               index = randint(0, len(self.durations) - 2)
               if self.durations[index] + self.durations[index + 1] in noteDurationJoins:
                  newDuration = self.durations[index] + self.durations[index + 1]
                  self.durations[index] = newDuration
                  del self.durations[index + 1]
                  del self.pitches[index + 1]
                  del self.chordIndexes[index + 1]
                  merged = True
            mutated = True

         elif diceRoll == 3: #modify some chords
            actuallyDifferent = False

            while not actuallyDifferent:
               index1 = randint(0, len(self.durations))
               index2 = randint(0, len(self.durations))

               if index2 < index1: # I feel like there's probably some clever way to do this but it'll take longer to google than to just write this
                  temp = index1
                  index1 = index2
                  index2 = temp

               newChordIndex = 0 if randint(0, 1) == 0 else randint(1, len(chords) - 1)

               newChordIndexes = copy.deepcopy(self.chordIndexes)
               for index in range(index1, index2):
                  newChordIndexes[index] = newChordIndex

               if newChordIndexes != self.chordIndexes:
                  actuallyDifferent = True
                  self.chordIndexes = newChordIndexes
            mutated = True

         elif diceRoll == 4: # randomly mutate a note
            index = randint(0, len(self.pitches) - 1)
            pitch = self.pitches[index]
            newPitch = randint(-4, 4)

            while newPitch == pitch:
               newPitch = randint(-4, 4)

            self.pitches[index] = newPitch
            mutated = True

         elif diceRoll == 5: # duplicate a random range and slap on the end
            startIndex = 0 if randint(0, 1) == 0 else randint(0, len(self.pitches))
            endIndex = len(self.pitches) if randint(0, 1) == 0 else randint(0, len(self.pitches))

            if startIndex > endIndex: # See my earlier comment
               temp = startIndex
               startIndex = endIndex
               endIndex = temp

            self.pitches.extend(self.pitches[startIndex:endIndex])
            self.durations.extend(self.durations[startIndex:endIndex])
            self.chordIndexes.extend(self.chordIndexes[startIndex:endIndex])
            mutated = True

   def generatePart(self):
      pitches = []
      for index in range(len(self.pitches)):
         pitches.append(self.scale.getPitch(self.pitches[index], self.chordIndexes[index]))
      phrase = Phrase(0.0)
      print pitches
      print self.durations
      print self.chordIndexes
      phrase.addNoteList(pitches, self.durations)
      part = Part(self.instrument, self.channel)
      part.addPhrase(phrase)
      return part

   def write(self, file):
      file.write("Channel\n")
      file.write(str(self.instrument) + "\n")
      file.write(str(self.channel) + "\n")
      file.write(str(self.pitches) + "\n")
      file.write(str(self.durations) + "\n")
      file.write(str(self.chordIndexes) + "\n")
      file.write(str(self.scalePattern) + "\n")
      file.write(str(self.offset) + "\n")

class BassChannel:
   def __init__(self, instrument, channel, scale, offset):
      self.instrument = instrument
      self.channel = channel
      self.scale = ScaleDefinition(scale, offset)
      self.pitches = [0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1]
      self.durations = [0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5]

   def generatePart(self):
      pitches = []
      for index in range(len(self.pitches)):
         pitches.append(self.scale.getPitch(self.pitches[index], None))
      phrase = Phrase(0.0)
      print pitches
      print self.durations
      phrase.addNoteList(pitches, self.durations)
      part = Part(self.instrument, self.channel)
      part.addPhrase(phrase)
      return part

channels = []
bassChannels = []

response = raw_input("Load from file?")

if response == 'y':
   filename = raw_input("Please enter filename")
   file = open(filename, 'rb')

   nekMinnit = file.readline()

   while (nekMinnit != "End\n"):
      if (nekMinnit == "Channel\n"):
         instrument = int(file.readline()[:-1])
         channel = int(file.readline()[:-1])
         pitches = eval(file.readline()[:-1])
         durations = eval(file.readline()[:-1])
         chordIndexes = eval(file.readline()[:-1])
         scalePattern = eval(file.readline()[:-1])
         offset = int(file.readline()[:-1])

         channels.append(Channel(instrument, channel, scalePattern, offset, pitches, durations, chordIndexes))

      nekMinnit = file.readline()

   file.close()

else:
   channels.append(Channel(ELECTRIC_GRAND, 0, [2, 2, 1, 2, 2, 2, 1], 36, [], [], []))
   #bassChannels.append(BassChannel(ELECTRIC_BASS, 1, [2, 2, 1, 2, 2, 2, 1], 24))

while (True):
   score = Score("Score", 120.0)

   mutantChannels = copy.deepcopy(channels)

   for channel in mutantChannels:
      channel.mutate()
      score.addPart(channel.generatePart())

   for bassChannel in bassChannels:
      score.addPart(bassChannel.generatePart())

   # Will play smoother on my laptop if I pause for a moment before playing.
   # I guess even computers need to get mentally prepared.
   # Note: My laptop is now dead anyway so this probably isn't a problem any more?
   sleep(1)

   Play.midi(score)
   response = raw_input("Accept mutation")

   if response == 'y':
      channels = mutantChannels

   if response == 's':
      channels = mutantChannels
      file = open("testfile.txt","wb")

      for channel in mutantChannels:
         channel.write(file)

      file.write("End\n")
      file.close()

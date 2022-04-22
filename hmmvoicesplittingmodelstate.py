import sys
import bisect

from mathutils import MathUtils
from voicesplittingmodelstate import VoiceSplittingModelState
from voice import Voice
import time
import math


class HmmVoiceSplittingModelState(VoiceSplittingModelState):

    def _initialize_instance_fields(self):
        self.__voices = None
        self.__logProb = 0
        self.__params = None
        self.start_time = time.time()

    def __init__(self):
        self._initialize_instance_fields()

    def set_fields(self, logProb, voices, params):
        self._initialize_instance_fields()
        self.__voices = voices
        self.__logProb = logProb
        self.__params = params

    def handle_incoming(self, notes):
        indices = self.__getOpenVoiceIndices(notes, self.__voices)
        return self.__getAllCandidateNewStatesRecursive(indices, notes,
                                                        self.__voices, self.__logProb, 0)

    def __getAllCandidateNewStatesRecursive(self, openVoiceIndices, incoming, newVoices, logProbSum, noteIndex):
        self.curr_time = time.time()
        if noteIndex == len(incoming) or round(self.curr_time - self.start_time) > 20:
            newStates = []
            state = HmmVoiceSplittingModelState()
            new_vcs = []
            for t in newVoices:
                new_vcs.append(t)
            state.set_fields(logProbSum, new_vcs, self.__params)
            bisect.insort(newStates, state)
            return newStates
        newStates = []
        self.curr_time = time.time()
        if round(self.curr_time - self.start_time) == 20:
            return
        if len(self.__voices) < 0x7fffffff:
            newVoiceProbs = [0 for _ in range(len(newVoices) + 1)]
            i = 0
            while i < len(newVoiceProbs):
                newVoiceProbs[i] = self.__getTransitionProb(incoming[noteIndex], -i - 1, newVoices)
                i += 1

            maxIndex = MathUtils.getMaxIndex(newVoiceProbs)
            if maxIndex != -1:
                self.__addNewVoicesRecursive(openVoiceIndices, incoming, newVoices, logProbSum, noteIndex,
                                             newVoiceProbs, newVoiceProbs[maxIndex], newStates)

        # Add to existing voices
        existingVoiceProbs = [0 for _ in range(len(openVoiceIndices[noteIndex]))]
        i = 0
        while i < len(existingVoiceProbs):
            existingVoiceProbs[i] = self.__getTransitionProb(incoming[noteIndex], openVoiceIndices[noteIndex][i],
                                                             newVoices)
            i += 1

        self.__addToExistingVoicesRecursive(openVoiceIndices, incoming, newVoices, logProbSum, noteIndex,
                                            existingVoiceProbs, newStates)

        return newStates

    def __addNewVoicesRecursive(self, openVoiceIndices, incoming, newVoices, logProbSum, noteIndex, newVoiceProbs,
                                maxValue, newStates):
        self.curr_time = time.time()
        if round(self.curr_time - self.start_time) > 20:
            return
        if len(newVoices) < sys.maxsize:
            newVoiceIndex = 0
            while newVoiceIndex < len(newVoiceProbs):
                if newVoiceProbs[newVoiceIndex] == maxValue:
                    # Add at any location with max probability
                    self.__doTransition(incoming[noteIndex], -newVoiceIndex - 1, newVoices)

                    # Fix openVoiceIndices
                    note = noteIndex + 1
                    while note < len(openVoiceIndices):
                        voice = 0
                        while voice < len(openVoiceIndices[note]):
                            if openVoiceIndices[note][voice] >= newVoiceIndex:
                                openVoiceIndices[note][voice] = openVoiceIndices[note][voice] + 1
                            voice += 1
                        note += 1

                    # (Pseudo-)recursive call
                    for temp in self.__getAllCandidateNewStatesRecursive(openVoiceIndices, incoming, newVoices,
                                                                         logProbSum + newVoiceProbs[newVoiceIndex],
                                                                         noteIndex + 1):
                        bisect.insort(newStates, temp)

                    # Fix for memory overflow - trim newStates as soon as we can

                    while len(newStates) > self.__params.BEAM_SIZE:
                        newStates.pop()

                    # The objects are mutable, so reverse changes. This helps with memory usage as well.
                    self.__reverseTransition(-newVoiceIndex - 1, newVoices)

                    # Reverse openVoiceIndices
                    note = noteIndex + 1
                    while note < len(openVoiceIndices):
                        voice = 0
                        while voice < len(openVoiceIndices[note]):
                            if openVoiceIndices[note][voice] > newVoiceIndex:
                                openVoiceIndices[note][voice] = openVoiceIndices[note][voice] - 1
                            voice += 1
                        note += 1
                newVoiceIndex += 1

    def __addToExistingVoicesRecursive(self, openVoiceIndices, incoming, newVoices, logProbSum, noteIndex,
                                       existingVoiceProbs, newStates):
        self.curr_time = time.time()
        if round(self.curr_time - self.start_time) > 20:
            return
        openVoiceIndex = 0
        while openVoiceIndex < len(existingVoiceProbs):
            # Try the transition
            voiceIndex = openVoiceIndices[noteIndex][openVoiceIndex]
            self.__doTransition(incoming[noteIndex], voiceIndex, newVoices)
            # Fix openVoiceIndices
            removed = [False for _ in range(len(openVoiceIndices))]
            note = noteIndex + 1
            while note < len(openVoiceIndices):

                if openVoiceIndices[note].__contains__(voiceIndex):
                    openVoiceIndices[note].remove(voiceIndex)
                    removed[note] = True
                note += 1
            # (Pseudo-)recursive call
            for temp in self.__getAllCandidateNewStatesRecursive(openVoiceIndices, incoming, newVoices,
                                                                 logProbSum + existingVoiceProbs[openVoiceIndex],
                                                                 noteIndex + 1):
                bisect.insort(newStates, temp)

            # Remove extras from newStates to save memory
            while len(newStates) > self.__params.BEAM_SIZE:
                newStates.pop()

            # Reverse transition
            self.__reverseTransition(voiceIndex, newVoices)

            # Reverse openVoiceIndices
            j = noteIndex + 1
            while j < len(removed):
                if removed[j]:
                    note = None
                    note = 0
                    while note < len(openVoiceIndices[j]) and openVoiceIndices[j][note] < voiceIndex:
                        pass
                        note += 1
                    openVoiceIndices[j].insert(note, voiceIndex)
                j += 1
            openVoiceIndex += 1

    def __getOpenVoiceIndices(self, incoming, voices):
        onsetTime = incoming[0].getOnsetTime()
        openIndices = []
        for note in incoming:
            noteOpen = []
            i = 0
            while i < len(voices):
                if note is not None and voices[i] is not None:
                    if voices[i].canAddNoteAtTime(onsetTime, note.getDurationTime(), self.__params):
                        noteOpen.append(i)
                i += 1
            openIndices.append(noteOpen)
        return openIndices

    def __reverseTransition(self, transition, newVoices):
        self.curr_time = time.time()
        if round(self.curr_time - self.start_time) > 20:
            return
        # For new Voices, we need to add the Voice, and then update the transition value to
        # point to that new Voice so the lower code works.
        if transition < 0 and newVoices.__contains__(-transition - 1):
            newVoices.remove(-transition - 1)
        elif newVoices[transition]:
            newVoices[transition] = newVoices[transition].get_previous()

    def __doTransition(self, note, transition, newVoices):
        self.curr_time = time.time()
        if round(self.curr_time - self.start_time) > 20:
            return
        # For new Voices, we need to add the Voice, and then update the transition value to
        # point to that new Voice so the lower code works.
        if transition < 0:
            transition = -transition - 1
            newVoices.insert(transition, Voice(note, None))
        else:
            newVoices[transition] = Voice(note, newVoices[transition])

    def __getTransitionProb(self, note, transition, newVoices):
        self.curr_time = time.time()

        logProb = None

        # For new Voices, we need to add the Voice, and then update the transition value to
        # point to that new Voice so the lower code works.
        if transition < 0:
            transition = -transition - 1
            logProb = math.log(self.__params.NEW_VOICE_PROBABILITY)
            prev = None if transition == 0 else newVoices[transition - 1]
            next = None if transition == len(newVoices) else newVoices[transition]
        else:
            if newVoices[transition] is not None:
                logProb = math.log(newVoices[transition].getProbability(note, self.__params))
            prev = None if transition == 0 else newVoices[transition - 1]
            next = None if transition == len(newVoices) - 1 else newVoices[transition + 1]

        # Check if we are in the wrong order with the prev or next Voices (or both)
        if prev is not None and note.getPitch() < prev.get_most_recent_note().getPitch():
            if logProb is not None:
                logProb = logProb - math.log(2)
            else:
                logProb = 1.7976931348623157e+308

        if next is not None and note.getPitch() > next.get_most_recent_note().getPitch():
            if logProb is not None:
                logProb = logProb - math.log(2)
            else:
                logProb = 1.7976931348623157e+308

        if logProb == -float("-inf") or logProb is None:
            logProb = 1.7976931348623157e+308

        return logProb

    def getVoices(self):
        return self.__voices

    def get_score(self):
        return self.__logProb

    def __str__(self):
        return str(self.__voices) + " " + str(self.__logProb)

    def __lt__(self, other):
        return (self.__logProb, len(self.__voices)) < (other.__logProb, len(other.__voices))

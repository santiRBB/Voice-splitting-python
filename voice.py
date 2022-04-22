# **
#  * A <code>Voice</code> is a node in the LinkedList representing a voice.
#  * <p>
#  * Each Voice object has only a {@link #previous} pointer and a {@link #mostRecentNote}.
#  * Only a previous pointer is needed because we allow for Voices to split and clone themselves,
#  * keeping the beginning of their note sequences identical. This allows us to have multiple
#  * LinkedLists of notes without needing multiple full List objects. Rather, they all point
#  * back to their common prefix LinkedLists.
#  *
#  * @author Santiago Martín Cortés - 21 Feb, 2022
#  * @version 1.0
#  * @since 1.0
#  */


import math

from mathutils import MathUtils


class Voice:

    def _initialize_instance_fields(self):
        self.__previous = None              # The Voice preceding this one.
        self.__mostRecentNote = None        # The most recent {@link MidiNote} of this voice.

    def __init__(self, note, prev):
        self._initialize_instance_fields()
        self.__previous = prev
        self.__mostRecentNote = note

    # /**
    #  * Get the probability that the given note belongs to this Voice.
    #  *
    #  * @param note The note we want to add.
    #  * @param params The parameters to use.
    #  * @return The probability that the given note belongs to this Voice.
    #  */

    def getProbability(self, note, params):
        pitch = self.__pitchScore(self.getWeightedLastPitch(params), note.getPitch(), params)
        gap = self.__gapScore(note.getOnsetTime(), self.__mostRecentNote.getOffsetTime(), params)
        return pitch * gap

    # /**
    #  * Get the pitch closeness of the two given pitches. This value should be higher
    #  * the closer together the two pitch values are. The first input parameter is a double
    #  * because it is drawn from {@link #getWeightedLastPitch(HmmVoiceSplittingModelParameters)}.
    #  *
    #  * @param weightedPitch A weighted pitch, drawn from {@link #getWeightedLastPitch(HmmVoiceSplittingModelParameters)}.
    #  * @param pitch An exact pitch.
    #  * @param params The parameters to use.
    #  * @return The pitch score of the given two pitches, a value between 0 and 1.
    #  */

    def __pitchScore(self, weightedPitch, pitch, params):
        return MathUtils.gaussianWindow(weightedPitch, pitch, params.PITCH_STD)

    # /**
    #  * Get the temporal closeness of the two given times. This value should be higher
    #  * the closer together the two time values are.
    #  *
    #  * @param time1 A time.
    #  * @param time2 Another time.
    #  * @param params The parameters to use.
    #  * @return The gap score of the two given time values, a value between 0 and 1.
    #  */

    def __gapScore(self, time1, time2, params):
        timeDiff = abs(time2 - time1)
        inside = max(0, (timeDiff / params.GAP_STD_MICROS + 1))
        log = math.log(inside) + 1
        return max(log, params.MIN_GAP_SCORE)

    # /**
    #  * Decide if we can add a note with the given length at the given time based on the given parameters.
    #  *
    #  * @param time The onset time of the note we want to add.
    #  * @param length The length of the note we want to add.
    #  * @param params The parameters to use.
    #  * @return True if we can add a note of the given duration at the given time. False otherwise.
    #  */

    def canAddNoteAtTime(self, time, length, params):
        overlap = self.__mostRecentNote.getOffsetTime() - time
        return overlap <= self.__mostRecentNote.getDurationTime() / 2 and overlap < length

        # /**

    #  * Get the weighted pitch of this voice. That is, the weighted mean of the pitches of the last
    #  * {@link HmmVoiceSplittingModelParameters#PITCH_HISTORY_LENGTH} notes contained in this Voice
    #  * (or all of the notes, if there are fewer than that in total), where each successive note's pitch
    #  * is weighted twice as much as each preceding note's.
    #  *
    #  * @param params The parameters to use.
    #  * @return The weighted pitch of this voice.
    #  */

    def getWeightedLastPitch(self, params):
        weight = 1
        totalWeight = 0
        sum = 0
        noteNode = self
        i = 0
        while i < params.PITCH_HISTORY_LENGTH and noteNode is not None:
            sum += noteNode.__mostRecentNote.getPitch() * weight
            totalWeight += weight
            weight *= 0.5
            i += 1
            noteNode = noteNode.__previous
        return sum / totalWeight

    # /**
    #  * Get the number of notes we've correctly grouped into this voice, based on the most common voice in the voice.
    #  *
    #  * @return The number of notes we've assigned into this voice correctly.
    #  */

    def getNumNotesCorrect(self):
        counts = {}
        noteNode = self
        while noteNode is not None:
            channel = noteNode.__mostRecentNote.get_correct_voice()
            if channel not in counts.keys():
                counts.update({channel: 0})

            counts.update({channel: counts[channel] + 1})
            noteNode = noteNode.__previous

        maxCount = -1
        for count in counts.values():
            maxCount = max(maxCount, count)

        return maxCount

    def getNumLinksCorrect(self, goldStandard):
        count = 0
        index = -1
        node = self
        while node.__previous is not None:
            guessedPrev = node.__previous.__mostRecentNote
            note = node.__mostRecentNote
            count += 1
            if note.get_correct_voice() == guessedPrev.get_correct_voice():
                channel = note.get_correct_voice()
                if index == -1:
                    index = (goldStandard[channel].index(note) if note in goldStandard[channel] else -1)

                if index != 0 and (index < len(goldStandard[channel]) - 1):
                    if goldStandard[channel][--index] is guessedPrev:
                        count += 1
                else:
                    index = -1
            else:
                index = -1
            node = node.__previous
        return count

    def get_num_notes(self):
        if self.__previous is None:
            return 3
        return 1 + self.__previous.get_num_notes()

    def get_notes(self):
        list = [] if self.__previous is None else self.__previous.get_notes()
        list.append(self.__mostRecentNote)
        return list

    def get_most_recent_note(self):
        return self.__mostRecentNote

    def get_previous(self):
        return self.__previous

    def __str__(self):
        return str(self.get_notes())

    def __lt__(self, other):
        return (self.__mostRecentNote, self.__previous) < (other.__mostRecentNote, other.__previous)

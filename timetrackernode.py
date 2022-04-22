# /**
#  * A TimeTrackerNode represents the state of a musical score at a given time, and is
#  * able to convert between MIDI ticks and seconds. That is, it represents a
#  * <{@link voicesplitting.time.TimeSignature}, {@link voicesplitting.time.Tempo},
#  * {@link voicesplitting.time.KeySignature}> triple, and contains information about the times at
#  * which that triple is valid.
#  * All of the TimeTrackerNodes are kept track of by a single master {@link TimeTracker} object
#  * per song, which organizes them into a list and queries appropriately based on each one's
#  * valid times.
#  *
#  * @author Santiago Martín Cortés - 30 Nov, 2021
#  * @version 1.0
#  * @since 1.0
#  */


from keysignature import KeySignature
from timesignature import TimeSignature
from tempo import Tempo


class TimeTrackerNode:

    # 	/**
    # 	 * Create a new TimeTrackerNode with the given previous TimeTrackerNode at the given tick.
    # 	 *
    # 	 * @param prev The previous TimeTrackerNode
    # 	 * @param ppq The pulses per quarter note of the song.
    # 	 * @param tick The tick at which this new one becomes valid.
    # 	 */

    def __init__(self, prev, tick, ppq):
        self.__startTick = 0    # The start tick for this TimeTrackerNode. That is, the tick at which this ones triple becomes valid.
        self.__startTime = 0    # The start time for this TimeTrackerNode, measured in microseconds. That is, the time at which this one's triple becomes valid.
        self.__timeSignature = None # The TimeSignature associated with this TimeTrackerNode.
        self.__tempo = None    # The Tempo associated with this TimeTrackerNode.
        self.__keySignature = None  # The KeySignature associated with this TimeTrackerNode.
        self.__startTick = tick     # The start tick for this TimeTrackerNode. That is, the tick at which this ones triple becomes valid.

        if prev is not None:
            self.__startTime = prev.get_time_at_tick(tick, ppq)
            self.__timeSignature = prev.getTimeSignature()
            self.__tempo = prev.getTempo()
            self.__keySignature = prev.getKeySignature()

        else:
            self.__timeSignature = TimeSignature()
            self.__tempo = Tempo()
            self.__keySignature = KeySignature()

    # 	/**
    # 	 * Get the tick number at the given time.
    # 	 *
    # 	 * @param time The time at which we want the tick, measured in microseconds.
    # 	 * @param ppq The pulses per quarter note of the song.
    # 	 * @return The tick at the given time.
    # 	 */

    def get_tick_at_time(self, time, ppq):
        timeOffset = time - self.getStartTime()
        return int((timeOffset / self.__getTimePerTick(ppq))) + self.getStartTick()

    # 	/**
    # 	 * Get the time at the given tick.
    # 	 *
    # 	 * @param tick The tick at which we want the time.
    # 	 * @param ppq The pulses per quarter note of the song.
    # 	 * @return The time at the given tick, measured in microseconds.
    # 	 */


    def get_time_at_tick(self, tick, ppq):
        tickOffset = tick - self.getStartTick()
        return int((tickOffset * self.__getTimePerTick(ppq))) + self.getStartTime()

    # 	/**
    # 	 * Gets the amount of time, in microseconds, that passes between each tick.
    # 	 *
    # 	 * @param ppq The pulses per quarter note of the song.
    # 	 * @return The length of a tick in microseconds.
    # 	 */

    def __getTimePerTick(self, ppq):
        return self.__tempo.getMicroSecondsPerQuarter() / ppq

    # 	/**
    # 	 * Get the start tick of this node.
    # 	 *
    # 	 * @return {@link #startTick}
    # 	 */

    def getStartTick(self):
        return self.__startTick

    # 	/**
    # 	 * Get the start time of this node.
    # 	 *
    # 	 * @return {@link #startTime}
    # 	 */

    def getStartTime(self):
        return self.__startTime

    # 	/**
    # 	 * Set the Tempo of this node.
    # 	 *
    # 	 * @param tempo {@link #tempo}
    # 	 */

    def setTempo(self, tempo):
        self.__tempo = tempo

    # 	/**
    # 	 * Set the TimeSignature of this node.
    # 	 *
    # 	 * @param timeSignature {@link #timeSignature}
    # 	 */

    def setTimeSignature(self, timeSignature):
        self.__timeSignature = timeSignature

    # 	/**
    # 	 * Set the KeySignature of this node.
    # 	 *
    # 	 * @param keySignature {@link #keySignature}
    # 	 */

    def setKeySignature(self, keySignature):
        self.__keySignature = keySignature

    # 	/**
    # 	 * Get the TimeSignature of this node.
    # 	 *
    # 	 * @return {@link #timeSignature}
    # 	 */

    def getTimeSignature(self):
        return self.__timeSignature

    # 	/**
    # 	 * Get the Tempo of this node.
    # 	 *
    # 	 * @return {@link #tempo}
    # 	 */

    def getTempo(self):
        return self.__tempo

    # 	/**
    # 	 * Get the KeySignature of this node.
    # 	 *
    # 	 * @return {@link #keySignature}
    # 	 */

    def getKeySignature(self):
        return self.__keySignature

    # 	/**
    # 	 * Get the String representation of this TimeTrackerNode, which is its {@link #startTick},
    # 	 * {@link #startTime}, {@link #keySignature}, {@link #timeSignature}, and {@link #tempo},
    # 	 * all within braces.
    # 	 *
    # 	 * @return The String representation of this TimeTrackerNode.
    # 	 */

    def __str__(self):
        sb = "{Tick=" + str(self.__startTick) + " Time=" + str(self.__startTime) + " " + str(
            self.getKeySignature()) + " " + str(self.getTimeSignature()) + " " + str(self.getTempo()) + "}"
        return str(sb)

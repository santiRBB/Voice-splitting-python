# /**
#  * A <code>TimeTracker</code> is able to interpret MIDI tempo, key, and time signature change events and keep track
#  * of the song timing in seconds, instead of just using ticks as MIDI events do. It does this by using
#  * a LinkedList of {@link TimeTrackerNode} objects.
#  *
#  * @author Santiago Martín Cortés - 30 Nov, 2021
#  * @version 1.0
#  * @since 1.0
#  */


from timetrackernode import TimeTrackerNode
from timesignature import TimeSignature
from keysignature import KeySignature
from tempo import Tempo

class TimeTracker:
    def __init__(self):
        self.__PPQ = 0  # Pulses (ticks) per Quarter note, as in the current Midi song's header.
        self.__nodes = None # LinkedList of TimeTrackerNode objects.
        self.__lastTick = 0 # The last tick for any event in this song, initially 0.
        self.__nodes = []   # The LinkedList of TimeTrackerNodes of this TimeTracker, ordered by start time.
        self.__nodes.append(TimeTrackerNode(None, 0, self.__PPQ))   # The first node is always the start of the song.

    #     /**
    #      * A {@link TimeSignature} event was detected. Deal with it.
    #      *
    #      * @param event The event.
    #      * @param mm The message from the event.
    #      */

    def addTimeSignatureChange(self, event, tick):
        ts = TimeSignature()
        ts.set_fields(event)
        if not ts is self.__nodes[-1].getTimeSignature():
            self.__nodes.append(TimeTrackerNode(self.__nodes[-1], tick, self.__PPQ))
            self.__nodes[-1].setTimeSignature(ts)

    #     /**
    #      * A {@link Tempo} event was detected. Deal with it.
    #      *
    #      * @param event The event.
    #      * @param mm The message from the event.
    #      */

    def addTempoChange(self, event, tick):
        t = Tempo()
        t.set_fields(event)
        if not t is self.__nodes[-1].getTempo():
            self.__nodes.append(TimeTrackerNode(self.__nodes[-1], tick, self.__PPQ))
            self.__nodes[-1].setTempo(t)

    #     /**
    #      * A {@link KeySignature} event was detected. Deal with it.
    #      *
    #      * @param event The event.
    #      * @param mm The message from the event.
    #      */

    def addKeySignatureChange(self, event, tick):
        ks = KeySignature()
        ks.set_fields(event)
        if not ks is self.__nodes[-1].getKeySignature():
            self.__nodes.append(TimeTrackerNode(self.__nodes[-1], tick, self.__PPQ))
            self.__nodes[-1].setKeySignature(ks)

    #     /**
    #      * Returns the time in microseconds of a given tick number.
    #      *
    #      * @param tick The tick number to calculate the time of
    #      * @return The time of the given tick number, measured in microseconds since the most recent epoch.
    #      */

    def getTimeAtTick(self, tick):
        return self.__getNodeAtTick(tick).get_time_at_tick(tick, self.__PPQ)

    #     /**
    #      * Get the {@link TimeTrackerNode} which is valid at the given tick.
    #      *
    #      * @param tick The tick.
    #      * @return The valid TimeTrackerNode.
    #      */

    def __getNodeAtTick(self, tick):
        i = 1
        node = self.__nodes[0]
        while i<len(self.__nodes):
            node = self.__nodes[i]
            if node.getStartTick() > tick:
                i = i-1
                return i
            i = i+1
        return node

    #     /**
    #      * Get the TimeTrackerNode which is valid at the given time.
    #      *
    #      * @param time The time.
    #      * @return The valid TimeTrackerNode.
    #      */

    def __getNodeAtTime(self, time):
        i = 1
        node = self.__nodes[0]
        while i < len(self.__nodes):
            node = self.__nodes[i]
            if node.getStartTime() > time:
                i = i - 1
                return i
            i = i + 1
        return node

    #     /**
    #      * Get a list of the {@link TimeTrackerNode}s tracked by this object.
    #      *
    #      * @return {@link #nodes}
    #      */

    def getNodes(self):
        return self.__nodes

    #     /**
    #      * Set the last tick for this song to the given value.
    #      *
    #      * @param lastTick {@link #lastTick}
    #      */

    def setLastTick(self, lastTick):
        self.__lastTick = lastTick

    #     /**
    #      * Get the last tick for this song.
    #      *
    #      * @return {@link #lastTick}
    #      */

    def getLastTick(self):
        return self.__lastTick

    #     /**
    #      * Set the PPQ for this TimeTracker.
    #      *
    #      * @param ppq {@link #PPQ}
    #      */

    def setPPQ(self, ppq):
        self.__PPQ = ppq

    #     /**
    #      * Get the PPQ of this TimeTracker.
    #      *
    #      * @return {@link #PPQ}
    #      */

    def getPPQ(self):
        return self.__PPQ

    #     /**
    #      * Get the String representation of this object, which is exactly {@link #nodes}.
    #      *
    #      * @return The String representation of this object.
    #      */

    def __str__(self):
        return str(self.__nodes)

from noteeventparser import NoteEventParser
from midinote import MidiNote

class NoteListGenerator(NoteEventParser):
    def __init__(self, timeTracker):
        self.__activeNotes = []
        self.__completedNotes = []
        self.timeTracker = None

        self.__activeNotes = []
        self.__completedNotes = []

        self.timeTracker = timeTracker

    def noteOn(self, key, velocity, tick, channel):
        time = self.timeTracker.getTimeAtTick(tick)
        note = MidiNote(key, velocity, time, tick, channel, -1)
        self.__activeNotes.append(note)
        return note

    def noteOff(self, key, tick, channel):
        time = self.timeTracker.getTimeAtTick(tick)
        for note in self.__activeNotes:
            if note.getPitch() == key and note.get_correct_voice() == channel:
                self.__activeNotes.pop()
                note.close(time, tick)
                self.__completedNotes.append(note)
                return

    def getNoteList(self):
        self.__completedNotes.sort()
        return self.__completedNotes

    def getIncomingLists(self):
        incomingLists = []
        noteList = self.getNoteList()

        i = 0
        while i < len(noteList):
            incoming = set([])
            mm = []
            onsetTime = noteList[i].getOnsetTime()
            condition = True
            while condition:
                incoming.add(noteList[i])
                i += 1
                condition = i < len(noteList) and noteList[i].getOnsetTime() == onsetTime
            for t in incoming:
                mm.append(t)
            incomingLists.append(mm)
        return incomingLists

import math

from mido import MidiFile, MetaMessage


class EventParser:

    def __init__(self, midiFile, noteEventParser, timeTracker, useChannel):
        self.song = MidiFile(midiFile)
        self.noteEventParser = noteEventParser
        self.timeTracker = timeTracker
        self.timeTracker.setPPQ(self.song.ticks_per_beat)
        self.useChannel = useChannel
        self.goldStandard = list()
        self.ticks_per_beat = self.song.ticks_per_beat

    def run(self):
        lastTick = 0
        calculate_tick = 0
        for trackNum in range(len(self.song.tracks)):
            note_on_tick = 0
            note_off_tick = 0
            track = self.song.tracks[trackNum]
            lastTick = max(calculate_tick, lastTick)
            for i in range(len(track)):
                event = track[i]
                if isinstance(event, MetaMessage):
                    calculate_tick = 0
                    if event.type == 'set_tempo':
                        self.timeTracker.addTempoChange(event, 0)
                    elif event.type == 'time_signature':
                        self.timeTracker.addTimeSignatureChange(event, 0)
                    elif event.type == 'key_signature':
                        self.timeTracker.addKeySignatureChange(event, 0)
                elif event.type == 'note_on':
                    key = event.note
                    velocity = event.velocity
                    channel = event.bytes()[0] & 0x0f
                    correctVoice = channel if self.useChannel else trackNum
                    note_on_tick = note_off_tick
                    if velocity!=0:
                        note = self.noteEventParser.noteOn(key, velocity, note_on_tick, correctVoice)
                        while len(self.goldStandard) <= correctVoice:
                            self.goldStandard.append(list())
                        self.goldStandard.__getitem__(correctVoice).append(note)
                    calculate_tick = calculate_tick + int(event.time)
                elif event.type == 'note_off':
                    if event.time != 0:
                        note_off_tick = note_off_tick + event.time
                    else:
                        note_off_tick = note_off_tick + self.song.ticks_per_beat
                    self.noteEventParser.noteOff(event.note, note_off_tick, correctVoice)
                    calculate_tick = calculate_tick + int(event.time)
                else:
                    calculate_tick = calculate_tick + int(event.time)

        for gS in range(len(self.goldStandard)):
            self.goldStandard.sort()
        self.timeTracker.setLastTick(lastTick)
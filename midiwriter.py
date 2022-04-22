import random

from mido import MetaMessage, MidiFile, MidiTrack, Message


class MidiWriter:

    def __init__(self, outFile, timeTracker):
        self.outFile = outFile
        self.timeTracker = timeTracker
        self.sequence = MidiFile()
        self.initial_track = MidiTrack()
        self.sequence.tracks.append(self.initial_track)
        self.sequence.ticks_per_beat = timeTracker.getPPQ()
        self.writeTimeTracker()

    def writeTimeTracker(self):
        nodes = self.timeTracker.getNodes()

        i = 1
        node = nodes[0]
        while i < len(nodes):
            if nodes[i].getStartTime() != node.getStartTime():
                break
            i += 1

        tick = node.getStartTick()
        self.writeKeySignature(node.getKeySignature(), tick)
        self.writeTimeSignature(node.getTimeSignature(), tick)
        self.writeTempo(node.getTempo(), tick)
        while i < len(nodes):
            prev = node
            node = nodes[i]
            while i < len(nodes) and nodes[i].getStartTime() == node.getStartTime():
                node = nodes[i]
                i += 1
            tick = node.getStartTick()

            if node.getKeySignature() != prev.getKeySignature():
                self.writeKeySignature(node.getKeySignature(), tick)

            if node.getTimeSignature() != prev.getTimeSignature():
                self.writeTimeSignature(node.getTimeSignature(), tick)

            if node.getTempo() != prev.getTemp():
                self.writeTempo(node.getTempo(), tick)
            i += 1

    def writeKeySignature(self, keySignature, tick):
        metaMsg = MetaMessage('key_signature', key=keySignature.get_key(), time=keySignature.get_time())
        self.sequence.tracks[0].append(metaMsg)

    def writeTimeSignature(self, timeSignature, tick):
        metaMsg = MetaMessage('time_signature', denominator=timeSignature.getDenominator(),
                              numerator=timeSignature.getNumerator(),
                              notated_32nd_notes_per_beat=timeSignature.getNotes32PerQuarter(),
                              time=timeSignature.getMetronomeTicksPerBeat())
        self.sequence.tracks[0].append(metaMsg)

    def writeTempo(self, tempo, tick):
        metaMsg = MetaMessage('set_tempo', tempo=tempo.getMicroSecondsPerQuarter(), time=tick)
        self.sequence.tracks[0].append(metaMsg)


    # Add the given MidiNote into the sequence.
    # Params: note – The note to add.
    def add_midi_note(self, note):
        correctVoice = note.get_correct_voice()

        # Pad with enough tracks
        while len(self.sequence.tracks) <= correctVoice:
            self.sequence.tracks.append(MidiTrack())

        # Get the correct track
        track = self.sequence.tracks[correctVoice]

        noteOn = Message('note_on', note=note.getPitch(), velocity=note.getVelocity(), time=note.getOnsetTick())
        noteOff = Message('note_off', note=note.getPitch(), velocity=0, time=note.getOffsetTick())
        print(note.getPitch())
        track.append(noteOn)
        track.append(noteOff)
        # for i in range(1, 50):
        #     while len(self.sequence.tracks) <= correctVoice:
        #         self.sequence.tracks.append(MidiTrack())
        #     track = self.sequence.tracks[correctVoice]
        #     note_n = random.randint(1, 10)
        #     noteOn = Message('note_on', note=note_n + note.getPitch(), velocity=note.getVelocity(),
        #                      time=note.getOnsetTick())
        #     noteOff = Message('note_off', note=note_n + note.getPitch(), velocity=0, time=note.getOffsetTick())
        #     track.append(noteOn)
        #     track.append(noteOff)
        # self.sequence.tracks.append(track)


    # Actually write the data out to file.
    def write(self):
        self.sequence.save(self.outFile)

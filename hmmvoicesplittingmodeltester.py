# /**
#  * An <code>HmmVoiceSplittingModelTester</code> contains the {@link #main(String[])} method used
#  * to train and test the {@link HmmVoiceSplittingModel} class from the command line.
#  * <p>
#  * It can run multiple threads (total number according to {@link #NUM_PROCS}) simultaneously, managing
#  * return values and reporting the best setting for {@link HmmVoiceSplittingModelParameters}.
#  * <p>
#  * This was the class used to perform training for the paper.
#  *
#  * @author Santiago Martín Cortés - 15 April, 2022
#  * @version 1.0
#  * @since 1.0
#  */

import math
import multiprocessing
import os.path
import sys
from decimal import Decimal

from eventparser import EventParser
from hmmvoicesplittingmodel import HmmVoiceSplittingModel
from hmmvoicesplittingmodelparameters import HmmVoiceSplittingModelParameters
from hmmvoicesplittingmodelreturn import HmmVoiceSplittingModelTesterReturn
from midiwriter import MidiWriter
from notelistgenerator import NoteListGenerator
from timetracker import TimeTracker


class HmmVoiceSplittingModelTester:

    def __init__(self):
        pass

    def __init__(self):
        self.__parametersList = None
        self.NUM_PROCS = multiprocessing.cpu_count()
        self.files = []
        self.songs = []
        self.goldStandard = []
        self.tts = []
        self.MAX_VOICES = sys.maxsize
        self.USE_CHANNEL = True
        self.VERBOSE = False
        self.EPSILON = 0.000000001

    def set_params(self, params):
        self.__parametersList = params

    def start(self):
        tune = False
        run = False
        extract = False
        dir = None
        live = False

        BS = HmmVoiceSplittingModelParameters.BEAM_SIZE_DEFAULT
        NVP = HmmVoiceSplittingModelParameters.NEW_VOICE_PROBABILITY_DEFAULT
        PHL = HmmVoiceSplittingModelParameters.PITCH_HISTORY_LENGTH_DEFAULT
        GSM = HmmVoiceSplittingModelParameters.GAP_STD_MICROS_DEFAULT
        PS = HmmVoiceSplittingModelParameters.PITCH_STD_DEFAULT
        MGS = HmmVoiceSplittingModelParameters.MIN_GAP_SCORE_DEFAULT

        steps = 5

        args = sys.argv
        i = 1
        while i < len(args):
            if args[i][0] != '-' and len(args[i]) > 1:
                if not os.path.exists(args[i]):
                    print("Error: File not found: " + args[i])
                    sys.exit(1)
                else:
                    for f in os.listdir('./' + args[i]):
                        self.files.append('./' + args[i] + '/' + f)
            else:
                if len(args[i]) == 1:
                    self.argumentError(args[i])
                if args[i][1] == 'T':
                    self.USE_CHANNEL = False
                elif args[i][1] == 'l':
                    live = True
                elif args[i][1] == 'w':
                    try:
                        i = i + 1
                        dir = args[i]
                    except:
                        self.argumentError("-w requires a directory to be given")
                elif args[i][1] == 'v':
                    self.VERBOSE = True
                elif args[i][1] == 't':
                    tune = True
                    try:
                        i = i + 1
                        steps = int(args[i])
                    except Exception as e:
                        i = i - 1
                elif args[i][1] == 'r':
                    run = True
                elif args[i][1] == 'e':
                    extract = True
                elif args[i][1] == 'b':
                    try:
                        i = i + 1
                        BS = int(args[i])
                    except Exception:
                        self.argumentError("-b")
                elif args[i][1] == 'n':
                    try:
                        i = i + 1
                        NVP = Decimal(args[i])
                    except Exception:
                        self.argumentError(args[i][1])
                elif args[i][1] == 'h':
                    try:
                        i = i + 1
                        PHL = int(args[i])
                    except Exception:
                        self.argumentError("-h")
                elif args[i][1] == 'g':
                    try:
                        i = i + 1
                        GSM = Decimal(args[i])
                    except Exception:
                        self.argumentError("-g")
                elif args[i][1] == 'p':
                    try:
                        i += 1
                        PS = Decimal(args[i])
                    except Exception:
                        self.argumentError("-p")
                elif args[i][1] == 'm':
                    try:
                        i += 1
                        MGS = Decimal(args[i])
                    except Exception:
                        self.argumentError("-m")
                elif args[i][1] == 'M':
                    try:
                        i += 1
                        global MAX_VOICES
                        MAX_VOICES = int(args[i])
                    except Exception:
                        self.argumentError("-M")
                else:
                    self.argumentError(args[i])
            i += 1
        self.getSongs(self.files)

        if live:
            params = HmmVoiceSplittingModelParameters()
            params.set_defaults()
        else:
            params = HmmVoiceSplittingModelParameters()
            params.set_fields(BS, NVP, PHL, GSM, PS, MGS)

        if tune:
            best = self.tune(steps)
            if best is None:
                params = best

        if run or extract or dir is not None:
            result = self.runTest(params, extract, dir)

            if run:
                print(result)

        if not tune and not run and not extract and dir is None:
            self.argumentError("Neither -t, -r, -w, nor -e selected")

    # /**
    #  * Tune the {@link HmmVoiceSplittingModelParameters}.
    #  *
    #  * @param steps The number of steps to make in our grid search.
    #  * @return The best {@link HmmVoiceSplittingModelParameters} we found.
    #  *
    #  * @throws ExecutionException If there is some generic execution exception.
    #  * @throws InterruptedException If there is some interrupt received.
    #  */

    def tune(self, steps):
        bsMin = 10
        bsMax = 11
        nvpMin = 1E-9
        nvpMax = 1.0E-7
        phlMin = 5
        phlMax = 10
        gsmMin = 30000
        gsmMax = 1000000
        psMin = 4
        psMax = 9
        mgsMin = 1.0E-6
        mgsMax = 1.0E-4
        steps = max(1, steps)
        bsStep = max((bsMax - bsMin) / steps, 1)
        nvpStep = (nvpMax - nvpMin) / steps
        phlStep = max((phlMax - phlMin) / steps, 1)
        gsmStep = (gsmMax - gsmMin) / steps
        psStep = max((psMax - psMin) / steps, 0.5)
        mgsStep = (mgsMax - mgsMin) / steps

        testList = []
        NVP = nvpMin
        while nvpMax - NVP > self.EPSILON:
            PHL = phlMin
            while phlMax - PHL > self.EPSILON:
                GSM = gsmMin
                while gsmMax - GSM > self.EPSILON:
                    PS = psMin
                    while psMax - PS > self.EPSILON:
                        MGS = mgsMin
                        while mgsMax - MGS > self.EPSILON:
                            BS = bsMin
                            while bsMax - BS > self.EPSILON:
                                temp_param = HmmVoiceSplittingModelParameters()
                                temp_param.set_fields(int(round(BS)), NVP, int(round(PHL)), GSM, PS, MGS)
                                testList.append(temp_param)
                                BS += bsStep
                            MGS += mgsStep
                        PS += psStep
                    GSM += gsmStep
                PHL += phlStep
            NVP += nvpStep

        temp_param = HmmVoiceSplittingModelParameters()
        temp_param.set_fields(int(round(BS)), NVP, int(round(PHL)), GSM, PS, MGS)
        best = HmmVoiceSplittingModelTesterReturn()
        best.set_defaults()
        testerRun = self.runTest(temp_param, False, None)
        if testerRun.getF1() > best.getF1():
            best = testerRun
        print(testerRun)

    def call(self, paramList):
        best = HmmVoiceSplittingModelTesterReturn()
        best.set_defaults()
        for param in paramList:
            result = self.runTest(param, False, None)
            if result.getF1() > best.getF1():
                best = result
        return best

    def runTest(self, params, extract, dir):
        voiceAccSum = 0
        recall = 0
        precision = 0
        songIndex = -1
        tempIndex = songIndex
        for nlg in self.songs:
            tempIndex = tempIndex + 1
            gs = self.goldStandard[tempIndex]
            if self.VERBOSE:
                print(os.path.abspath(self.files[tempIndex]))
            voiceCount = set([])
            for note in nlg.getNoteList():
                voiceCount.add(note.get_correct_voice())
            voiceAccSongSum = 0
            vs = HmmVoiceSplittingModel(params)
            self.performInference(vs, nlg)
            if not vs.get_hypotheses():
                print('Error: No result found.')
                sys.exit(1)
            if self.MAX_VOICES != sys.maxsize:
                print('Try with a larger -M. It is possible that there are too many simultaneous notes.')
                sys.exit(1)
                continue

            # voices = []
            voices = vs.get_hypotheses()[0].getVoices()
            if extract:
                self.getExtractString(voices, tempIndex)

            songTruePositives = 0
            songFalsePositives = 0
            songNoteCount = 0

            for i in range(len(vs.get_hypotheses())):
                for voice in vs.get_hypotheses()[i].getVoices():
                    if voice:
                        voiceNumNotes = voice.get_num_notes()
                        voiceCorrect = voice.getNumNotesCorrect()
                        voiceTruePositives = voice.getNumLinksCorrect(gs)
                        voiceFalsePositives = voiceNumNotes - voiceTruePositives - 1
                        songNoteCount += voiceNumNotes
                        voiceAccSongSum += float(voiceCorrect) / float(voiceNumNotes)
                        songTruePositives += voiceTruePositives
                        songFalsePositives += voiceFalsePositives
                        if self.VERBOSE:
                            print(str(voiceCorrect) + '/' + str(voiceNumNotes) + '=' + str(voiceAccSongSum))

            songFalseNegatives = songNoteCount - len(voiceCount) - songTruePositives

            if len(voices) != 0:
                voiceAccSum += float(voiceAccSongSum) / float(len(voices))

            if songTruePositives != 0 and songFalsePositives != 0:
                precision += (float(songTruePositives)) / float((songTruePositives + songFalsePositives))

            if songTruePositives != 0 and songFalseNegatives != 0:
                recall += (float(songTruePositives)) / float((songTruePositives + songFalseNegatives))

            if self.VERBOSE:
                print("P=" + str(((float(songTruePositives)) / float((songTruePositives + songFalsePositives)))))
                print("R=" + str(((float(songTruePositives)) / float((songTruePositives + songFalseNegatives)))))
                print("F1=" + str((2 * (float(songTruePositives)) / (
                        2 * songTruePositives + songFalseNegatives + songFalsePositives))))

            if dir is not None:
                if not os.path.exists(dir):
                    os.makedirs(dir)
                fName = os.path.basename(self.files[tempIndex])
                fileName = dir + '//' + fName
                writer = MidiWriter(fileName, self.tts[songIndex])

                for voice in voices:
                    for midiNode in voice.get_notes():
                        writer.add_midi_note(midiNode)
                writer.write()
                print('Output successfully written to ' + dir)

        if self.songs:
            voiceC = float(voiceAccSum) / float(len(self.songs))
            recall /= float(len(self.songs))
            precision /= float(len(self.songs))
        else:
            voiceC = math.nan
            precision = math.nan
            recall = math.nan
        returns_field = HmmVoiceSplittingModelTesterReturn()
        returns_field.set_fields(params, voiceC, precision, recall)
        return returns_field

    # /**
    # * Get the extracted voices as a String.
    # *
    # * @param voices The voices returned from voice separation.
    # * @param songId The index of the song. Used to disambiguate in case multiple songs are being split at once.
    # *
    # * @return The print out of the extracted voices in the following format:
    # *         songID noteID voiceID onsetTime(microseconds) offsetTime(microseconds) pitch velocity
    # */

    def getExtractString(self, voices, songId):
        for i in range(len(voices)):
            if voices[i].get_notes() is not None:
                note = voices[i].get_notes()[0]
                if note is not None:
                    t = i + 1
                    print(str(songId) + ' ' + str(t) + ' ' + str(note.getOnsetTime()) + ' ' + str(
                        note.getOffsetTime()) + ' ' + str(note.getPitch()) + ' ' + str(note.getVelocity()))

    # /**
    # * Return if the voices are finished printing or not.
    # *
    # * @param voices A List of the voices.
    # * @param voiceIndex The current index of the note we need to print next for each voice.
    # * @return True if there are no notes left to print. False otherwise.
    # */

    def finished(self, voices, voiceIndex):
        for i in range(voices):
            if voices[i].get_num_notes() != voiceIndex[i]:
                return False
        return True

    # /**
    # * Return the index of the voice containing the unprinted note with the lowest onset time.
    # *
    # * @param voices A List of the voices.
    # * @param voiceIndex The current index of the note we need to print next for each voice.
    # * @return The voice containing the unprinted note with the lowest onset time.
    # */

    def getNextVoiceIndex(self, voices, voiceIndex):
        index = -1
        onsetTime = -1

        for i in range(len(voices)):
            if voices[i].get_num_notes() != voiceIndex[i]:
                note = voices[i].get_notes()[voiceIndex[i]]
                if index == -1 or note.getOnsetTime() < onsetTime:
                    index = i
                    onsetTime = note.getOnsetTime()

        return index

    # /**
    # * Perform inference on the given model.
    # *
    # * @param model The model on which we want to perform inference.
    # * @param nlg The NoteListGenerator which will give us the incoming note lists.
    # */

    def performInference(self, model, nlg):
        for incoming in nlg.getIncomingLists():
            ls = []
            for t in incoming:
                ls.append(t)
            model.handle_incoming(ls)

    # /**
    # * Print an argument error to stderr.
    # *
    # * @param arg The argument which caused the error.
    # */

    def argumentError(self, arg):
        print("VoiceSplittingTester: Argument error: ")
        print(arg)
        print("Usage: ARGS Files")
        print("RUNNING:")
        print("-t [STEPS] = Train, and optionally set the number of steps to make within each parameter range")
        print(" to an Integer value (default = 5)")
        print("-r = Run voice splitting.")
        print("-w DIR = Write out results of voice splitting to MIDI files, separating voices by channel and track.")
        print(" The files will be saved in the DIR directory.")
        print("-e = Extract the separated voices in the following format: songID noteID voiceID onsetTime(microseconds)"
              " offsetTime(microseconds) pitch velocity")
        print("-v = Verbose (print out each song and each individual voice when running)")
        print("-T = Use tracks as correct voice (instead of channels)")
        print("Note that either -t, -r, or -e is required for the program to run.")
        print("PARAMETERS (with -r):")
        print("-b INT = Set the Beam Size parameter to the value INT (defualt = " + str(
            HmmVoiceSplittingModelParameters.BEAM_SIZE_DEFAULT) + ")")
        print("-n DOUBLE = Set the New Voice Probability parameter to the value DOUBLE(defualt = " + str(
            HmmVoiceSplittingModelParameters.NEW_VOICE_PROBABILITY_DEFAULT) + ")")
        print("-h INT = Set the Pitch History Length parameter to the value INT(defualt = " + str(
            HmmVoiceSplittingModelParameters.PITCH_HISTORY_LENGTH_DEFAULT) + ")")
        print("-g DOUBLE = Set the Gap Std Micros parameter to the value DOUBLE(defualt = " + str(
            HmmVoiceSplittingModelParameters.GAP_STD_MICROS_DEFAULT) + ")")
        print("-p DOUBLE = Set the Pitch Std parameter to the value DOUBLE(defualt = " + str(
            HmmVoiceSplittingModelParameters.PITCH_STD_DEFAULT) + ")")
        print("-m DOUBLE = Set the Min Gap Score parameter to the value DOUBLE(defualt = " + str(
            HmmVoiceSplittingModelParameters.MIN_GAP_SCORE_DEFAULT) + ")")
        print(
            "-M INT = Set the maximum number of voices (default = Unlimited). Helps speed up processing in some cases.")
        sys.exit(1)

    # /**
    # * Generate a {@link NoteListGenerator}s for each given MIDI File and return them in a List.
    # *
    # * @param files A List of Files to read (should be MIDI files).
    # * @return A List of the {@link NoteListGenerator}s for each song.
    # * @throws IOException If there was some I/O error in reading one of the Files.
    # * @throws InvalidMidiDataException If one of the Files is not in proper MIDI format.
    # */

    def getSongs(self, files):
        for f in files:
            tt = TimeTracker()
            nlg = NoteListGenerator(tt)
            ep = EventParser(f, nlg, tt, self.USE_CHANNEL)
            ep.run()
            self.songs.append(nlg)
            self.tts.append(tt)
            self.goldStandard.append(ep.goldStandard)
        return self.songs


if __name__ == '__main__':
    hmm = HmmVoiceSplittingModelTester()
    hmm.start()

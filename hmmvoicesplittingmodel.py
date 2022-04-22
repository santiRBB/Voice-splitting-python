import bisect

from voicesplittingmodel import VoiceSplittingModel
from hmmvoicesplittingmodelstate import HmmVoiceSplittingModelState
import time



class HmmVoiceSplittingModel(VoiceSplittingModel):

    def __init__(self, params):
        self.__hypothesisStates = None
        self.__params = None
        self.__params = params
        self.__hypothesisStates = []
        state = HmmVoiceSplittingModelState()
        state.set_fields(0,[],params)
        bisect.insort(self.__hypothesisStates,state)

    def get_hypotheses(self):
        return self.__hypothesisStates

    def handle_incoming(self, notes):
        if len(self.__hypothesisStates)>10:
            return
        newStates = []
        for state in self.__hypothesisStates:
            returned_notes = state.handle_incoming(notes)
            for temp in returned_notes:
                bisect.insort(newStates, temp)
        self.__hypothesisStates = newStates

    def getF1(self, goldStandard):
        if self.__hypothesisStates is None or len(self.__hypothesisStates)==0:
            return 0.0

        voices = self.__hypothesisStates[0].getVoices()

        totalPositives = 0
        truePositives = 0
        falsePositives = 0
        falseNegatives = 0

        for goldVoice in goldStandard:
            if len(goldVoice) != 0:
                totalPositives += len(goldVoice) - 1

        for voice in voices:
            voiceTruePositives = voice.getNumLinksCorrect(goldStandard)
            voiceFalsePositives = voice.get_num_notes() - 1 - voiceTruePositives

            truePositives += voiceTruePositives
            falsePositives += voiceFalsePositives

        falseNegatives = totalPositives - truePositives

        precision = (float(truePositives)) / (truePositives + falsePositives)
        recall = (float(truePositives)) / (truePositives + falseNegatives)

        f1 = 2 * precision * recall / (precision + recall)

        return f1

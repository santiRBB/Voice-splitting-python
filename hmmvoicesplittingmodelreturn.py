import math

class HmmVoiceSplittingModelTesterReturn:

    def _initialize_instance_fields(self):
        self.__parameters = None
        self.__voiceConsistency = 0
        self.__precision = 0
        self.__recall = 0

    def __init__(self):
        self._initialize_instance_fields()

    def set_fields(self,params, voiceC, prec, rec):
        self.__parameters = params
        self.__voiceConsistency = voiceC
        self.__precision = prec
        self.__recall = rec

    def set_defaults(self):
        self.__parameters = None
        self.__voiceConsistency = -float('inf')
        self.__precision = -float('inf')
        self.__recall = -float('inf')

    def getParameters(self):
        return self.__parameters

    def getVoiceConsistency(self):
        return self.__voiceConsistency

    def getPrecision(self):
        return self.__precision

    def getRecall(self):
        return self.__recall

    def getF1(self):
        if self.__precision !=0 and self.__recall != 0:
            return -float('inf') if self.__precision == -float('inf') else 2 * self.__precision * self.__recall / (self.__precision + self.__recall)
        return -float('inf')

    def setParams(self, params):
        self.__parameters = params

    def setVoiceConsistency(self, voiceC):
        self.__voiceConsistency = voiceC

    def setPrecision(self, prec):
        self.__precision = prec

    def setRecall(self, rec):
        self.__recall = rec

    def __str__(self):
        return str(self.__parameters) + " = V=" + str(self.__voiceConsistency) + " P=" + str(self.__precision) + " R=" + str(self.__recall) + " F1=" + str(str(self.getF1()))

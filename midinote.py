class MidiNote:

    def __init__(self, key, velocity, onsetTime, onsetTick, correctVoice, guessedVoice):
        self.__correctVoice = 0
        self.__onsetTime = 0
        self.__onsetTick = 0
        self.__offsetTime = 0
        self.__offsetTick = 0
        self.__velocity = 0
        self.__pitch = 0
        self.__guessedVoice = 0

        self.__pitch = key
        self.__velocity = velocity
        self.__onsetTime = onsetTime
        self.__onsetTick = onsetTick
        self.__correctVoice = correctVoice
        self.__offsetTime = 0
        self.__offsetTick = 0
        self.__guessedVoice = guessedVoice

    def setOffset(self, offsetTime, offsetTick):
        self.__offsetTime = offsetTime
        self.__offsetTick = offsetTick

    def isActive(self):
        return self.__offsetTime == 0

    def close(self, offsetTime, offsetTick):
        self.setOffset(offsetTime, offsetTick)

    def overlaps(self, other):
        if other is None:
            return False
        if self.__pitch == other.__pitch:
            if self.__onsetTick < other.__offsetTick and self.__offsetTick > other.__onsetTick:
                return True
            elif other.__onsetTick < self.__onsetTick and other.__offsetTick > self.__offsetTick:
                return True
        return False

    def getOnsetTime(self):
        return self.__onsetTime

    def getOnsetTick(self):
        return self.__onsetTick

    def getOffsetTime(self):
        return self.__offsetTime

    def getOffsetTick(self):
        return self.__offsetTick

    def getDurationTime(self):
        return self.__offsetTime - self.__onsetTime

    def getPitch(self):
        return self.__pitch

    def getVelocity(self):
        return self.__velocity

    def get_correct_voice(self):
        return self.__correctVoice

    def set_correct_voice(self, correctVoice):
        self.__correctVoice = correctVoice

    def set_guessed_voice(self, voice):
        self.__guessedVoice = voice

    def get_guessed_voice(self):
        return self.__guessedVoice

    def __str__(self):
        # return 's'
        return "(K:{0:d}  V:{1:d}  [{2:d}-{3:d}] {4:d})".format(self.__pitch, self.__velocity, self.__onsetTick,
                                                                self.__offsetTick, self.__correctVoice)

    def __lt__(self, other):
        return (self.__onsetTick, self.__offsetTick, self.__pitch, self.__velocity, self.__correctVoice,
                self.__guessedVoice) < (
               other.__onsetTick, other.__offsetTick, other.__pitch, other.__velocity, other.__correctVoice,
               other.__guessedVoice)


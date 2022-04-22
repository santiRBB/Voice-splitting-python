class HmmVoiceSplittingModelParameters:

    def _initialize_instance_fields(self):
        self.MIN_GAP_SCORE = 0
        self.PITCH_STD = 0
        self.GAP_STD_MICROS = 0
        self.PITCH_HISTORY_LENGTH = 0
        self.NEW_VOICE_PROBABILITY = 0
        self.BEAM_SIZE = 0


    MIN_GAP_SCORE_DEFAULT = 8E-4
    PITCH_STD_DEFAULT = 4
    GAP_STD_MICROS_DEFAULT = 127000
    PITCH_HISTORY_LENGTH_DEFAULT = 6
    NEW_VOICE_PROBABILITY_DEFAULT = 1E-9
    BEAM_SIZE_DEFAULT = 25

    def __init__(self):
        self._initialize_instance_fields()


    def set_fields(self, BS, NVP, PHL, GSM, PS, MGS):
        self._initialize_instance_fields()
        self.BEAM_SIZE = BS
        self.NEW_VOICE_PROBABILITY = NVP
        self.PITCH_HISTORY_LENGTH = PHL
        self.GAP_STD_MICROS = GSM
        self.PITCH_STD = PS
        self.MIN_GAP_SCORE = MGS

    def set_defaults(self):
        self.BEAM_SIZE = self.BEAM_SIZE_DEFAULT
        self.NEW_VOICE_PROBABILITY = self.NEW_VOICE_PROBABILITY_DEFAULT
        self.PITCH_HISTORY_LENGTH = self.PITCH_HISTORY_LENGTH_DEFAULT
        self.GAP_STD_MICROS = self.GAP_STD_MICROS_DEFAULT
        self.PITCH_STD = self.PITCH_STD_DEFAULT
        self.MIN_GAP_SCORE = self.MIN_GAP_SCORE_DEFAULT

    def __eq__(self, other):
        if not(isinstance(other, HmmVoiceSplittingModelParameters)):
            return False
        p = other
        return self.BEAM_SIZE == p.BEAM_SIZE and self.NEW_VOICE_PROBABILITY == p.NEW_VOICE_PROBABILITY and self.PITCH_HISTORY_LENGTH == p.PITCH_HISTORY_LENGTH and self.GAP_STD_MICROS == p.GAP_STD_MICROS and self.PITCH_STD == p.PITCH_STD and self.MIN_GAP_SCORE == p.MIN_GAP_SCORE


    def __hash__(self):
        return self.BEAM_SIZE + hash(self.NEW_VOICE_PROBABILITY) + self.PITCH_HISTORY_LENGTH + hash(self.GAP_STD_MICROS) + hash(self.PITCH_STD) + hash(self.MIN_GAP_SCORE)

    def __str__(self):
        return "(" + str(self.BEAM_SIZE) + ',' + str(self.NEW_VOICE_PROBABILITY) +',' + str(self.PITCH_HISTORY_LENGTH)+',' +str(self.GAP_STD_MICROS)+','+str(self.PITCH_STD)+','+str(self.MIN_GAP_SCORE)+')'

    def __lt__(self, other):
        (self.BEAM_SIZE, self.MIN_GAP_SCORE, self.PITCH_STD, self.GAP_STD_MICROS, self.NEW_VOICE_PROBABILITY, self.PITCH_HISTORY_LENGTH) <  (other.BEAM_SIZE, other.MIN_GAP_SCORE, other.PITCH_STD, other.GAP_STD_MICROS, other.NEW_VOICE_PROBABILITY, other.PITCH_HISTORY_LENGTH)
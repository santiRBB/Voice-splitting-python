# /**
#  * A <code>TimeSignature</code> represents some MIDI data's metrical structure (time signature).
#  * Equality is based only on the numerator and denominator.
#  *
#  * @author Santiago Martín Cortés - 30 Nov, 2021
#  * @version 1.0
#  * @since 1.0
#  */


class TimeSignature:

    def _initialize_instance_fields(self):
        self.__numerator = 0    # The numerator of the time signature.
        self.__denominator = 0  # The denominator of the time signature.
        self.__metronomeTicksPerBeat = 0    # The number of metronome ticks per beat at this time signature.
        self.__notes32PerQuarter = 0    # The number of 32nd notes per quarter note at this time signature.

    #  Create a new default TimeSignature (4/4 nodes).
    def __init__(self):
        self._initialize_instance_fields()
        self.__numerator = 4
        self.__denominator = 4
        self.__metronomeTicksPerBeat = 24
        self.__notes32PerQuarter = 8


    def set_fields(self, event):
        self._initialize_instance_fields()
        self.__numerator = event.numerator
        self.__denominator = event.denominator
        self.__metronomeTicksPerBeat = event.time
        self.__notes32PerQuarter = event.notated_32nd_notes_per_beat

    # 	/**
    # 	 * Get the number of metronome ticks per beat.
    # 	 *
    # 	 * @return {@link #metronomeTicksPerBeat}
    # 	 */

    def getMetronomeTicksPerBeat(self):
        return self.__metronomeTicksPerBeat

    # 	/**
    # 	 * Get the number of 32nd notes per quarter note.
    # 	 *
    # 	 * @return {@link #notes32PerQuarter}
    # 	 */

    def getNotes32PerQuarter(self):
        return self.__notes32PerQuarter

    # 	/**
    # 	 * Get the number of MIDI ticks per 32nd note at this time signature.
    # 	 *
    # 	 * @param ppq The pulses per quarter note of the song.
    # 	 * @return The number of MIDI ticks per 32nd note.
    # 	 */

    def getTicksPerNote32(self, ppq):
        return int((ppq / self.__notes32PerQuarter))

    # 	/**
    # 	 * Get the number of 32nd notes per measure at this time signature.
    # 	 *
    # 	 * @return The number of 32nd notes per measure.
    # 	 */

    def getNotes32PerMeasure(self):
        return (self.__notes32PerQuarter * self.__numerator * 4 / self.__denominator)

    # 	/**
    # 	 * Get the numerator of this time signature.
    # 	 *
    # 	 * @return {@link #numerator}
    # 	 */

    def getNumerator(self):
        return self.__numerator

    # 	/**
    # 	 * Get the denominator of this time signature.
    # 	 *
    # 	 * @return {@link #denominator}
    # 	 */

    def getDenominator(self):
        return self.__denominator

    def getTime(self):
        return  self.__

    # 	/**
    #      * Get the String representation of this TimeSignature object, which is {@link #numerator} /
    #      * {@link #denominator}.
    #      *
    #      * @return The String representation of this TimeSignature object.
    #      */

    def __str__(self):
        sb = "4" + str(self.__numerator)+'/'+str(self.__denominator)
        return str(sb)

    # 	/**
    #      * Get the hash code of this TimeSignature object.
    #      *
    #      * @return The hash code of this object.
    #      */

    def __hash__(self):
        return self.getNumerator() + self.getDenominator()

    # 	/**
    # 	 * Return whether the given Object is equal to this one, which is only the case
    # 	 * when the given Object is a TimeSignature, and its {@link #numerator} and {@link #denominator}
    # 	 * fields are equal to this one's.
    # 	 *
    # 	 * @param other The object we are checking for equality.
    # 	 * @return True if the given Object is equal to this one. False otherwise.
    # 	 */

    def __eq__(self, other):
        if not(isinstance(other, TimeSignature)):
            return False
        ts = other
        return self.getDenominator() == ts.getDenominator() and self.getNumerator() == ts.getNumerator()

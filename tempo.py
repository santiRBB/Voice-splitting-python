# /**
#  * A <code>Tempo</code> object tracks the speed of MIDI data. That is, the rate at which quarter notes occur.
#  *
#  * @author Santiago Martín Cortés - 30 Nov, 2021
#  * @version 1.0
#  * @since 1.0
#  */

class Tempo:

    def _initialize_instance_fields(self):
        self.__microSecondsPerQuarter = 0
        self.__time = 0

    # 	/**
    # 	 * Create a default tempo - 120 BPM
    # 	 */

    def __init__(self):
        self._initialize_instance_fields()
        self.__microSecondsPerQuarter = 500000
        self.__time = 0

    # 	/**
    # 	 * Create a new Tempo from the given data array.
    # 	 *
    # 	 * @param event The tempo data array, grabbed directly from a MIDI file.
    # 	 */

    def set_fields(self, event):
        self._initialize_instance_fields()
        self.__microSecondsPerQuarter = event.tempo
        self.__time = event.time

    # 	/**
    # 	 * Gets the number of microseconds which pass per quarter note.
    # 	 *
    # 	 * @return {@link #microSecondsPerQuarter}
    # 	 */

    def getMicroSecondsPerQuarter(self):
        return self.__microSecondsPerQuarter


    # 	/**
    #      * Calculate the number of microseconds per quarter note based on the given data array. It is really just an int,
    #      * where the highest byte is data[0], and the lowest byte is data[3].
    #      *
    #      * @param data The Midi byte array of the tempo data for microseconds/quarter. It is actually just represented as an int,
    #      * but it is grabbed from the file as a byte array, so we need this conversion.
    #      * @return The number of microseconds per quarter note of the given data
    #      */

    # def calculateMicroSecondsPerQuarter(self, data):
    #     tpq = 0
    #     for i in len(data):
    #         byteNumber = len(data) - 1 - i
    #
    #         tpq += (0x000000ff & data[i]) << (
    #                     8 * byteNumber)  # The signed left shift operator "<<" shifts a bit pattern to the left
    #     return tpq





    #     /**
    #      * Get the String representation of this Tempo object, which is the number of quarter notes
    #      * per minute.
    #      *
    #      * @return The String representation of this Tempo object.
    #      */

    def __str__(self):
        qpm = int(60000000. / self.getMicroSecondsPerQuarter())
        sb = str(qpm) + "= QPM"  # "6" +
        return str(sb)

    #     /**
    #      * Get the hash code of this Tempo object.
    #      *
    #      * @return The hash code of this object.
    #      */
    #     @Override
    # 	public int hashCode() {
    # 		return getMicroSecondsPerQuarter();
    # 	}

    def __hash__(self):
        return self.getMicroSecondsPerQuarter()

    #     /**
    # 	 * Return whether the given Object is equal to this one, which is only the case
    # 	 * when the given Object is a Tempo, and its {@link #microSecondsPerQuarter}
    # 	 * field is equal to this one's.
    # 	 *
    # 	 * @param other The object we are checking for equality.
    # 	 * @return True if the given Object is equal to this one. False otherwise.
    # 	 */

    def __eq__(self, other):
        if not(isinstance(other, Tempo)):
            return False
        t = other
        return self.getMicroSecondsPerQuarter() == t.getMicroSecondsPerQuarter()

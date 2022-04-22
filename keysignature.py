# /**
#  * A <code>KeySignature</code> stores the key signature of a song. That is, the key (represented by the
#  * number of sharps in its signature), and whether it is major or minor.
#  *
#  * @author Santiago Martín Cortés - 30 Nov, 2021
#  * @version 1.0
#  * @since 1.0
#  */

class KeySignature:

    def _initialize_instance_fields(self):
        self.__key = None  # The key of the song
        self.__tick = None  # The tick of the key signature

    def __init__(self):
        self._initialize_instance_fields()
        self.__key = 'C'    # Default key is C
        self.__tick = 0     # Default tick is 0

    def set_fields(self, event):
        self._initialize_instance_fields()  # Initialize instance fields
        self.__key = event.key       # Set key
        self.__tick = event.time     # Set tick

    def get_key(self):
        return self.__key

    def get_time(self):
        return self.__tick

    def __str__(self):
        return str(self.__key)

    # TODO Equals method and hashcode if possible

# import math
#
#
# class KeySignature:
#
#     def _initialize_instance_fields(self):
#         self.__numSharps = 0
#         self.__major = False
#
#     def __init__(self):
#         self(bytearray([0, 0]))
#
#     def __init__(self, data):
#         self._initialize_instance_fields()
#         self.__numSharps = data[0]
#         self.__major = data[1] == 0
#
# /**
# 	 * Get the positive offset from C of the tonic note of this key.
# 	 *
# 	 * @return The number of semitones between C and the next highest instance
# 	 * of the tonic of this key, on the range [0,11]
# 	 */
#
#     def get_positive_offset_from_C(self):
#         offset = math.fmod((7 * self.__numSharps), 12)
#         if not self.is_major():
#             offset -= 3
#
#         while offset < 0:
#             offset += 12
#
#         return offset
#
# 	/**
# 	 * Get the number of sharps in this key signature.
# 	 *
# 	 * @return {@link #numSharps}
#
#     def get_num_sharps(self):
#         return self.__numSharps
# 	/**
# 	 * Return whether this key is major or not.
# 	 *
# 	 * @return {@link #major}
# 	 */
#
#     def is_major(self):
#         return self.__major
#
#     def __str__(self):
#         sb = "4"
#         if not self.is_major():
#             sb.join([self.__numSharps, 'm'])
#         else:
#             sb.join([self.__numSharps])
#         return str(sb)
#
#     def __hash__(self):
#         return self.get_positive_offset_from_C() * (-1 if self.is_major() else 1)
#
#     def __eq__(self, other):
#         if not (isinstance(other, KeySignature)):
#             return False
#         ks = other
#         return self.get_positive_offset_from_C() == ks.get_positive_offset_from_C() and self.is_major() == ks.is_major()

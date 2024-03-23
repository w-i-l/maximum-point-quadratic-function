from math import log2, ceil

class Decode:
    def __init__(self, lower_bound, upper_bound, precision):
        self.lower_bound = lower_bound
        self.upper_bound = upper_bound
        self.precision = precision

    def decode(self, binary):
        index = self.__convert_to_base_10(binary)
        return self.lower_bound + index * self.__get_discretization_step()

    def __get_bin_length(self):
        diff = self.upper_bound - self.lower_bound
        exp = 10 ** self.precision
        bits = log2(diff * exp)
        return ceil(bits)
    
    def __get_discretization_step(self):
        diff = self.upper_bound - self.lower_bound
        exp = 2 ** self.__get_bin_length()
        return diff / exp
    
    def __convert_to_base_10(self, binary):
        return int(binary, 2)

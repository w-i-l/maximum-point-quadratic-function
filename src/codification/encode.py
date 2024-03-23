from math import log2, ceil, floor

class Encode:

    def __init__(self, lower_bound, upper_bound, precision):
        self.lower_bound = lower_bound
        self.upper_bound = upper_bound            
        self.precision = precision

    def encode(self, number):
        interval_lower_bound = self.__get_interval_lower_bound(number)
        binary = self.__convert_to_binary(interval_lower_bound)
        return binary

    def __get_bin_length(self):
        diff = self.upper_bound - self.lower_bound
        exp = 10 ** self.precision
        bits = log2(diff * exp)
        return ceil(bits)
    
    def __get_discretization_step(self):
        diff = self.upper_bound - self.lower_bound
        exp = 2 ** self.__get_bin_length()
        return diff / exp
    
    def __get_interval_lower_bound(self, number):
        diff = number - self.lower_bound
        div = diff / self.__get_discretization_step()
        return floor(div)
    
    def __convert_to_binary(self, number):
        binary = bin(number)[2:]

        bits_length = self.__get_bin_length()
        if len(binary) == bits_length:
            return binary
        elif len(binary) < bits_length:
            diff = bits_length - len(binary)
            return '0' * diff + binary
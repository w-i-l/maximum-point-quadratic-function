from math import log2, ceil

class Decode:
    def __init__(
            self: object, 
            lower_bound: float,
            upper_bound: float, 
            precision: int
        ):
        self.lower_bound = lower_bound
        self.upper_bound = upper_bound
        self.precision = precision

    def decode(self: object, binary: str) -> float:
        index = self.__convert_to_base_10(binary)
        return self.lower_bound + index * self.__get_discretization_step()

    def __get_bin_length(self: object) -> int:
        diff = self.upper_bound - self.lower_bound
        exp = 10 ** self.precision
        bits = log2(diff * exp)
        return ceil(bits)
    
    def __get_discretization_step(self: object) -> float:
        diff = self.upper_bound - self.lower_bound
        exp = 2 ** self.__get_bin_length()
        return diff / exp
    
    def __convert_to_base_10(self, binary: str) -> int:
        return int(binary, 2)

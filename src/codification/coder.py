from src.codification.encode import Encode
from src.codification.decode import Decode
from src.base_class import BaseClass

class Coder():
    def __init__(
            self: object, 
            lower_bound: float,
            upper_bound: float, 
            precision: int
        ):
        self.encoder = Encode(lower_bound, upper_bound, precision)
        self.decoder = Decode(lower_bound, upper_bound, precision)
        self.lower_bound = lower_bound
        self.upper_bound = upper_bound
        self.precision = precision
    
    def set_print(self: object, should_print: bool) -> None:
        self.encoder.should_print = should_print
        self.decoder.should_print = should_print


# lower_bound = 0
# upper_bound = 1
# precision = 1
# coder = Coder(lower_bound, upper_bound, precision)
# test1 = (0.2, '0011')
# test2 = (0.5, '1000')
# test3 = ('0101', 0.3125)
# test4 = ('1111', 0.9375)

# assert coder.encode(test1[0]) == test1[1]
# assert coder.encode(test2[0]) == test2[1]
# assert coder.decode(str(test3[0])) == test3[1]
# assert coder.decode(str(test4[0])) == test4[1]
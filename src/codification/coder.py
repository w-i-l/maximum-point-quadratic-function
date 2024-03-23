from src.codification.encode import Encode
from src.codification.decode import Decode

class Coder(Encode, Decode):
    def __init__(
            self: object, 
            lower_bound: float,
            upper_bound: float, 
            precision: int
        ):
        Encode.__init__(self, lower_bound, upper_bound, precision)
        Decode.__init__(self, lower_bound, upper_bound, precision)
        print(f'Coder initialized with lower_bound={lower_bound}, upper_bound={upper_bound}, precision={precision}')
        print(f'Discretization step: {self._Encode__get_discretization_step()}')
        print(f'Binary length: {self._Encode__get_bin_length()}')

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
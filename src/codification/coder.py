from encode import Encode
from decode import Decode

class Coder(Encode, Decode):
    def __init__(self, lower_bound, upper_bound, precision):
        Encode.__init__(self, lower_bound, upper_bound, precision)
        Decode.__init__(self, lower_bound, upper_bound, precision)

lower_bound = 0
upper_bound = 1
precision = 1
coder = Coder(lower_bound, upper_bound, precision)
test1 = (0.2, '0011')
test2 = (0.5, '1000')
test3 = ('0101', 0.3125)
test4 = ('1111', 0.9375)

assert coder.encode(test1[0]) == test1[1]
assert coder.encode(test2[0]) == test2[1]
assert coder.decode(test3[1]) == test3[0]
assert coder.decode(test4[0]) == test4[1]
from src.codification.coder import Coder
from src.base_class import BaseClass

class Cromosome(BaseClass):
    __STATIC_ID = 0
    __CODER = None
    __FUNCTION = None

    @staticmethod
    def init(
            coder: Coder, 
            function: object
        ):
        Cromosome.__CODER = coder
        Cromosome.__FUNCTION = function

    def __init__(
            self: object, 
            value: float,
            binary: str, 
            fitness: float
        ):
        self.value = value
        self.binary = binary
        self.fitness = fitness
        self.id = Cromosome.__STATIC_ID
        Cromosome.__STATIC_ID += 1
        super().__init__()
    
    def __str__(self: object) -> str:
        return f'{self.id}'
    
    def __repr__(self: object) -> str:
        return f'{self.id}'
    
    def show(self: object):
        print(f'{self.id}: {self.value} x= {self.binary} f={self.fitness}')

    def update_value(self: object, value: float) -> None:
        self.value = value
        self.binary = Cromosome.__CODER.encoder.encode(value)
        self.fitness = Cromosome.__FUNCTION(value)
        if self.should_print:
            print(f'Updated value for {self.id}')
    
    def update_binary(self: object, binary: str) -> None:
        self.binary = binary
        value = Cromosome.__CODER.decoder.decode(binary)
        value = round(value, Cromosome.__CODER.precision)
        self.value = value
        self.fitness = Cromosome.__FUNCTION(self.value)
        if self.should_print:
            print(f'Updated binary for {self.id}')

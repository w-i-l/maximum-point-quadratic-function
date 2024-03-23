class Cromozom:
    __STATIC_ID = 0

    def __init__(
            self: object, 
            value: float,
            binary: str, 
            fitness: float
        ):
        self.value = value
        self.binary = binary
        self.fitness = fitness
        self.id = Cromozom.__STATIC_ID
        Cromozom.__STATIC_ID += 1
    
    def __str__(self: object) -> str:
        return f'{self.id}'
    
    def __repr__(self: object) -> str:
        return f'{self.id}'
    
    def show(self: object):
        print(f'{self.id}: {self.value} x= {self.binary} f={self.fitness}')
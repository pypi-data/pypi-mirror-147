from mygalaxy.calc import planet_mass, planet_vol

class Planet:

    # class attribute
    shape = 'round'

    # instance method
    def __init__(self, name, radius, gravity, system):
        self.name = name
        self.radius = radius
        self.gravity = gravity
        self.system = system

    # instance method
    def orbit(self):
        return f'{self.name} is orbiting in the {self.system}'

    # static method
    @staticmethod
    def spin(speed = '2000 miles per hour'):
        return f'The planet spins and spins at {speed}'

    # class method
    @classmethod
    def commons(cls):
        return f'All planets are {cls.shape} because of gravity'

    def mass(self):
        return f'The planet mass is {planet_mass(self.gravity, self.radius)}'
    
    def volume(self):
        return f'The planet volume is {planet_vol(self.radius)}'

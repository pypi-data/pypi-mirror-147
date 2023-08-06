from scipy.constants import pi, G

def planet_mass(gravity, radius):
    mass = ( gravity*radius**2 ) / G
    return mass

def planet_vol(radius):
    vol = ( 4*pi*radius**2 ) / 3
    return vol
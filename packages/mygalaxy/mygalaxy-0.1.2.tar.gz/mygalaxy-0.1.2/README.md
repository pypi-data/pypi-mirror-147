# mygalaxy 

A small galaxy to learn poetry. 

## How to install 

`pip install mygalaxy`

## How to use

### Create your planet

    from mygalaxy.planet import Planet
    earth = Planet(name='earth', radius=6371000, gravity=9.807, system='solar')
    print(earth.gravity)

### Make your planet spin 

`earth.spin()`

### Make your planet orbit

`earth.orbit()`

### Learn the shape of your planet

`earth.commons()`


### Compute the mass of your planet

`earth.mass()`


### Compute the volume of your planet 

`earth.volume()`

You may also use the mass and volume compute functions separately by doing: 

    from mygalaxy.calc import planet_mass, planet_vol
    r = 6371000
    g = 9.807
    print(planet_mass(gravity=g, radius=r))
    print(planet_vol(radius=r))

### Related URLs
* https://python-poetry.org/
* https://realpython.com/dependency-management-python-poetry/
* https://www.youtube.com/watch?v=f26nAmfJggw
* https://realpython.com/pypi-publish-python-package/
* https://www.youtube.com/watch?v=sugvnHA7ElY&t=242s
* https://stackoverflow.com/a/70027834/7762646




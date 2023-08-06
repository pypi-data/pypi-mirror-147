# Physical Quantity library for Python

This is a really simple Physical Quantity library for Python that implements basic dimensional decomposition and
operators for physical quantities. Most of the library is centered around SI units, but there is currently partial
support for non-SI units as well. 

The current release is a real early beta. 

Some examples of usage: 

```python
from physicalquantity import PhysicalQuantity as PQ

voltage = PQ(20,"miliampere") * PQ(15,"kiloohm")
print(voltage.value, voltage.unit_name, voltage.same_dimensions("milivolt"))
```

```
300.0 volt True
```

An example of the current (limited) support for non-SI units. 
```python
from physicalquantity import PhysicalQuantity as PQ

temperature = (PQ(76,"fahrenheid") + PQ(19,"celcius") / PQ(2, "one")).as_absolute("fahrenheid")
print(temperature.value, temperature.unit_name)
temperature2 = temperature.as_absolute("fahrenheid")
print(temperature2.value, temperature2.unit_name)
temperature3 = (PQ(76,"fahrenheid") - PQ(19,"celcius")).as_relative("fahrenheid")
print(temperature3.value, temperature3.unit_name)
```

```
881.8944222256 kelvin
71.10001999735194 fahrenheid
9.799960005296041 fahrenheid
```

## constructor

The PhysicalQuantity (in normal use) takes up to two arguments. The first argument (defaulting to zero) is a numeric value for the physical quantity, the second argument (defaulting to "one") is the name of the units or physical phenonemon the physical quantity refers to. This name can be prefixed with any of the metric prefixes from yotta down to yocto.

We distinguish between:

* si units
* no-name units
* transposed units
* aliasses
* prefixes

The following SI units (with aliasses) are currently defined.
* one
  * number
  * dimentionless
  * radians
  * steradian
* metre
  * meter
  * meters
  * length
  * m
* kg
  * weight
* second
  * seconds
  * sec
  * time
* ampere
  * current
  * amp
* kelvin
  * temperature
* mole
* candela
  * intencity
  * lumen
  * illuminance
* hertz
  * frequency
  * becquerel
  * hz
* newton
  * force
* pascal
  * stress
  * pressure
  * pa
* joule
  * energy
  * work
  * heat
* watt
  * power
* coulomb
  * charge
* volt
  * potential
* ohm
  * resistance
* siemens
* farad
  * capacitance
* tesla
  * fluxdensity
* weber
  * flux
* henry
  * inductance
* lux
  * illuminance
* grey
  * absorbedradiation
  * sievert
* m2
  * squaremetre
* m3
  * cubicmetre

```python
from physicalquantity import PhysicalQuantity as PQ

force1 = PQ(40, "newton")
```

Next to these SI units we have a set of nameless units for what quantities are constructed using the name of the physical phenonemon.

* velocity
* acceleration
* wavenumber
* density
* surfacedensity
* specificvolume
* currentdensity
* magneticfieldstrength
* concentration
* massconcentration
* luminance

```python
from physicalquantity import PhysicalQuantity as PQ

acc1 = PQ(9.8, "acceleration") 
```

An other set of units are the transposed and/or scaled units. Note that when quantoties of these units are used with operators, the result will get normalized to their coresponding SI units.

* degrees
* foot
  * feet
  * ft
* inch
* mile
* yard
* au
  * astronomicalunit
* lightyear
* parsec
* gram
  * g
* pound
  * pounds
  * lbs
  * lb
* ounce
  * oz
* minute
  * minutes
  * min
* hour
  * hr
* day
  * dy
* year
  * yr
* celcius
* fahrenheid
* are
* hectare
* acre
* barn
* litre
  * liter
* barrel
* gallon
* pint

```python
from physicalquantity import PhysicalQuantity as PQ

vol1 = PQ(22, "litre")   
```

Each of the units and their aliases may be prefixed with one of the metric prefixes

* yotta
* zetta
* exa
* peta
* tera
* giga
* mega
* kilo
* hecto
* deca
* deci
* centi
* mili
* micro
* nano
* pico
* femto
* atto
* zepto
* yocto

```python
from physicalquantity import PhysicalQuantity as PQ

res1 = PQ(2.4, "megaohm")   
```

# normalized

While many operations will return an SI normalized result, it is possible to do so explicitly

```
from physicalquantity import PhysicalQuantity as PQ

temperature = PQ(79, "fahrenheid").normalized()  # normalize to Kelvin
```

# as

The reverse of normalization comes in two variants. An absolute and a relative variant. 

```python
from physicalquantity import PhysicalQuantity as PQ

temperature = (PQ(76,"fahrenheid") + PQ(19,"celcius") / PQ(2, "one")).as_absolute("fahrenheid")
``` 

```python
from physicalquantity import PhysicalQuantity as PQ

temperature = (PQ(76,"fahrenheid") - PQ(19,"celcius")).as_relative("fahrenheid")
```

```python
from physicalquantity import PhysicalQuantity as PQ

distance = PQ(1,"attoparsec").as_absolute("centiinch").as_dict()

```

# dimensions check

Often you will want to check if a wuantity has the expected dimensions

```python
assert temperature.same_dimensions("temperature")
```

# operators

The following operators are supported:

* \* : multiplication
* \/ : division
* \+ : addition
* \- : subtraction
* \*\* : power 

Impossible operations will throw an RuntimeError, If the operation succeed, the result will always have a normalized value.
It is important to note that not all resulting values will have a *unit_name* value. The *dimensions* value of the PhysicalQuantity though
will always uniquely identify the units used.

```python
voltage1 = PQ(20,"miliampere") * PQ(15,"kiloohm")

voltage2 = PQ(100, "watt") / PQ(6, "ampere")

voltage3 = voltage1 - voltage2

voltage4 = (voltage1 + voltage2) / PQ(2, "one")

volume = PQ(0.15, "metre") ** 3
```

# comparison

All the comparison operators work on PhysicalQuantity objects

```python
if voltage2 > voltage1:
    ...
```

# serialization

While PhysicalQuantity has a *json* method for serializing a single PhysicalQuantity as JSON, the expected usage would be the use of a serializable PhysicalQuantity structure as part of a larger structure.

```python
import json
from physicalquantity import PhysicalQuantity as PQ

collection = {}
collections["temperature"] = PQ(94, "fahrenheit").normalized().as_dict()
collections["distance"] = PQ(1,"attoparsec").normalized().as_dict()
serialized = json.dumps(collection)
```

```python
import json
from physicalquantity import PhysicalQuantity as PQ
from physicalquantity import from_dict as pq_from_dict

collection = json.loads(serialized)
temperature = pq_from_dict(collection["temperature"])
```


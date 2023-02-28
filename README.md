# Quaternionic python: a (small) Python 3.11 resource
### Perform quaternionic arithmetic easily in Python

:dragon: Author: Samuele Ferri (@ferrixio)

:star: Version 2.1.8

📜 Check this [useful file](https://github.com/ferrixio/Quaternions/blob/main/How%20to%20assemble%20a%20quaternion.md)

===========================================================================

## TABLE OF CONTENTS 

1. Features
2. How to use
3. Known issues
4. Future ideas
5. Description
6. Changelog

===========================================================================

## 1. FEATURES

This class allows user to emulate quaternionic algebra in Python. The class can do:

	> internal and external sums
	> scalar multiplications
	> internal left-multiplications
	> internal right-multiplications
	> integer powers
	> divisions
	> floordivisions
	> modulos
	> normalizations
	> conjugations
	> inversions
	> algebric prints
	> type casting (int, float, complex)
	> random generations
	> exponential and logarithmic functions
	> dot product, cross product and commutator
	> extraction or generation from 3D rotations

I used mostly magic methods to allow users to write `x+y`, `x*y`, `x/y`, ..., directly.

I recommend reading [this file](https://github.com/ferrixio/Quaternions/blob/main/How%20to%20assemble%20a%20quaternion.md) to better understand how to construct a quaternion.

Every value below 1e-13 is treated as 0, especially during logical checks. This does NOT imply that the value is set to 0!

===========================================================================

## 2. HOW TO USE

Open the file `test_me.py` and try it, or simply copy and paste the class in the file you want to use and then import it. (Don't forget to __cite me__ if you are using this in a project!)

===========================================================================

## 3. KNOWN ISSUES

The operations +=, -=, *= and so on, don't work if on the left side there isn't a quaternion.

===========================================================================

## 4. FUTURE IDEAS

+ :o: Plotting quaternions (stereographic projection?)
+ :o: Implementing rotation of 3D objects
+ :white_check_mark: Vector representation
+ :white_check_mark: Add complex compatibility
+ :white_check_mark: Quaternionic functions
+ :white_check_mark: Floor division
+ :white_check_mark: Add @ operator
+ :warning: Create a library

Legend: :o: = solution not (yet) found, :white_check_mark: = solution found and implemented, :warning: = solution found but the implementation needs to be improved

===========================================================================

## 5. DESCRIPTION

The [quaternion number system](https://en.wikipedia.org/wiki/Quaternion) is an extended version of the complex numbers, firstly introduced by Rowan Hamilton in 1843. A quaternion is a 4-tuple of informations:
	q := a + bi + cj + dk
where a, b, c, d are real numbers, and i, j, k are the basic quaternions.

Instead of having a single imaginary part, as a complex number, quaternions have three imaginary parts, that is, there are three elements, namely i, j and k, such that
	i^2 = j^2 = k^2 = ijk = -1

Addition works componentwise and it is commutative, and so is the scalar multiplication.
The Hamilton product, that is the multiplication between two quaternions, follows the expression:

 > (a1 + b1i + c1j + d1k)*(a2 + b2i + c2j + d2k) = 
	a1a2 - b1b2 - c1c2 - d1d2
	+ (b1a2 + b1a2 + c1d2 - d1c2)i
	+ (a1c2 - b1d2 + c1a2 + d1b2)j
	+ (a1d2 + b1c2 - c1b2 + d1a1)k

and sadly it is not commutative since ij = k, ji = -k, jk = i, kj = -i, ki = j, ik = -j.

===========================================================================

## 6. CHANGELOG

### Version 2.1.8
Extended the random number generator to float numbers. Renamed `random` to `random_unit` and `randint` to `random`.

Added the variable `ACCURACY` to easily handle the floating point during logical checks. The user can edit it with the method `change_bound`.

### Version 2.1.7
Implemented some elements of 3D geometry. Added the property `rotation` which returns a tuple with the four elements of a rotation: the angle and the 3D axis. By the equivalence `3D rotation == versor quaternion`, the method automatically normalizes the quaternion if it is not unitary (and raises a warning to the user).

Added the classmethod `from_rotation()` which generates a quaternion from a rotation.

### Version 2.1.6
Corrected the // and % operations. In the real numbers, `x / y = (k, r)`, where `k = x // y` is the quotient and `r = x % y` is the reminder. Since in H this kind of operations don't exist, I move the problem in HP1 and look for two quaternions `k` and `r` such that the previous relation is fullfilled. With this method, `k` belongs to the same equivalence class of `q` in HP1, that is, it lies on the same line that starts from the origin and passes through `q`.

Added the magic method `__matmul__`: `x @ y` performs an homotethy on x to the sphere of radius y.

Fixed a little bit of floating point in `__bool__`, `__eq__` and `__str__`.

### Version 2.1.5
Added // operation. x // y performs an homotethy of x to a quaternion with norm y.
Changed the default decimals of `round()` to 3.

Added the classmethod `randint()`, that generates a random quaternion with integer values.

Fixed a bug in `random()` method.

### Version 2.1.4
Added modulo operation %.

### Version 2.1.3
Minor change: used `isinstance()` instead of `type()`.

### Version 2.1.2
Added the method `check_other` to handle with unsupported type errors in arithmetic.

### Version 2.1.1
Added geodesic distance calculator. Riarranged the code in a more understandable way. Discovered the floating point issue in random number generator.

### Version 2.1
Added dot/cross product, commutator and exponential/logarithmic function.

### Version 2.0.1
Corrected a type error in the using of property `norm`. Removed methods `__floor__` and `__ceil__`.

### Version 2.0
Major changes in everything. Now the object quaternion is initialized with the list of its components. A quaternion can be built from four numbers, from a list, from a tuple or from a complex number, using the classmethod `from_complex`. In the latter case, the user can specify which quaternion-imaginary part is the complex-imaginary one. The optional argument `to_real` has been removed.

Added the classmethod `random()`, that generates a uniformly random unitary quaternion.

Now, the real part, i, j, k and the norm are defined as `properties` of the Quaternion. Added the property `vector` to return the list of imaginary parts of the Quaternion.

Every operation is compatible with complex numbers.

Added the conversion from Quaternion to complex number. Added `__repr__` magic method.

Boolean magic methods have been improved, and the methods `is_real` and `is_imagy` have been added.

### Version 1.6.1
Minor changes. Added the method `is_real` to check if a quaternion is a real number.

### Version 1.6
The norm method evaluate the square-root using math.sqrt (more accuracy and time-saving).
Added an optional argument `to_real` in the initialization of the quaternion. If it is True, the creation returns real_part as int/float number; this means that the item lives outside from the class Quaternion. 
Added

```py
__int__ 	== to cast a quaternion in integer
__float__ 	== to cast a quaternion in float
```

### Version 1.5.2
Minor bug fixed (again).

### Version 1.5.1
Minor bug fixed (arised after the implementation of `__new__`).

### Version 1.5
Minor bug fixed. Added the magic method `__new__` to return real numbers when `Quaternion(x,0,0,0)` is initialized.

### Version 1.4

Minor bug fixed. Added right sum and subtraction. Added the method `__inverse_ip__`, that inverse the quaternion in place. Changed the name of conj to conjugate_ip.

### Version 1.3

Minor changes, saved some computational cost (thx to @Scarlet06).

### Version 1.2

Lowered execution time for all operations, removed `__scalarProduct__` and `__algebricPrint__` (thx to @Scarlet06).

### Version 1.1

Minor changes in the boolean magic methods (thx to @Scarlet06).

### Version 1.0

Created the class Quaternion. It stores four elements: the real part and the three imaginary parts i, j, k.
Build-in methods (ordered by utility):

+ Components:
Returns a 4-tuple with the components of the quaternions.

+ Algebric print:
Prints the algebric form of the quaternion, that is a+bi+cj+dk. The magic method `__str__` calls this function to see it writing `print(x)` directly.

+ Norm:
Returns the norm of the quaternion. The magic method `__abs__` grants user to get the norm writing `abs(x)`.

+ Normalize:
Returns the normalized quaternion.

+ Conj and Conjugate:
Conjugates quaternion, that is, if q = a+bi+cj+dk, then q* = a-bi-cj-dk. Moreover, x.conj().conj() = x.

+ Inverse:
Returns the inverse quaternion, that is, a quaternion h such that qh=hq=1. The magic method __inverse__ allows the user to get the inverse writing ~x.

+ Internal sum:
Componentwise sum between quaternions. Also there are the magic methods

```py
__add__ 	== x + y
__iadd__ 	== x += y
__sub__ 	== x - y
__isub__	== x -= y
```

+ Scalar product:
Performs componentwise scalar multiplication.

+ Multiplications:
Since multiplication between quaternions is not commutative, I have to distinquish between left and right multiplication. If the second argument of the multiplication is a scalar number, they return the standard scalar product. Magic methods:

```py
__mul__		== x * y
__rmul__	== y * x
__imul__	== x *= y
__pow__		== x ** c, where c is an integer
__ipow__	== x **= c, where c is an integer
```

+ Division:
Performs left-division between quaternions, that is, x / y = x * y^-1. Magic methods:

```py
__truediv__	== x / y
__itruediv__	== x /= y
```

+ Booleans methods:
is_unit		== checks if the quaternion has norm 1. Magic methods:

```py
__eq__		== performs the componentwise check x == y
__ne__		== performs the componentwise check x != y
__bool__	== checks if the quaternion is non zero
```

+ Unary operations:

```py
__pos__		== performs unary operation +x
__neg__		== returns -x, that is, -a-bi-cj-dk (it's not the conjugate!)
__round__	== rounds quaternion's decimals
__floor__	== applies floor to each components of the quaternion
__ceil__	== applies ceil to each components of the quaternion
```

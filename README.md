# QUATERNIONS - A (small) Python 3.11 resource
## > Perform quaternionic arithmetic easily in Python!
> Author: @ferrixio
> Version 1.5.1

===========================================================================

### TABLE OF CONTENTS 

1. Features
2. How to use
3. Known issues
4. Things to do
5. Description
6. Changelog

===========================================================================

### 1. FEATURES

This class allows user to emulate quaternionic algebruh in Python. The class can do:

	> internal and external sums
	> scalar multiplications
	> internal left-multiplications
	> internal right-multiplications
	> integer powers
	> divisions
	> normalizations
	> conjugations
	> inversions
	> algebric prints

I used mostly magic methods to allow user to write x+y, x*y, y/x, ..., directly.

===========================================================================

### 2. HOW TO USE

Open the file test_me.py and try it, or simply copy and paste the class in the file you want to use and then import it. (Don't forget to __cite me__ if you are using this in a project!)

===========================================================================

### 3. KNOWN ISSUES

The floating point is a #@!* and it breaks the accuracy of the computations when the number has a irrational norm, that is, the most of the time since the calculation of the norm needs a square root...
The operations +=, -=, *= and so on, don't work if on the left side there isn't a quaternion.

===========================================================================

### 4. THINGS TO DO

+ Create a library!!!
+ Quaternionic functions
+ Plotting quaternions (stereographic projection?)
+ Find a solution for floating point accuracy errors
+ Maybe use the @ operation?
+ Floor division?
+ Vector representation

===========================================================================

### 5. DESCRIPTION

The quaternion number system is an extended version of the complex numbers, firstly introduced by Rowan Hamilton in 1843. A quaternion is a 4-tuple of informations:
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

Enjoy :)

===========================================================================

### 6. CHANGELOG

§§ Version 1.5.1
Minor bug fixed (arised after the implementatio on _new_).

§§ Version 1.5
Minor bug fixed. Added the magic method _new_ to return real numbers when Quaternion(x,0,0,0) is initialized.

§§ Version 1.4

Minor bug fixed. Added right sum and subtraction. Added the method __inverse_ip__, that inverse the quaternion in place. Changed the name of conj to conjugate_ip.

§§ Version 1.3

Minor changes, saved some computational cost (thx to @Scarlet06).

§§ Version 1.2

Lowered execution time for all operations, removed _scalarProduct_ and _algebricPrint_ (thx to @Scarlet06).

§§ Version 1.1

Minor changes in the boolean magic methods (thx to @Scarlet06).

§§ Version 1.0

Created the class Quaternion. It stores four elements: the real part and the three imaginary parts i, j, k.
Build-in methods (ordered by utility):

> Components:
Returns a 4-tuple with the components of the quaternions.

> Algebric print:
Prints the algebric form of the quaternion, that is a+bi+cj+dk. The magic method __str__ calls this function to see it writing print(x) directly.

> Norm:
Returns the norm of the quaternion. The magic method __abs__ grants user to get the norm writing abs(x).

> Normalize:
Returns the normalized quaternion.

> Conj and Conjugate:
Conjugates quaternion, that is, if q = a+bi+cj+dk, then q* = a-bi-cj-dk. Moreover, x.conj().conj() = x.

> Inverse:
Returns the inverse quaternion, that is, a quaternion h such that qh=hq=1. The magic method __inverse__ allows the user to get the inverse writing ~x.

> Internal sum:
Componentwise sum between quaternions. Also there are the magic methods

	__add__ 	== x + y
 	__iadd__ 	== x += y
 	__sub__ 	== x - y
	__isub__	== x -= y

> Scalar product:
Performs componentwise scalar multiplication.

> Multiplications:
Since multiplication between quaternions is not commutative, I have to distinquish between left and right multiplication. If the second argument of the multiplication is a scalar number, they return the standard scalar product. Magic methods:

	__mul__		== x * y
	__rmul__	== y * x
	__imul__	== x *= y
	__pow__		== x ** c, where c is an integer
	__ipow__	== x **= c, where c is an integer

> Division:
Performs left-division between quaternions, that is, x / y = x * y^-1. Magic methods:

	__truediv__	== x / y
	__itruediv__	== x /= y

> Booleans methods:
is_unit		== checks if the quaternion has norm 1. Magic methods:

	__eq__		== performs the componentwise check x == y
	__ne__		== performs the componentwise check x != y
	__bool__	== checks if the quaternion is non zero

> Unary operations:

	__pos__		== performs unary operation +x
	__neg__		== returns -x, that is, -a-bi-cj-dk (it's not the conjugate!)
	__round__	== rounds quaternion's decimals
	__floor__	== applies floor to each components of the quaternion
	__ceil__	== applies ceil to each components of the quaternion


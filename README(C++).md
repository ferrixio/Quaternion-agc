# Quaternionic C++: a (small) C++ resource
### Perform quaternionic arithmetic easily in C++

:dragon: Author: Samuele Ferri (@ferrixio)

:star: Version 1.1

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

This class allows user to emulate quaternionic algebra in C++. The class can do:

	> internal and external sums
	> scalar multiplications
	> internal left-multiplications
	> internal right-multiplications
	> divisions
	> integer powers
	> normalizations
	> conjugations
	> inversions
	> algebric prints
	> type casting (int, float, double)
	> random generations
	> homotethies
	> conversion to rotation

I overload some operators to allow users to write `x+y`, `x*y`, `x/y`, ..., directly.

I recommend reading [this file](https://github.com/ferrixio/Quaternions/blob/main/How%20to%20assemble%20a%20quaternion.md) to better understand how to construct a quaternion.

Every value below 1e-13 is treated as 0, especially during logical checks. This does NOT imply that the value is set to 0!

===========================================================================

## 2. HOW TO USE

Open the file `Quaternion.cpp` and try it, or simply copy and paste the class in the file you want to use. (Don't forget to __cite me__ if you are using this in a project!)

===========================================================================

## 3. KNOWN ISSUES

The operations +=, -=, *= and so on, don't work if on the left side there isn't a quaternion.

I'm NOT an expert of C++.

===========================================================================

## 4. FUTURE IDEAS

+ :o: Complex number compatibility
+ :o: Floor division and modulo
+ :o: Geometry methods
+ :white_check_mark: Rotations
+ :warning: Multiple construtors

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

### Versione 1.1.1
Minor bug fixed.

Added the variable `FP_BOUND` to easily handle the floating point during logical checks. The user can edit it with the void method `change_bound`.

Splitted the random quaternion generators. Use `random_unit` for unitary random quaternions and `random` for float random quaternions.

### Version 1.1
Discovered the difference between `int(x)` and `static_cast<int>(x)`.

I tried to convert the `@classmethods` `random()` and `randint()` from python to C++, but I could not overload the constructor. So I create the void method `random()` to rewrite the parameters of the quaternion. If the boolean `integer` is set to `true`, an unitary random quaternion is generated, instead of generating a quaternion with integer values (between -50 and 50).

Implemented the methods `power`, `power_ip`, `homotethy`, `homotethy_ip`, `vector`, `rotation`.

Changed to `public` the four components of the quaternion, to remove the four getter methods. 

### Version 1.0
Converted most of my quaternion class from python to C++ language.

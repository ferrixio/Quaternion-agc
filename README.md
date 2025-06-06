# Quaternion-agc: a Python 3.10 resource
### Perform quaternionic algebra and geometry easily in Python

:dragon: Author: Samuele Ferri (@ferrixio)

:star: Version **2.3.1**

:scroll: [Changelog](https://github.com/ferrixio/Quaternion-agc/blob/main/docs/CHANGELOG.md)

## TABLE OF CONTENTS

1. [Requirements](#1-requirements)
2. [Features](#2-features)
3. [Known issues](#3-known-issues)
4. [Future ideas](#4-future-ideas)

## 1. REQUIREMENTS

Python version: **3.10** or above

Additional packages: numpy, matplotlib

## 2. FEATURES

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
	> iterations
	> random generations
	> exponential and logarithmic functions
	> dot product, cross product and commutator
	> extraction or generation from 3D rotations
	> rotate points in 3D
	> plotting quaternions

I used mostly magic methods to allow users to write `x+y`, `x*y`, `x/y`, ..., directly.

I recommend reading [`how to build a quaternion`](https://github.com/ferrixio/Quaternion-agc/blob/main/docs/How%20to%20build%20a%20quaternion.md) to better understand how to define and use a quaternion.

Every value below 1e-13 is treated as 0, especially during logical checks. This does NOT imply that the value is set to 0!

The new class `Hplot` is used to plot quaternions in different ways. Also, I invite you to read [`how to plot quaternions`](https://github.com/ferrixio/Quaternion-agc/blob/main/docs/How%20to%20plot%20quaternions.md) to understand how to plot them.

The class `functions` contains many methods to perform quaternionic calculus [work in progress].

"agc" in the title stands for "algebra-geometry-calculus".

## 3. KNOWN ISSUES

+ The in_place operations +=, -=, *= and so on, don't work if on the left side there isn't a quaternion.
+ There is a little chance that the method `Hplot.__getColors` returns negative numbers.

## 4. FUTURE IDEAS

+ :o: Add custom quaternionic functions
+ :o: Add more algebra and calculus to the field
+ :o: Add colorbar in plot to represent the real parts
+ :o: Fix the PyPI package
+ :warning: Study the topology of lists of quaternions
+ :warning: Implementing rotation of 3D objects


### Legend:
:o: = solution not (yet) found

:white_check_mark: = solution found and implemented

:warning: = solution found but the implementation needs to be improved

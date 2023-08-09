# Quaternionic-beast: a (small) Python 3.11 resource
### Perform quaternionic arithmetic easily in Python

:dragon: Author: Samuele Ferri (@ferrixio)

:star: Version **2.2.2**

:scroll: [Changelog](https://github.com/ferrixio/Quaternionic-beasts/blob/main/CHANGELOG)

## TABLE OF CONTENTS 

1. [REQUIREMENTS](#1-requirements)
2. [FEATURES](#2-features)
3. [KNOWN ISSUES](#3-known-issues)
4. [FUTURE IDEAS](#4-future-ideas)

## 1. REQUIREMENTS

Python version: **3.11** or above

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
	> random generations
	> exponential and logarithmic functions
	> dot product, cross product and commutator
	> extraction or generation from 3D rotations
	> rotate points in 3D
	> plotting quaternions

I used mostly magic methods to allow users to write `x+y`, `x*y`, `x/y`, ..., directly.

I recommend reading [`how to build a quaternion`](https://github.com/ferrixio/Quaternionic-beasts/blob/main/docs/How%20to%20build%20a%20quaternion.md) to better understand how to define and use a quaternion.

Every value below 1e-13 is treated as 0, especially during logical checks. This does NOT imply that the value is set to 0!

The new class `Hplot` to plot quaternions in different ways. Also, I invite you to read [`how to plot quaternions`](https://github.com/ferrixio/Quaternionic-beasts/blob/main/docs/How%20to%20plot%20quaternions.md) to have an idea of how I decide to plot them. 

## 3. KNOWN ISSUES

+ The in_place operations +=, -=, *= and so on, don't work if on the left side there isn't a quaternion.
+ There is a little chance that the method `Hplot.__getColors` returns negative numbers.

## 4. FUTURE IDEAS

+ :o: Add colorbar in plot to represent the real parts
+ :o: Study the topology of lists of quaternions
+ :white_check_mark: Vector representation
+ :white_check_mark: Add complex compatibility
+ :white_check_mark: Quaternionic functions
+ :white_check_mark: Floor division
+ :white_check_mark: Add @ operator
+ :white_check_mark: Plotting quaternions
+ :white_check_mark: Autogeneration of versors
+ :white_check_mark: Literally use LaTeX to write the .md files
+ :warning: Implementing rotation of 3D objects
+ :warning: Create a library

### Legend:
:o: = solution not (yet) found

:white_check_mark: = solution found and implemented

:warning: = solution found but the implementation needs to be improved

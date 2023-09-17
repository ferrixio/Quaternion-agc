# Quaternion algebra class for python 3.10

# Author:     Samuele Ferri (@ferrixio)
# Version:    2.2.3

# This class contains functions that operates in quaternionic space.

from Quaternion import Quaternion
from math import sqrt, sin, cos, e, log2, acos


def dot(q1: Quaternion, q2: Quaternion) -> float:
    '''Performs Euclidean dot product between vector parts of the two given quaternions.'''

    if not (isinstance(q1, Quaternion) and isinstance(q2, Quaternion)):
        raise TypeError("unsupported operand type(s) for dot: arguments must be 'Quaternion'")

    return q1.i*q2.i + q1.j*q2.j + q1.k*q2.k


def cross(q1: Quaternion, q2: Quaternion) -> tuple[float]:
    '''Performs the cross product of two given quaternions relative to the orientation
    determined by the ordered basis i, j, and k of R3.
    It returns a 3-tuple of floats representing the orthogonal vector to vector parts of the
    two given quaternions.
    '''
    if not (isinstance(q1, Quaternion) and isinstance(q2, Quaternion)):
        raise TypeError("unsupported operand type(s) for cross: arguments must be 'Quaternion'")

    _i = q1.j*q2.k - q1.k*q2.j
    _j = q1.k*q2.i - q1.i*q2.k
    _k = q1.i*q2.j - q1.j*q2.i
    return _i, _j, _k


def commutator(q1: Quaternion, q2: Quaternion) -> tuple[float]:
    '''Performs the commutator of the vector parts of two given quaternions.'''
    C = Quaternion.cross(q1, q2)
    return 2*C[0], 2*C[1], 2*C[2]


def exp(Q: Quaternion) -> Quaternion:
    '''Quaternionic exponential function.'''
    if Q.is_real():
        raise ZeroDivisionError("This is real number, isn't it?")

    v = Q.vector
    v_norm = sqrt(v[0]**2 + v[1]**2 + v[2]**2)

    ecos = (e**Q.real)*cos(v_norm)
    esin = (e**Q.real)*sin(v_norm)

    i = (v[0]/v_norm) * esin
    j = (v[1]/v_norm) * esin
    k = (v[2]/v_norm) * esin

    return Quaternion(ecos, i, j, k)


def log2(Q: Quaternion) -> Quaternion:
    '''Quaternionic logarithmic function.'''
    if Q.is_real():
        raise ZeroDivisionError("This is real number, isn't it?")

    v = Q.vector
    v_norm = sqrt(v[0]**2 + v[1]**2 + v[2]**2)

    lnq = log2(v_norm)
    a_acos = acos(Q.real/v_norm)

    i = (v[0]/v_norm) * a_acos
    j = (v[1]/v_norm) * a_acos
    k = (v[2]/v_norm) * a_acos

    return Quaternion(lnq, i, j, k)


def geodesic_dist(q1: Quaternion, q2: Quaternion) -> float:
    '''Returns the geodesic distance between two given unitary quaternions.
    
    It is the absolute value of half the angle subtended by them along a great arc of the 3-sphere.
    '''
    if not (isinstance(q1, Quaternion) and isinstance(q2, Quaternion)):
        raise TypeError("unsupported operand type(s) for geodesic_dist: arguments must be 'Quaternion'")

    if not q1.is_unit() or not q2.is_unit():
        raise ArithmeticError("invalid argument(s) given: both quaternions must be unitary")

    return acos(2*(Quaternion.dot(q1,q2))**2 - 1)

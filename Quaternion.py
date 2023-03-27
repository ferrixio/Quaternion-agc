# Quaternion class for python 3.11

# Author:     Samuele Ferri (@ferrixio)
# Version:    2.2.2

from math import sqrt, pi, sin, cos, e, log2, acos
from typing import Iterable

class Quaternion:
    '''Class to represent quaternions.
    
    Quaternion object is a 4D number and a 3D rotation.
    
    Attributes:
    - q: 4-dimensional list
    - ACCURACY: range to handle with floating point
    '''

    ## Initializers ##
    def __new__(cls, real:float=0, i_img:float=0, j_img:float=0, k_img:float=0,
                seq=None, acc:float=1e-13):
        '''Pre-generation of the quaternion.'''

        if not isinstance(real, float|int):
            raise TypeError("The real part must be an integer or a float")

        if not all((isinstance(i_img, float|int), isinstance(j_img, float|int),
                isinstance(k_img, float|int))):
            raise TypeError("All imaginary parts must be integers or floats")

        if isinstance(seq, Iterable) and len(seq) > 4:
            raise IndexError("Invalid length: it must be from 0 to 4")
        
        if not isinstance(acc, float):
            raise TypeError("Accuracy must be a float")

        return super().__new__(cls)


    def __init__(self, real:float=0, i_img:float=0, j_img:float=0, k_img:float=0,
                 seq=None, acc:float=1e-13):
        '''Initializer of Quaternion object.

        See [How to assemble a quaternion](https://github.com/ferrixio/Quaternionic-beasts/blob/main/Documentations/How%20to%20assemble%20a%20quaternion.md)
        doc for complete behaviour.
        '''
        self.ACCURACY = acc       ## Floating point limiter ##

        if isinstance(seq, int|float):
            seq = [seq]

        if isinstance(seq, Iterable):
            match len(seq):
                case 0:
                    self.q = [0, 0, 0, 0]
                case 1:
                    self.q = [seq[0], 0, 0, 0]
                case 2:
                    self.q = [seq[0], seq[1], 0, 0]
                case 3:
                    self.q = [seq[0], seq[1], seq[2], 0]
                case 4:
                    self.q = [seq[0], seq[1], seq[2], seq[3]]
            return

        self.q = [real, i_img, j_img, k_img]


    @classmethod
    def from_complex(cls, cplx:complex=0j, imag:str='i'):
        '''Generates a quaternion from a complex number.
        
        The string imag is used to specify which imaginary part is to be used (i, j or k).
        As default, it is the first.
        '''
        match imag:
            case 'i':
                return cls(real=cplx.real, i_img=cplx.imag)
            case 'j':
                return cls(real=cplx.real, j_img=cplx.imag)
            case 'k':
                return cls(real=cplx.real, k_img=cplx.imag)
            case _:
                raise AttributeError("invalid attribute given: imag must be 'i', 'j', or 'k'")
                
                
    @classmethod
    def from_rotation(cls, theta:float=0, axis:Iterable[int|float]=(0,0,0)):
        '''Generates a quaternion from a 3D rotation.
        
        Arguments:
        - theta[float]: angle in degrees
        - axis[iterable]: vector in R3 representing the axis
        '''
        theta_rad = (theta/180)*pi
        a = cos(theta_rad/2)

        if not len(axis)==3:
            raise TypeError("invalid length of axis: must be 3")
        
        b,c,d = axis[0]*sin(theta_rad/2), axis[1]*sin(theta_rad/2), axis[2]*sin(theta_rad/2)
        return cls(a,b,c,d)


    @classmethod
    def random_unit(cls):
        '''Random unitary quaternion generator.'''
        from random import random
        while True:
            a,b,c = random(), random(), random()
            r = sqrt(1-a)*sin(2*pi*b)
            i = sqrt(1-a)*cos(2*pi*b)
            j = sqrt(a)*sin(2*pi*c)
            k = sqrt(a)*cos(2*pi*c)

            if r**2+i**2+j**2+k**2 == 1.0:
                break    

        return cls(r,i,j,k)


    @classmethod
    def random(cls, a:float = -50, b:float = 50):
        '''Random quaternion generator.
        
        Arguments:
        - a[float]: left bound of the uniform distribution; default value is -50
        - b[float]: right bound of the uniform distribution; default value is 50
        '''
        from random import uniform
        return cls(uniform(a,b), uniform(a,b), uniform(a,b), uniform(a,b))



    ## Properties ##
    @property
    def real(self) -> float:
        '''Returns the real part of the quaternion.'''
        return self.q[0]

    @property
    def i(self) -> float:
        '''Returns the first imaginary part of the quaternion.'''
        return self.q[1]

    @property
    def j(self) -> float:
        '''Returns the second imaginary part of the quaternion.'''
        return self.q[2]

    @property
    def k(self) -> float:
        '''Returns the third imaginary part of the quaternion.'''
        return self.q[3]


    @real.setter
    def real(self, a):
        if not isinstance(a, int|float):
            raise ValueError("Real part must be of type 'int' or 'float'")
        self.q[0] = a
        
    @i.setter
    def i(self, a):
        if not isinstance(a, int|float):
            raise ValueError("i must be of type 'int' or 'float'")
        self.q[1] = a
        
    @j.setter
    def j(self, a):
        if not isinstance(a, int|float):
            raise ValueError("j must be of type 'int' or 'float'")
        self.q[2] = a      

    @k.setter
    def k(self, a):
        if not isinstance(a, int|float):
            raise ValueError("k must be of type 'int' or 'float'")
        self.q[3] = a

    @property
    def vector(self) -> tuple:
        '''Returns a list with the three imaginary parts.'''
        return tuple(self.q[1:])

    @property
    def rotation(self) -> tuple:
        '''Gets the rotation associated to the quaternion.
        
        Returns a 2-tuple (theta, (x, y, z)) containing:
            theta: the angle
            (x,y,z): axis of rotation
            
        Notes:
        - the quaternion will be normalized if its norm is not 1
        - the method returns (0,(1,0,0)) if the real part is 1, because it is
        the pole of the conversion map
        '''
        if self.real == 1.0:
            return 0,(1,0,0)

        self_copy = self.normalize()

        theta = 2*acos(self_copy.real)
        return theta, (self_copy.i/sin(theta/2), self_copy.j/sin(theta/2), self_copy.k/sin(theta/2))
    

    def change_bound(self, fp:float=1e-13):
        '''Changes the floating point limiter. Default value is 1e-13.'''
        self.ACCURACY = fp


    ## Type magic methods ##
    def __str__(self) -> str:
        '''Magic method to show a quaternion using print().

        Returns a string of the form "a + bi + cj + dk".

        Note: numbers below ACCURACY will be printed as 0.
        '''
        ans, terms = '', {0:'', 1:'i', 2:'j', 3:'k'}

        for i,part in enumerate(self.q):
            if not part or abs(part)<self.ACCURACY:  #if zero coeff (or almost there), it doesn't write
                continue
            elif not ans:                      #positive coeff and not in first place
                ans += f'{part}{terms[i]}'
                continue
            ans += f'{part:+}{terms[i]}'

        if not ans:
            return '0'
        
        return ans

    def __repr__(self) -> str:
        '''Represents the quaternion as object declaration.'''
        return f"Quaternion({self.real}, {self.i}, {self.j}, {self.k})"

    def __int__(self) -> int:
        '''Magic method to convert a quaternion to an integer.

        Truncates the quaternion object by only considering its real part as an integer.
        '''
        return int(self.real)

    def __float__(self) -> float:
        '''Magic method to convert a quaternion to a float.

        Truncates the quaternion object by only considering its real part as a float.
        '''
        return float(self.real)

    def __complex__(self) -> complex:
        '''Magic method to convert a quaternion to a complex number.

        Truncates the quaternion object by only considering its first complex part,
        that is, a projection from the 3-sphere to the complex plane.
        '''
        return complex(self.real, self.i)



    ## Unary operation magic methods ##
    def __pos__(self):
        '''Magic method to perform unary operation +object.
        
        Actually it creates a copied version of the quaternion.
        '''
        return self.__class__(self.real, self.i, self.j, self.k)

    def __neg__(self):
        '''Magic method to perform the unary operation -object.
        
        It reverse the sign of each components of the quaternion.
        '''
        return self.__class__(-self.real, -self.i, -self.j, -self.k)

    def __invert__(self):
        '''Magic method to get the inverse quaternion using ~.'''
        return self.inverse()

    def __abs__(self) -> float:
        '''Magic method to perform abs().
        
        The absolute value of a quaternion is it's norm.
        '''
        return self.norm

    def __round__(self, n:int=3):
        '''Magic method to round the decimals of every components of the quaternion.
        Default value of n is 3.
        '''
        return Quaternion(round(self.real,n), round(self.i,n), round(self.j,n), 
                round(self.k,n))


    
    ## Binary operation magic methods ##
    @staticmethod
    def check_other(T_other, operation:str):
        '''Auxiliary function to raise exceptions during arithmetic.'''
        if isinstance(T_other, int|float|complex|Quaternion):
            return

        raise TypeError(f"unsupported operand type(s) for {operation}: \
            'Quaternion' and '{T_other.__name__}'")


    # Addition
    def __add__(self, other):
        '''Magic method to emulate the left sum.'''
        self.check_other(other, '+')

        if isinstance(other, int|float):
            return Quaternion(self.real+other,self.i,self.j,self.k)

        if isinstance(other, complex):
            return Quaternion(self.real+other.real,self.i+other.imag,self.j,self.k)

        return Quaternion(self.real+other.real, self.i+other.i, self.j+other.j, self.k+other.k)

    def __radd__(self, other):
        '''Magic method to emulate the right sum. Since (H,+) is an Abelian group,
        left and right are the same.'''
        return self.__add__(other)

    def __iadd__(self, other):
        '''Magic method to left-sum quaternions using +=.'''
        self.check_other(other, '+=')

        if isinstance(other, int|float):
            self.real += other
            return self

        if isinstance(other, complex):
            self.real += other.real
            self.i += other.imag
            return self

        self.real += other.real
        self.i += other.i
        self.j += other.j
        self.k += other.k
        return self


    # Subtraction
    def __sub__(self, other):
        '''Magic method to emulate left subtraction.'''
        self.check_other(other, '-')

        if isinstance(other, int|float):
            return Quaternion(self.real-other,self.i,self.j,self.k)

        if isinstance(other, complex):
            return Quaternion(self.real-other.real,self.i-other.imag,self.j,self.k)

        return Quaternion(self.real-other.real,
                    self.i-other.i, self.j-other.j, self.k-other.k)

    def __rsub__(self, other):
        '''Magic method to emulate right subtraction.'''
        self.check_other(other, 'r-')

        if isinstance(other, int|float):
            return Quaternion(other-self.real,-self.i,-self.j,-self.k)

        if isinstance(other, complex):
            return Quaternion(other.real-self.real,other.imag-self.i,self.j,self.k)

        return Quaternion(other.real-self.real,
                    other.i-self.i, other.j-self.j, other.k-self.k)

    def __isub__(self, other):
        '''Magic method to subtract quaternions using -=.'''
        self.check_other(other, '-=')

        if isinstance(other, int|float):
            self.real -= other
            return self

        if isinstance(other, complex):
            self.real -= other.real
            self.i -= other.imag
            return self

        self.real -= other.real
        self.i -= other.i
        self.j -= other.j
        self.k -= other.k
        return self


    # Multiplication
    def __mul__(self, other):
        '''Magic method to perform quaternionic left-multiplication x * y.'''
        self.check_other(other, '*')

        if isinstance(other, int|float):
            return Quaternion(self.real*other,self.i*other,self.j*other,self.k*other)

        if isinstance(other, complex):
            return Quaternion(self.real*other.real - self.i*other.imag, 
                self.real*other.imag + self.i*other.real,
                self.j*other.real + self.k*other.imag,
                self.k*other.real - self.j*other.imag)

        return Quaternion(
            self.real*other.real - self.i*other.i - self.j*other.j - self.k*other.k,
            self.real*other.i + self.i*other.real + self.j*other.k - self.k*other.j,
            self.real*other.j + self.j*other.real - self.i*other.k + self.k*other.i,
            self.real*other.k + self.k*other.real + self.i*other.j - self.j*other.i)

    def __rmul__(self, other):
        '''Magic method to perform quaternionic right-multiplication y * x.'''
        self.check_other(other, 'r*')

        if isinstance(other, int|float):
            return Quaternion(self.real*other,self.i*other,self.j*other,self.k*other)

        if isinstance(other, complex):
            return Quaternion(self.real*other.real - self.i*other.imag,
                self.real*other.imag + self.i*other.real,
                self.j*other.real - self.k*other.imag,
                self.k*other.real + self.j*other.imag)

        return Quaternion(
            self.real*other.real - self.i*other.i - self.j*other.j - self.k*other.k,
            self.real*other.i + self.i*other.real - self.j*other.k + self.k*other.j,
            self.real*other.j + self.j*other.real + self.i*other.k - self.k*other.i,
            self.real*other.k + self.k*other.real - self.i*other.j + self.j*other.i)

    def __imul__(self, other):
        '''Magic method to perform quaternionic left-multiplication x *= y.'''
        self.check_other(other, '*=')

        if isinstance(other, int|float):
            self.real *= other
            self.i *= other
            self.j *= other
            self.k *= other
            return self

        if isinstance(other, complex):
            other = self.from_complex(other)

        n_real = self.real*other.real - self.i*other.i - self.j*other.j - self.k*other.k
        n_i = self.real*other.i + self.i*other.real + self.j*other.k - self.k*other.j
        n_j = self.real*other.j + self.j*other.real - self.i*other.k + self.k*other.i
        n_k = self.real*other.k + self.k*other.real + self.i*other.j - self.j*other.i

        del other
        self.real, self.i, self.j, self.k  = n_real, n_i, n_j, n_k
        return self


    # Powers
    def __pow__(self, power):
        '''Magic method to implement int-exponentiation operation **, by applying left-multiplication.'''
        self.check_other(power, '**')

        if not isinstance(power, int):
            raise TypeError('The power must be a positive or a negative integer')

        h = Quaternion(1)
        if power > 0:
            h = +self
            for _ in range(power-1):
                h *= self

        elif power < 0:
            h = self.inverse()
            q = +h
            for _ in range(-power-1):
                h *= q

        return h

    def __ipow__(self, power):
        '''Magic method to implement int-exponentiation operation **=, by applying 
        left-multiplication.'''
        self.check_other(power, '**=')

        if not isinstance(power, int):
            raise TypeError('The power must be a positive or a negative integer')

        if power < 0:
            self.inverse_ip()
            power *= -1

        if power:
            h = +self
            for _ in range(power-1):
                self *= h
            return self

        self.real, self.i, self.j, self.k = 1, 0, 0, 0
        return self


    # Division
    def __truediv__(self, other):
        '''Magic method to perform left quaternionic division x / y.'''
        self.check_other(other, '/')

        if isinstance(other, int|float):
            return Quaternion(self.real/other, self.i/other, self.j/other, self.k/other)

        if isinstance(other, complex):
            return self.__mul__(self.from_complex(other).inverse_ip())

        return self.__mul__(~other)

    def __itruediv__(self, other):
        '''Magic method to perform quaternionic division x /= y.'''
        self.check_other(other, '/=')

        if isinstance(other, int|float):
            self.real /= other
            self.i /= other
            self.j /= other
            self.k /= other
            return self

        if isinstance(other, complex):
            return self.__imul__(self.from_complex(other).inverse_ip())

        return self.__imul__(~other)


    # Modulo
    def __mod__(self, other):
        '''Magic method to implement int-modulo operation x % y.
        
        Since there is not a true modulo operation in H, it returns the reminder of
        an hipotetical division along the line, in HP1, through the given quaternion.
        '''
        self.check_other(other, '%')

        if not isinstance(other, int|float) or other < 0:
            raise TypeError('The modulo must be a positive integer')

        f = self.norm % other
        return self.normalize().__mul__(f)


    # Floordivision
    def __floordiv__(self, other):
        '''Magic method to implement int-modulo operation x // y.
        
        Since there is not a true modulo operation in H, it returns the quotient of
        an hipotetical division along the line, in HP1, through the given quaternion.
        '''
        self.check_other(other, '//')

        if not isinstance(other, int|float) or other < 0:
            raise TypeError('The divisor must be a positive integer')

        f = self.__mod__(other)
        return self.__sub__(f).__truediv__(other)


    # Matmul
    def __matmul__(self, other):
        '''Magic method to implement matmul x @ y.
        
        Since floordivision doesn't exist in H, it performs an homotethy on x
        to the sphere of radius y.
        '''
        self.check_other(other, '@')

        if not isinstance(other, int|float) or other < 0:
            raise TypeError('The divisor must be a positive number')

        return self.normalize().__mul__(other)

    def __imatmul__(self, other):
        '''Magic method to implement matmul x @= y.'''
        self.check_other(other, '@=')

        if not isinstance(other, int|float) or other < 0:
            raise TypeError('The divisor must be a positive number')

        return self.normalize().__imul__(other)



    ## Boolean magic methods ##
    def __eq__(self, other) -> bool:
        '''Magic method to perform ==.
        
        Checks if all the components between the two quaternions are the same.
        '''
        return self.__sub__(other).__abs__() < self.ACCURACY

    def __ne__(self, other) -> bool:
        '''Magic method to perform !=.

        Returns the negation of __eq__.
        '''
        return not self.__eq__(other)

    def __bool__(self) -> bool:
        '''Magic method to perform bool().

        Returns True if the quaternion is not zero.
        '''
        return any(map(lambda x: abs(x) > self.ACCURACY, self.q))

    def is_unit(self) -> bool:
        '''Checks if the quaternion is unitary, that is, if it lies on the 3-sphere.'''
        return abs(self.norm-1) < self.ACCURACY

    def is_real(self) -> bool:
        '''Checks if the quaternion is a real number.'''
        return abs(self.i)<=self.ACCURACY and abs(self.j)<=self.ACCURACY and abs(self.k)<=self.ACCURACY

    def is_imagy(self) -> bool:
        '''Checks if the quaternion has only imginary parts.'''
        return abs(self.real)<=self.ACCURACY and not self.is_real()



    ## Special functions to get quaternionic components ##
    @property
    def norm(self) -> float:
        '''Returns the norm of the quaternion.'''
        return sqrt(self.square_norm())

    def square_norm(self) -> float:
        '''Returns the square norm of the quaternion. That is the square of the euclidean norm
         in R4.
         '''
        return self.real**2 + self.i**2 + self.j**2 + self.k**2


    def normalize(self):
        '''Returns the normalized quaternion.'''
        t = self.norm
        return Quaternion(self.real/t, self.i/t, self.j/t, self.k/t)

    def normalize_ip(self):
        '''Normalizes the quaternion in place.'''
        t = self.norm
        if t != 1.0:
            self.real /= t
            self.i /= t
            self.j /= t
            self.k /= t
        return self


    def conjugate(self):
        '''Returns the conjugated quaternion, that is a quaternion with the signs of the
        imaginary parts reversed.
        '''
        return Quaternion(self.real,-self.i,-self.j,-self.k)

    def conjugate_ip(self):
        '''Conjugates the quaternion in place.'''
        self.i *= -1
        self.j *= -1
        self.k *= -1
        return self
    

    def inverse(self):
        '''Returns the inverse quaternion with respect to multiplication.'''
        if not self.__bool__():
            raise ZeroDivisionError("It's not possible to invert the zero quaternion")

        n = self.square_norm()
        return Quaternion(self.real/n, -self.i/n, -self.j/n, -self.k/n)

    def inverse_ip(self):
        '''Inverts (in place) the quaternion with respect to multiplication.'''
        if not self.__bool__():
            raise ZeroDivisionError("It's not possible to invert the zero quaternion")

        n = self.square_norm()
        self.real /= n
        self.i /= -n
        self.j /= -n
        self.k /= -n
        return self


    ## Geometry (functions) ##
    def rotate_point(self, point:Iterable[int|float], passive:bool=False) -> tuple:
        '''Performs the rotation of a given point by this quaternion.
        
        Notes:
        - normalizes the quaternion if it is not unitary
        - the boolean passive, if set to True, performs the passive rotation, that is the inverse
        rotation.
        '''
        if not len(point)==3:
            raise TypeError("point must be a 3-dimensional iterable of floats")
        
        p = Quaternion(seq=(0,*point))
        self_copy = self.normalize()

        if not passive:
            return (self_copy.inverse() * p * self_copy).vector
        
        return (self_copy * p * self_copy.inverse()).vector


    # They are @staticmethods since they "exit" from the object
    @staticmethod
    def dot(q1, q2) -> float:
        '''Performs Euclidean dot product between vector parts of the two given quaternions.'''

        if not (isinstance(q1, Quaternion) and isinstance(q2, Quaternion)):
            raise TypeError("unsupported operand type(s) for dot: arguments must be 'Quaternion'")

        return q1.i*q2.i + q1.j*q2.j + q1.k*q2.k

    @staticmethod
    def cross(q1, q2) -> tuple:
        '''Performs the cross product of two given quaternions relative to the orientation
        determined by the ordered basis i, j, and k of R3.'''
        if not (isinstance(q1, Quaternion) and isinstance(q2, Quaternion)):
            raise TypeError("unsupported operand type(s) for cross: arguments must be 'Quaternion'")

        _i = q1.j*q2.k - q1.k*q2.j
        _j = q1.k*q2.i - q1.i*q2.k
        _k = q1.i*q2.j - q1.j*q2.i
        return _i, _j, _k

    @staticmethod
    def commutator(q1, q2) -> tuple:
        '''Performs the commutator of the vector parts of two given quaternions.'''
        C = Quaternion.cross(q1, q2)
        return 2*C[0], 2*C[1], 2*C[2]
    
    @staticmethod
    def exp(Q):
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

    @staticmethod
    def log2(Q):
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

    @staticmethod
    def geodesic_dist(q1, q2) -> float:
        '''Returns the geodesic distance between two given unitary quaternions.
        
        It is the absolute value of half the angle subtended by them along a great arc of the 3-sphere.
        '''
        if not (isinstance(q1, Quaternion) and isinstance(q2, Quaternion)):
            raise TypeError("unsupported operand type(s) for geodesic_dist: arguments must be 'Quaternion'")

        if not q1.is_unit() or not q2.is_unit():
            raise ArithmeticError("invalid argument(s) given: both quaternions must be unitary")

        return acos(2*(Quaternion.dot(q1,q2))**2 - 1)

# End of Quaternion class


class Versor(Quaternion):
    '''Class to represent unitary quaternions.
    
    Unitary quaternions are called 'versors', because they have norm equal to 1.
    
    Attributes:
    - q: 4-dimensional list of norm 1
    - ACCURACY: range to handle with floating point
    '''

    def __new__(cls, real:float = 1, i_img:float = 0, j_img:float = 0, k_img:float = 0,
                seq=None, acc: float = 1e-13):
        '''Pre-generation of the versor.'''

        if real==i_img==j_img==k_img==0:
            return Quaternion(0,acc=acc)
        
        if isinstance(seq, int|float):
            seq = [seq]
        if isinstance(seq, list|tuple) and any((h==0 for h in seq)):
            return Quaternion(seq=seq, acc=acc)
                
        return super().__new__(cls)

    def __init__(self, real:float = 1, i_img:float = 0, j_img:float = 0, k_img:float = 0,
                 seq=None, acc:float = 1e-13):
        '''Initializer of Versor object, subclass of Quaternion.
        
        The parameters in input are slightly different from Quaternion. The real part has
        default value 1, in order to generate a unitary quaternion if 'Versor()' is called.

        If a zero quaternion is given in input, the constructor __new__ exits from Versor
        and generates the 0 as Quaternion object. 
        '''
        self.ACCURACY = acc       ## Floating point limiter ##

        if isinstance(seq, tuple|list):
            match len(seq):
                case 0:
                    temp = [1, 0, 0, 0]
                case 1:
                    temp = [seq[0], 0, 0, 0]
                case 2:
                    temp = [seq[0], seq[1], 0, 0]
                case 3:
                    temp = [seq[0], seq[1], seq[2], 0]
                case 4:
                    temp = [seq[0], seq[1], seq[2], seq[3]]

        else:
           temp = [real, i_img, j_img, k_img] 

        norm = sqrt(temp[0]**2 + temp[1]**2 + temp[2]**2 + temp[3]**2)
        self.q=[t/norm for t in temp]

## End of Versor class
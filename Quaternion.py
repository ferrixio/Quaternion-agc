'''
Quaternion class

Author:     Samuele Ferri (@ferrixio)
Version:    2.0
Read me:    ---
'''

from math import sqrt, pi, sin, cos

class Quaternion:
    #Initializers
    def __new__(cls, real:float=0, i_img:float=0, j_img:float=0, k_img:float=0, seq=None):
        '''Pre-generation of the quaternion.'''

        if not isinstance(real, float|int):
            raise TypeError('The real part must be an integer or a float.')

        if not all((isinstance(i_img, float|int), isinstance(j_img, float|int),
                isinstance(k_img, float|int))):
            raise TypeError('All imaginary parts must be integers or floats.')

        if type(seq) in (list,tuple) and len(seq)>4:
            raise IndexError('Invalid length given. It must be from 0 to 4.')

        return super().__new__(cls)

        
    def __init__(self, real:float=0, i_img:float=0, j_img:float=0, k_img:float=0, seq=None):
        '''Quaternion's initialization.'''
            
        if type(seq) in (list, tuple):
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
        '''Generates a quaternion from a complex number. imag is a string used to specify 
        which imaginary part is to be used (i, j or k). As default, it is the first.
        '''
        match imag:
            case 'i':
                return cls(real=cplx.real, i_img=cplx.imag)
            case 'j':
                return cls(real=cplx.real, j_img=cplx.imag)
            case 'k':
                return cls(real=cplx.real, k_img=cplx.imag)
            case _:
                raise RecursionError('Wtf?')
                

    @classmethod
    def random(cls):
        '''Random unitary quaternion generator.'''
        from random import random
        a,b,c = random(), random(), random()

        return cls(sqrt(1-a)*sin(2*pi*b), \
            sqrt(1-a)*cos(2*pi*b), sqrt(a)*sin(2*pi*c), sqrt(a)*cos(2*pi*c))

    
    #Properties
    @property
    def real(self): return self.q[0]

    @property
    def i(self): return self.q[1]

    @property
    def j(self): return self.q[2]

    @property
    def k(self): return self.q[3]

    @real.setter
    def real(self, a):
        if not isinstance(a,(int,float,chr)):
            raise ValueError('Real part must be int, float or chr.')
        self.q[0] = a
        
    @i.setter
    def i(self, a):
        if not isinstance(a,(int,float,chr)):
            raise ValueError('i must be int, float or chr.')
        self.q[1] = a
        
    @j.setter
    def j(self, a):
        if not isinstance(a,(int,float,chr)):
            raise ValueError('j must be int, float or chr.')
        self.q[2] = a      

    @k.setter
    def k(self, a):
        if not isinstance(a,(int,float,chr)):
            raise ValueError('k must be int, float or chr.')
        self.q[3] = a

    @property
    def vector(self):
        return self.q[1:]


    #Type magic methods
    def __str__(self) -> str:
        '''Magic method to print a quaternion using print().'''

        ans = ''
        terms = {0:'', 1:'i', 2:'j', 3:'k'}

        for i,part in enumerate(self.q):
            if not part:                                #if zero coeff, it doesn't write
                continue
            elif not ans:                               #positive coeff and not in first place
                ans += f'{part}{terms[i]}'
            else:                                       #negative coeff
                ans += f'{part:+}{terms[i]}'

        if not ans:
            return '0'

        del terms
        return ans

    def __repr__(self) -> str:
        '''Represents the quaternion as object declaration.'''
        return f"Quaternion({self.real}, {self.i}, {self.j}, {self.k})"

    def __int__(self) -> int:
        '''Magic method to convert a quaternion to an integer.
        Truncates the quaternion object by only considering its real part as integer.'''
        return int(self.real)

    def __float__(self) -> float:
        '''Magic method to convert a quaternion to a float.
        Truncates the quaternion object by only considering its real part as float.'''
        return float(self.real)

    def __complex__(self):
        '''Magic method to convert a quaternion to a complex number.
        Truncates the quaternion object by only considering the first complex part,
        that is, a projection from the hypersphere in 4-dim to the complex plane.'''
        return complex(self.real, self.i)



    #Unary operation magic methods
    def __pos__(self):
        '''Magic method to perform unary operation +object.'''
        return self.__class__(self.real,self.i,self.j,self.k)

    def __neg__(self):
        '''Magic method to perform the unary operation -object.'''
        return self.__class__(-self.real, -self.i, -self.j, -self.k)

    def __invert__(self):
        '''Magic method to get the inverse quaternion using ~.'''
        return self.inverse()

    def __abs__(self):
        '''Magic method to perform abs(). The absolute value of a quaternion is it's norm.'''
        return self.norm()

    def __round__(self, n:int=2):
        '''Magic method to round the decimals of every components of the quaternion.
        If n is not given, n = 2.'''
        return Quaternion(round(self.real,n), round(self.i,n), round(self.j,n), 
                round(self.k,n))

    def __floor__(self):
        '''Magic method to round to the floor every components of the quaternion.'''
        return Quaternion(self.real.__floor__(),
                self.i.__floor__(), self.j.__floor__(), self.k.__floor__())

    def __ceil__(self):
        '''Magic method to round to the ceiling every components of the quaternion.'''
        return Quaternion(self.real.__ceil__(),
                self.i.__ceil__(), self.j.__ceil__(), self.k.__ceil__())


    
    #Binary operation magic methods

    #Addition
    def __add__(self, other):
        '''Magic method to emulate the left sum.'''
        if type(other) in (int, float):
            return Quaternion(self.real+other,self.i,self.j,self.k)

        if type(other) is complex:
            return Quaternion(self.real+other.real,self.i+other.imag,self.j,self.k)

        return Quaternion(self.real+other.real,
                    self.i+other.i, self.j+other.j, self.k+other.k)

    def __radd__(self, other):
        '''Magic method to emulate the right sum.'''
        if type(other) in (int, float):
            return Quaternion(other+self.real,self.i,self.j,self.k)

        if type(other) is complex:
            return Quaternion(self.real+other.real,self.i+other.imag,self.j,self.k)

        return Quaternion(self.real+other.real,
                    self.i+other.i, self.j+other.j, self.k+other.k)

    def __iadd__(self, other):
        '''Magic method to left-sum quaternions using +=.'''
        if type(other) in (int, float):
            self.real += other
            return self

        if type(other) is complex:
            self.real += other.real
            self.i += other.imag
            return self

        self.real += other.real
        self.i += other.i
        self.j += other.j
        self.k += other.k
        return self


    #Subtraction
    def __sub__(self, other):
        '''Magic method to emulate left subtraction.'''
        if type(other) in (int, float):
            return Quaternion(self.real-other,self.i,self.j,self.k)

        if type(other) is complex:
            return Quaternion(self.real-other.real,self.i-other.imag,self.j,self.k)

        return Quaternion(self.real-other.real,
                    self.i-other.i, self.j-other.j, self.k-other.k)

    def __rsub__(self, other):
        '''Magic method to emulate right subtraction.'''
        if type(other) in (int, float):
            return Quaternion(other-self.real,-self.i,-self.j,-self.k)

        if type(other) is complex:
            return Quaternion(other.real-self.real,other.imag-self.i,self.j,self.k)

        return Quaternion(other.real-self.real,
                    other.i-self.i, other.j-self.j, other.k-self.k)

    def __isub__(self, other):
        '''Magic method to subtract quaternions using -=.'''
        if type(other) in (int, float):
            self.real -= other
            return self

        if type(other) is complex:
            self.real -= other.real
            self.i -= other.imag
            return self

        self.real -= other.real
        self.i -= other.i
        self.j -= other.j
        self.k -= other.k
        return self


    #Multiplication
    def __mul__(self, other):
        '''Magic method to perform quaternionic left-multiplication x * y.'''
        if type(other) in (int, float):
            return Quaternion(self.real*other,self.i*other,self.j*other,self.k*other)

        if type(other) is complex:
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
        if type(other) in (int, float):
            return Quaternion(self.real*other,self.i*other,self.j*other,self.k*other)

        if type(other) is complex:
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
        if type(other) in (int, float):
            self.real *= other
            self.i *= other
            self.j *= other
            self.k *= other
            return self

        if type(other) is complex:
            other = self.from_complex(other)

        n_real = self.real*other.real - self.i*other.i - self.j*other.j - self.k*other.k
        n_i = self.real*other.i + self.i*other.real + self.j*other.k - self.k*other.j
        n_j = self.real*other.j + self.j*other.real - self.i*other.k + self.k*other.i
        n_k = self.real*other.k + self.k*other.real + self.i*other.j - self.j*other.i

        del other
        self.real = n_real
        self.i, self.j, self.k = n_i, n_j, n_k
        return self


    #Powers
    def __pow__(self, power):
        '''Magic method to implement int-exponentiation operation **, by applying left-multiplication.'''
        if type(power) is not int:
            raise Exception('The power must be a positive or a negative integer.')

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
        if type(power) is not int:
            raise Exception('The power must be a positive or a negative integer.')

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


    #Division
    def __truediv__(self, other):
        '''Magic method to perform left quaternionic division x / y.'''
        if type(other) in (int, float):
            return Quaternion(self.real/other, self.i/other, self.j/other, self.k/other)

        if type(other) is complex:
            return self.__mul__(self.from_complex(other).inverse_ip())

        return self.__mul__(~other)

    def __itruediv__(self, other):
        '''Magic method to perform quaternionic division x /= y.'''
        if type(other) in (int, float):
            self.real /= other
            self.i /= other
            self.j /= other
            self.k /= other
            return self

        if type(other) is complex:
            return self.__imul__(self.from_complex(other).inverse_ip())

        return self.__imul__(~other)


    #Dot product == scalar product between vectors in R4
    # def __matmul__(self, other) -> float:
    #     if not isinstance(other, Quaternion):
    #         raise TypeError("unsupported operand type(s) for @: arguments must be 'Quaternion'.")

    #     return self.real*other.real + self.i*other.i + self.j*other.j + self.k*other.k


    #Boolean (magic) methods
    def __eq__(self, other) -> bool:
        '''Checks if all the components between the two quaternions are the same.'''
        return self.q == other.q

    def __ne__(self, other) -> bool:
        '''Checks if one of the components between the two quaternions are different.'''
        return self.q != other.q

    def __bool__(self) -> bool:
        '''Checks if the quaternion is not zero.'''
        return self.q != [0,0,0,0]

    def is_unit(self) -> bool:
        '''Checks if the quaternion is unitary, that is, if it lies on the 3-sphere.'''
        return self.square_norm() == 1.0

    def is_real(self) -> bool:
        '''Checks if the quaternion is a real number.'''
        return not bool(self.i or self.j or self.k)

    def is_imagy(self) -> bool:
        '''Checks if the quaternion has only imginary parts.'''
        return bool((not self.real) and (self.i or self.j or self.k))



    #Special functions to get quaternionic components
    @property
    def norm(self) -> float:
        '''Returns the norm of the quaternion.'''
        return sqrt(self.square_norm())

    def square_norm(self) -> float:
        '''Returns the square norm of the quaternion'''
        return self.real**2 + self.i**2 + self.j**2 + self.k**2

    def normalize(self):
        '''Returns the normalized quaternion.'''
        t = self.norm()
        if t != 1.0:
            return Quaternion(self.real/t, self.i/t, self.j/t, self.k/t)

    def conjugate_ip(self):
        '''Conjugates the quaternion in place.'''
        self.i *= -1
        self.j *= -1
        self.k *= -1
        return self

    def conjugate(self):
        '''Returns the conjugated quaternion.'''
        return Quaternion(self.real,-self.i,-self.j,-self.k)

    def inverse_ip(self):
        '''Inverts (in place) the quaternion with respect to multiplication.'''
        if not self.__bool__():
            raise ZeroDivisionError('It is not possible to invert the zero quaternion.')

        n = self.square_norm()
        self.real /= n
        self.i /= -n
        self.j /= -n
        self.k /= -n
        return self

    def inverse(self):
        '''Returns the inverse quaternion with respect to multiplication.'''
        if not self.__bool__():
            raise ZeroDivisionError('It is not possible to invert the zero quaternion.')

        n = self.square_norm()
        return Quaternion(self.real/n, -self.i/n, -self.j/n, -self.k/n)

    # Work in progress...
    # @staticmethod
    # def distance_L2(q1, q2):
    #     '''Returns the L2-distance, that is the norm-2, between two given (unitary) quaternions.'''
    #     return abs(q1-q2)

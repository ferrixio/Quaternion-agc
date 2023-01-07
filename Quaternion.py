#Quaternion object

class Quaternion:
    '''Ver 1.6.1'''

    #Initializer
    def __new__(cls, real_part:float=0, i_img:float=0, j_img:float=0, k_img:float=0, to_real:bool = False):
        '''Pre-generation of the quaternion.'''
        if i_img or j_img or k_img or not to_real:
            return super().__new__(cls)

        return real_part
        

    def __init__(self, real_part:float=0, i_img:float=0, j_img:float=0, k_img:float=0, to_real:bool = False) -> None:
        '''Quaternion's inputs:\n
        real_part   = real part of the number,
        i_img       = first imaginary part,
        j_img       = second imaginary part,
        k_img       = third imaginary part,
        to_real     = switch to create the quaternion as int|float.\n

        Remember that i**2 = j**2 = k**2 = ijk = -1\n

        The attributes of the quaternion are: real_part, i, j, k. The boolean to_real, if set to True, \
            returns an int|float if the quaternion is composed only by a real part.
        '''
        self.real_part, self.i, self.j, self.k = real_part, i_img, j_img, k_img


    
    #Type magic methods
    def __str__(self) -> str:
        '''Magic method to print a quaternion using print().'''
        ans = ''
        terms = {0:'', 1:'i', 2:'j', 3:'k'}

        for i,part in enumerate(self.components()):
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

    def __int__(self) -> int:
        '''Magic method to cast a quaternion to integer.'''
        return int(self.real_part)

    def __float__(self) -> float:
        '''Magic method to cast a quaternion to float.'''
        return float(self.real_part)



    #Unary operation magic methods
    def __pos__(self):
        '''Magic method to perform unary operation +object.'''
        return Quaternion(self.real_part,self.i,self.j,self.k)

    def __neg__(self):
        '''Magic method to perform the unary operation -object.'''
        return Quaternion(-self.real_part,-self.i,-self.j,-self.k)

    def __invert__(self):
        '''Magic method to get the inverse quaternion using ~.'''
        return self.inverse()

    def __abs__(self):
        '''Magic method to perform abs(). The absolute value of a quaternion is it's norm.'''
        return self.norm()

    def __round__(self, n:int=2):
        '''Magic method to round the decimals of every components of the quaternion.
        If n is not given, n = 2.'''
        return Quaternion(round(self.real_part,n), round(self.i,n), round(self.j,n), round(self.k,n))

    def __floor__(self):
        '''Magic method to round to the floor every components of the quaternion.'''
        return Quaternion(self.real_part.__floor__(),\
                    self.i.__floor__(), self.j.__floor__(), self.k.__floor__())

    def __ceil__(self):
        '''Magic method to round to the ceiling every components of the quaternion.'''
        return Quaternion(self.real_part.__ceil__(),\
                    self.i.__ceil__(), self.j.__ceil__(), self.k.__ceil__())


    
    #Binary operation magic methods
    def __add__(self, other):
        '''Magic method to emulate the left sum.'''
        if type(other) in (int, float):
            return Quaternion(self.real_part+other,self.i,self.j,self.k)

        return Quaternion(self.real_part+other.real_part,\
                    self.i+other.i, self.j+other.j, self.k+other.k)

    def __radd__(self, other):
        '''Magic method to emulate the right sum.'''
        if type(other) in (int, float):
            return Quaternion(other+self.real_part,self.i,self.j,self.k)

        return Quaternion(self.real_part+other.real_part,\
                    self.i+other.i, self.j+other.j, self.k+other.k)

    def __iadd__(self, other):
        '''Magic method to left-sum quaternions using +=.'''
        if type(other) in (int, float):
            self.real_part += other
            return self

        self.real_part += other.real_part
        self.i += other.i
        self.j += other.j
        self.k += other.k
        return self

    def __sub__(self, other):
        '''Magic method to emulate left subtraction.'''
        if type(other) in (int, float):
            return Quaternion(self.real_part-other,self.i,self.j,self.k)

        return Quaternion(self.real_part-other.real_part, \
                    self.i-other.i, self.j-other.j, self.k-other.k)

    def __rsub__(self, other):
        '''Magic method to emulate right subtraction.'''
        if type(other) in (int, float):
            return Quaternion(other-self.real_part,-self.i,-self.j,-self.k)

        return Quaternion(other.real_part-self.real_part, \
                    other.i-self.i, other.j-self.j, other.k-self.k)

    def __isub__(self, other):
        '''Magic method to subtract quaternions using -=.'''
        if type(other) in (int, float):
            self.real_part -= other
            return self

        self.real_part -= other.real_part
        self.i -= other.i
        self.j -= other.j
        self.k -= other.k
        return self

    def __mul__(self, other):
        '''Magic method to perform quaternionic left-multiplication x * y.'''
        if type(other) in (int, float):
            return Quaternion(self.real_part*other,self.i*other,self.j*other,self.k*other)

        new_real = self.real_part*other.real_part - self.i*other.i - self.j*other.j - self.k*other.k
        new_i = self.real_part*other.i + self.i*other.real_part + self.j*other.k - self.k*other.j
        new_j = self.real_part*other.j + self.j*other.real_part - self.i*other.k + self.k*other.i
        new_k = self.real_part*other.k + self.k*other.real_part + self.i*other.j - self.j*other.i

        return Quaternion(new_real,new_i,new_j,new_k)

    def __rmul__(self, other):
        '''Magic method to perform quaternionic right-multiplication y * x.'''
        if type(other) in (int, float):
            return Quaternion(self.real_part*other,self.i*other,self.j*other,self.k*other)

        new_real = self.real_part*other.real_part - self.i*other.i - self.j*other.j - self.k*other.k
        new_i = self.real_part*other.i + self.i*other.real_part - self.j*other.k + self.k*other.j
        new_j = self.real_part*other.j + self.j*other.real_part + self.i*other.k - self.k*other.i
        new_k = self.real_part*other.k + self.k*other.real_part - self.i*other.j + self.j*other.i

        return Quaternion(new_real,new_i,new_j,new_k)

    def __imul__(self, other):
        '''Magic method to perform quaternionic left-multiplication x *= y.'''
        if type(other) in (int, float):
            self.real_part *= other
            self.i *= other
            self.j *= other
            self.k *= other
            return self

        new_real = self.real_part*other.real_part - self.i*other.i - self.j*other.j - self.k*other.k
        new_i = self.real_part*other.i + self.i*other.real_part + self.j*other.k - self.k*other.j
        new_j = self.real_part*other.j + self.j*other.real_part - self.i*other.k + self.k*other.i
        new_k = self.real_part*other.k + self.k*other.real_part + self.i*other.j - self.j*other.i

        self.real_part = new_real
        self.i, self.j, self.k = new_i, new_j, new_k

        return self

    def __pow__(self, power):
        '''Magic method to implement int-exponentiation operation **, by applying left-multiplication.'''
        if type(power) is int:
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

        raise Exception('The power must be a positive or a negative integer.')

    def __ipow__(self, power):
        '''Magic method to implement int-exponentiation operation **=, by applying left-multiplication.'''
        if type(power) is int:
            if power < 0:
                self.inverse_ip()
                power *= -1

            if power:
                h = +self
                for _ in range(power-1):
                    self *= h

                return self

            self.real_part, self.i, self.j, self.k = 1, 0, 0, 0
            return self

        raise Exception('The power must be a positive or a negative integer.')
        
    def __truediv__(self, other):
        '''Magic method to perform quaternionic division x / y.'''
        if type(other) in (int, float):
            return Quaternion(self.real_part/other,\
                        self.i/other, self.j/other, self.k/other)

        return self.__mul__(~other)

    def __itruediv__(self, other):
        '''Magic method to perform quaternionic division x /= y.'''
        if type(other) in (int, float):
            self.real_part /= other
            self.i /= other
            self.j /= other
            self.k /= other
            return self

        return self.__imul__(~other)



    #Boolean magic methods
    def __eq__(self, other) -> bool:
        '''Checks if all the components between the two quaternions are the same.'''
        return self.real_part==other.real_part and self.i==other.i and self.j==other.j and self.k==other.k

    def __ne__(self, other) -> bool:
        '''Checks if one of the components between the two quaternions are different.'''
        return self.real_part!=other.real_part or self.i!=other.i or self.j!=other.j or self.k!=other.k

    def __bool__(self) -> bool:
        '''Checks if the quaternion is not zero.'''
        return bool(self.real_part or self.i or self.j or self.k)



    #Special functions to get quaternionic components
    def components(self) -> tuple:
        '''Returns a tuple with the four attributes of the quaternion.'''
        return (self.real_part,self.i,self.j,self.k)

    def norm(self) -> float:
        '''Returns the norm of the quaternion.'''
        from math import sqrt
        return sqrt(self.square_norm())

    def square_norm(self) -> float:
        '''Returns the square norm of the quaternion'''
        return self.real_part**2 + self.i**2 + self.j**2 + self.k**2

    def normalize(self):
        '''Returns the normalized quaternion.'''
        t = self.norm()
        return Quaternion(self.real_part/t, self.i/t, self.j/t, self.k/t)

    def is_unit(self) -> bool:
        '''Checks if the quaternion is unitary, that is, if it lies on the 3-sphere.'''
        return self.square_norm() == 1

    def is_real(self) -> bool:
        '''Checks if the quaternion is a real number.'''
        return not bool(self.i or self.j or self.k)

    def conjugate_ip(self):
        '''Conjugates the quaternion (in place).'''
        self.i *= -1
        self.j *= -1
        self.k *= -1
        return self

    def conjugate(self):
        '''Returns the conjugated quaternion.'''
        return Quaternion(self.real_part,-self.i,-self.j,-self.k)

    def inverse_ip(self):
        '''Inverts (in place) the quaternion with respect to multiplication.'''
        n = self.square_norm()
        self.real_part /= n
        self.i /= -n
        self.j /= -n
        self.k /= -n
        return self

    def inverse(self):
        '''Returns the inverse quaternion with respect to multiplication.'''
        n = self.square_norm()
        return Quaternion(self.real_part/n, -self.i/n, -self.j/n, -self.k/n)


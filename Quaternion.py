#Quaternion object

class Quaternion:
    '''Ver 1.0'''

    #Initializer
    def __init__(self, real_part:float=0, i_img:float=0, j_img:float=0, k_img:float=0) -> None:
        '''Quaternion's inputs:\n
        real_part   = real part of the number,
        i_img       = first imaginary part,
        j_img       = second imaginary part,
        k_img       = third imaginary part.\n

        Remember that i**2 = j**2 = k**2 = ijk = -1\n

        The attributes of the quaternion are: real_part, i, j, k.
        '''
        self.real_part, self.i, self.j, self.k = real_part, i_img, j_img, k_img


    
    #Type magic methods
    def __str__(self) -> str:
        '''Magic method to print a quaternion using print().'''
        return self.algebric_print()

    def algebric_print(self) -> str:
        '''Show the algebric form of the quaternion.'''
        ans = ''
        terms = {0:'', 1:'i', 2:'j', 3:'k'}

        for i,part in enumerate(self.components()):
            if not part:                                #coefficiente nullo -> non scrive
                pass
            elif part > 0 and i != 0:                   #coeff positivo e non in prima posizione
                ans += f'+{part}{terms[i]} '
            else:                                       #coeff negativo
                ans += f'{part}{terms[i]} '

        if not ans:
            return '0'

        del terms
        return ans
    


    #Unary operation magic methods
    def __pos__(self):
        '''Magic method to perform unary operation +object.'''
        return self

    def __neg__(self):
        '''Magic method to return the opposite quaternion with respect to the sum.'''
        return self*-1

    def __invert__(self):
        '''Magic method to get the inverse quaternion using ~.'''
        return self.inverse()

    def __abs__(self):
        '''Magic method to perform abs(). The absolute value of a quaternion is it's norm.'''
        return self.norm()

    def __round__(self, n:int=2):
        '''Magic method to round the decimals of every components of the quaternion.
        If n is not given, n = 2.'''
        self.real_part = round(self.real_part,n)
        self.i = round(self.i,n)
        self.j = round(self.j,n)
        self.k = round(self.k,n)

        return self

    def __floor__(self):
        '''Magic method to round to the floor every components of the quaternion.'''
        from math import floor
        self.real_part = floor(self.real_part)
        self.i = floor(self.i)
        self.j = floor(self.j)
        self.k = floor(self.k)

        return self

    def __ceil__(self):
        '''Magic method to round to the ceiling every components of the quaternion.'''
        from math import ceil
        self.real_part = ceil(self.real_part)
        self.i = ceil(self.i)
        self.j = ceil(self.j)
        self.k = ceil(self.k)

        return self


    
    #Binary operation magic methods
    def __add__(self, other):
        '''Magic method to sum quaternions using +.'''
        return Quaternion(self.real_part+other.real_part, self.i+other.i, self.j+other.j, self.k+other.k)

    def __iadd__(self, other):
        '''Magic method to sum quaternions using +=.'''
        self.real_part += other.real_part
        self.i += other.i
        self.j += other.j
        self.k += other.k

        return self

    def __sub__(self, other):
        '''Magic method to subtract quaternions using -.'''
        return Quaternion(self.real_part-other.real_part, self.i-other.i, self.j-other.j, self.k-other.k)

    def __isub__(self, other):
        '''Magic method to subtract quaternions using -=.'''
        self.real_part -= other.real_part
        self.i -= other.i
        self.j -= other.j
        self.k -= other.k

        return self

    def scalarProduct(self, number) -> tuple:
        '''Auxiliary function to get scalar multiplication.'''
        return self.real_part*number,self.i*number,self.j*number,self.k*number

    def __mul__(self, other):
        '''Magic method to perform quaternionic left-multiplication x * y.'''
        if type(other) in (int, float):
            new_real,new_i,new_j,new_k = self.scalarProduct(other)

        else:
            new_real = self.real_part*other.real_part - self.i*other.i - self.j*other.j - self.k*other.k
            new_i = self.real_part*other.i + self.i*other.real_part + self.j*other.k - self.k*other.j
            new_j = self.real_part*other.j + self.j*other.real_part - self.i*other.k + self.k*other.i
            new_k = self.real_part*other.k + self.k*other.real_part + self.i*other.j - self.j*other.i

        return Quaternion(new_real,new_i,new_j,new_k)

    def __rmul__(self, other):
        '''Magic method to perform quaternionic right-multiplication y * x.'''
        if type(other) in (int, float):
            new_real,new_i,new_j,new_k = self.scalarProduct(other) 

        else:
            new_real = self.real_part*other.real_part - self.i*other.i - self.j*other.j - self.k*other.k
            new_i = self.real_part*other.i + self.i*other.real_part - self.j*other.k + self.k*other.j
            new_j = self.real_part*other.j + self.j*other.real_part + self.i*other.k - self.k*other.i
            new_k = self.real_part*other.k + self.k*other.real_part - self.i*other.j + self.j*other.i

        return Quaternion(new_real,new_i,new_j,new_k)

    def __imul__(self, other):
        '''Magic method to perform quaternionic left-multiplication x *= y.'''
        if type(other) in (int, float):
            new_real,new_i,new_j,new_k = self.scalarProduct(other)

        else:
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
                for i in range(power):
                    h *= self

            elif power < 0:
                q = self.inverse()
                for i in range(-power):
                    h *= q

            return Quaternion(h.real_part, h.i, h.j, h.k)

        else:
            raise Exception('The power must be a positive or a negative integer.')

    def __ipow__(self, power):
        '''Magic method to implement exponentiation operation **=, by applying left-multiplication.'''
        if type(power) is int:
            h = Quaternion(1)

            if power > 0:
                for i in range(power):
                    h *= self

            elif power < 0:
                q = self.inverse()
                for i in range(-power):
                    h *= q

            self.real_part, self.i, self.j, self.k = h.real_part, h.i, h.j, h.k        
            return self

        else:
            raise Exception('The power must be a positive or a negative integer.')
        
    def __truediv__(self, other):
        '''Magic method to perform quaternionic division x / y.'''
        if type(other) in (int, float):
            div = 1/other
        else:
            div = ~other

        return self.__mul__(div)

    def __itruediv__(self, other):
        '''Magic method to perform quaternionic division x /= y.'''
        if any((type(other) is int, type(other) is float)):
            div = 1/other
        else:
            div = ~other
        return self.__imul__(div)



    #Boolean magic methods
    def __eq__(self, other) -> bool:
        '''Checks if all the components between the two quaternions are the same.'''
        return bool((self.real_part==other.real_part)*(self.i==other.i)*(self.j==other.j)*(self.k==other.k))

    def __ne__(self, other) -> bool:
        '''Checks if one of the components between the two quaternions are different.'''
        return not bool((self.real_part==other.real_part)*(self.i==other.i)*(self.j==other.j)*(self.k==other.k))

    def __bool__(self) -> bool:
        '''Checks if the quaternion is not zero.'''
        return not bool((self.real_part==0)*(self.i==0)*(self.j==0)*(self.k==0))



    #Special functions to get quaternionic components
    def components(self) -> tuple:
        '''Returns a tuple with the four attributes of the quaternion.'''
        return (self.real_part,self.i,self.j,self.k)

    def norm(self) -> float:
        '''Returns the norm of the quaternion.'''
        return (self.real_part**2 + self.i**2 + self.j**2 + self.k**2)**0.5

    def normalize(self):
        '''Returns the normalized quaternion.'''
        return Quaternion(self.real_part/self.norm(), self.i/self.norm(), self.j/self.norm(), self.k/self.norm())

    def is_unit(self) -> bool:
        '''Checks if the quaternion is unitary, that is, if it lies on the 3-sphere.'''
        return self.norm() == 1

    def conjugate(self):
        '''Conjugates the quaternion.'''
        self.i *= -1
        self.j *= -1
        self.k *= -1

        return self

    def inverse(self):
        '''Returns the inverse quaternion with respect to multiplication.'''
        n = self.norm()**2
        return Quaternion(self.real_part/n, -self.i/n, -self.j/n, -self.k/n)

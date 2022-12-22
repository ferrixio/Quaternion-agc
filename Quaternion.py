#Sviluppiamo i quaternioni ahah!!

class Quaternion:
    '''Classe che inizializza l'oggetto quaternione'''

    def __init__(self, real_part:float=0, i_img:float=0, j_img:float=0, k_img:float=0) -> None:
        '''Quaternion's inputs:\n
        real_part   = real part of the number\n
        i_img       = first imaginary part\n
        j_img       = second imaginary part\n
        k_img       = third imaginary part\n
        
        Remember that i**2 = j**2 = k**2 = ijk = -1
        '''
        self.real_part, self.i, self.j, self.k = real_part, i_img, j_img, k_img
        self.components = (real_part,i_img,j_img,k_img)
        self.norm = (self.real_part**2 + self.i**2 + self.j**2 + self.k**2)**0.5

    def __str__(self) -> str:
        return self.algebric_print()

    def algebric_print(self) -> str:
        '''Show the algebric form of the quaternion'''
        ans = ''
        terms = {0:'', 1:'i', 2:'j', 3:'k'}

        for i,part in enumerate(self.components):
            if not part:                               #coefficiente nullo -> non scrive
                pass
            elif part > 0 and i != 0:                   #coeff positivo e non in prima posizione
                ans += f'+{part}{terms[i]} '
            else:                                       #coeff negativo
                ans += f'{part}{terms[i]} '

        if not ans:
            return '0'

        del terms
        return ans


    def conjugate(self) -> None:
        '''Conjugates the quaternion'''
        self.i *= -1
        self.j *= -1
        self.k *= -1
        self.components = (self.real_part, -self.i, -self.j, -self.k)

    def normalize(self):
        '''Returns the normalized quaternion'''
        return Quaternion(self.real_part/self.norm, self.i/self.norm, self.j/self.norm, self.k/self.norm)

    def inverse(self):
        '''Returns the inverse quaternion'''
        n = self.norm()**2
        return Quaternion(self.real_part/n, -self.i/n, -self.j/n, -self.k/n)

    def is_unit(self) -> bool:
        '''Checks if the quaternion is unitary, that is, if it lies on the 3-sphere'''
        return self.norm == 1


#Operazioni di corpo
def inner_sum(*quaternions:Quaternion) -> Quaternion:
    '''Returns the quaternionic inner sum'''
    new_real, new_i, new_j, new_k = 0,0,0,0
    for q in quaternions:
        new_real += q.real_part
        new_i += q.i
        new_j += q.j
        new_k += q.k

    return Quaternion(new_real, new_i, new_j, new_k)

def left_product(*quaternions:Quaternion) -> Quaternion:
    '''Returns the quaternionic left-multiplication'''
    new_real, new_i, new_j, new_k = quaternions[0].real_part, quaternions[0].i, quaternions[0].j, quaternions[0].k
    for item in quaternions[1:]:
        new_real = new_real*item.real_part - new_i*item.i - new_j*item.j - new_k*item.k
        new_i = new_real*item.i + new_i*item.real_part + new_j*item.k - new_k*item.j
        new_j = new_real*item.j + new_j*item.real_part - new_i*item.k + new_k*item.i
        new_k = new_real*item.k + new_k*item.real_part + new_i*item.j - new_j*item.i

    return Quaternion(new_real,new_i,new_j,new_k)

def right_product(*quaternions:Quaternion) -> Quaternion:
    '''Returns the quaternionic right-multiplication'''
    new_real, new_i, new_j, new_k = quaternions[0].real_part, quaternions[0].i, quaternions[0].j, quaternions[0].k
    for item in quaternions[1:]:
        new_real = new_real*item.real_part - new_i*item.i - new_j*item.j - new_k*item.k
        new_i = new_real*item.i + new_i*item.real_part - new_j*item.k + new_k*item.j
        new_j = new_real*item.j + new_j*item.real_part + new_i*item.k - new_k*item.i
        new_k = new_real*item.k + new_k*item.real_part - new_i*item.j + new_j*item.i

    return Quaternion(new_real,new_i,new_j,new_k)



# if __name__ == "__main__":
#     q = Quaternion(3,0,-1,0)
#     h = Quaternion(1,1,1,1)
#     print(f'q = {q.algebric_print()}\tnorma = {q.norm}')
#     print(f'h = {h.algebric_print()}\tnorma = {h.norm}')

#     print(f'q+h = {inner_sum(q,h).algebric_print()}')
#     print(f'q*h = {left_product(q,h).algebric_print()}')
#     print(f'h*q = {right_product(q,h).algebric_print()}')

x = Quaternion(1,2,3)
print(x:=1+3j,~x)


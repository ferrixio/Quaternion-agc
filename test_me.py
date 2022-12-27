from Quaternion import Quaternion

x = Quaternion(1,2,3,-4)
y = Quaternion(1,-1,1)

print(bool(y))
print(f'x*y = {x*y}\ny*x = {y*x}')
print(f'x+y = {x+y}\nx-y = {x-y}')
print(f'x/y = {x/y}\nx**2 = {x**2}')
print(f'x^-1 = {round(x.inverse(),4)} = ~x = {round(~x,4)}')
print(f'x.conj() = {x.conjugate()}')
print(f'x.norm() = {x.norm()} = abs(x) = {abs(x)}')
print(f'x*4.1 = {x*4.1}')

x *= y
print(f'x *= y: {x}')
print(f'is_unit(y): {y.is_unit()}\nnorm(y): {y.norm()}\nnormalize(y): {y.normalize()}')
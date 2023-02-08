from Quaternion import Quaternion

x = Quaternion(2,1,1,0)
y = Quaternion(1,-1,1,4)
z = Quaternion(0)

print(x, type(x), repr(x))
print(y, bool(y))
print(z, bool(z))

d = Quaternion(-3)
print(f'{d} is real = {d.is_real()}')

print(f'x-1 = {x-1}\nx+1 = {x+1}')
print(f'x*y = {x*y}\ny*x = {y*x}')
print(f'x+y = {x+y}\nx-y = {x-y}')
print(f'x/y = {x/y}\nx**2 = {x**2}\nx**-2 = {x**-2}')
print(f'x^-1 = {round(x.inverse(),4)} = ~x = {round(~x,4)}')
print(f'x.conj() = {x.conjugate()}')
print(f'x.norm() = {x.norm} = abs(x) = {abs(x)}')
print(f'x*4.1 = {x*4.1}')

h,z = +x,+x
h **= 3
z **= -3
print(f'x **= 3: {h}\nx **= -3: {z}')
x *= y
print(f'x *= y: {x}')
print(f'is_unit(y): {y.is_unit()}\nnorm(y): {y.norm}\nnormalize(y): {y.normalize()}')

print(f'h inverse_ip = {h.inverse_ip()}')
print(f'h conjugate_ip = {h.conjugate_ip()}')

c = Quaternion(seq=[1,3,7,-2])
c //= 2
print(f'x//2 : {c}\nx.norm: {c.norm}')

c = Quaternion.randint()
d = c.inverse()
print(f'c = {c}\nc^-1 = {d}\nc*d = {c*d}\nd*c = {d*c}')

x = Quaternion(3,3,3,3)
y = x % 3
z = x // 3
w = x @ 3
print(f'x = {x}\nx % 3 = {y}\nx // 3 = {z}\nx @ 3 = {w}\nnorm(x @ 3) = {w.norm}')
print(f'x ~ x//3 in HP1? {x.normalize()==z.normalize()}')
print(f'x ~ x@3 in HP1? {x.normalize()==w.normalize()}')

x = Quaternion(1,2,3,4)
y = Quaternion(2,1,3,4)
print(f'x.rotation = {x.rotation}\ny.rotation = {y.rotation}')

r = Quaternion.from_rotation(112, 1,2,3)
print(f'from_rotation(112,1,2,3) = {r}')
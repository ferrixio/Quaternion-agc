from Quaternion import Quaternion
from Hplot import Hplot

L = []
for i in range(100):
    L.append(Quaternion.random())

K = Hplot(L)
# K.plot()
# K.distplot()
K.pathplot()
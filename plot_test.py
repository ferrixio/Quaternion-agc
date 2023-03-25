from Quaternion import Quaternion
from Hplot import Hplot

L = [Quaternion.random() for _ in range(50)]

Hplot.pathplot(L)
# Hplot.plot(L)
# Hplot.distplot(L)
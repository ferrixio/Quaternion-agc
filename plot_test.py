from Quaternion import Quaternion
from Hplot import Hplot
from multiprocessing import Process,freeze_support

if __name__ == '__main__':
    freeze_support()
    L = [Quaternion.random() for _ in range(50)]
    r = Process(target=Hplot.pathplot, args=(L,))
    r.start()
    s = Process(target=Hplot.plot, args=(L,))
    s.start()
    t = Process(target=Hplot.distplot, args=(L,))
    t.start()
    t.join()
    r.join()
    s.join()
    print("END")
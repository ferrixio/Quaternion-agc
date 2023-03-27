from Quaternion import Quaternion
from Hplot import Hplot
from multiprocessing import Process

if __name__ == '__main__':
    
    L = [Quaternion.random() for _ in range(50)]+[Quaternion(0,0,0,1)]
#     L = [Quaternion(0,1), Quaternion(0,0,1,0), Quaternion(0,0,0,1), Quaternion(0,1,1,0),
#          Quaternion(0,0,1,1), Quaternion(0,1,1,1), Quaternion(0,1,0,1), Quaternion()]
    
#     r = Process(target=Hplot.pathplot, args=(L,))
#     r.start()
#     s = Process(target=Hplot.plot, args=(L,))
#     s.start()
#     t = Process(target=Hplot.distplot, args=(L,))
#     t.start()
#     t.join()
#     r.join()
#     s.join()

    # Hplot.pathplot(L)
    Hplot.stereo_pjrN(L)
    # Hplot.stereo_prjS(L)
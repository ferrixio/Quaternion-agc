# Quaternion plotting class for python 3.10

# Author:       Samuele Ferri (@ferrixio)
# Licence:      MIT 2025

from Quaternion import Quaternion
import matplotlib.pyplot as plt
from numpy import arange, linspace
from matplotlib.colors import hsv_to_rgb
from typing import Iterable
from math import inf, ceil, sqrt
from functools import wraps


'''Class to plot quaternions.

Quaternions are objects of a 4-dimensional space and therefore is difficult to
plot. So, we must use different approaches.

The class does not expect initializers. Every time a method is called, it checks the input
with a decorator and extracts the necessary colors to paint the graph.    
'''

## Decorator
def __are_quaternions(func):
    '''Decorator to check for invalid input.'''
    
    @wraps(func)
    def typo(quaternions, *args, **kw):
        if not isinstance(quaternions,Iterable):
            raise TypeError("Invalid type in input: first argument must be an Iterable of Quaternion objects")
        if not len(quaternions):
            raise TypeError('Invalid type in input: Iterable must contain at least one Quaternion object')
        if not all(isinstance(item, Quaternion) for item in quaternions):
            raise ValueError('Invalid type in input: Iterable must contain only Quaternion objects')
        
        return func(quaternions, *args, **kw)
    return typo


## Useful methods
def __getColors(H_points:Iterable[Quaternion], rainbow:bool=True):
    '''Returns a list of colors to paint the plot.
    
    Arguments:
    - H_point: iterable of quaternions
    - rainbow[bool]: get rainbow color to the set of points
    '''
    if rainbow:
        color_max = ceil(max(max(list(item.q for item in H_points), key=max)))
        c_list = tuple((t/color_max+1)/2 for t in [item.real for item in H_points])
        return (hsv_to_rgb((c,1,1)) for c in c_list)
    
    dt = 1/len(H_points)
    new_color = 0
    c_list = []
    for _ in H_points:
        c_list.append([new_color,0,0])
        new_color += dt
    return c_list
    
def __distance(a:Quaternion, b:Quaternion) -> float:
    '''Returns the euclidean distance between two quaternions.'''
    return (a.real-b.real)**2 + (a.i-b.i)**2 + (a.j-b.j)**2 + (a.k-b.k)**2

def __getPicture():
    '''Returns the figure where points will be drawn.'''
    pic = plt.figure().add_subplot(projection='3d')
    pic.set_xlabel('i axis')
    pic.set_ylabel('j axis')
    pic.set_zlabel('k axis')
    return pic

def __stereo_prj_S3(number:Quaternion, north:bool=True):
    '''Evaluates the stereographic projection of a given quaternion, which is the stereographic
    projection from S^3 to R^3.
    
    Arguments:
    - number[Quaternion]: the quaternion to be projected
    - south[bool]: if set to false, the projection will be evaluate from south pole
    '''
    if number==Quaternion(0,0,0,1) and north:
        raise ZeroDivisionError("Can't map the north pole using north-stereographic projection.")
    if number==Quaternion(0,0,0,-1) and not north:
        raise ZeroDivisionError("Can't map the south pole using south-stereographic projection.")

    temp = number.normalize()
    mod = (1-temp.k)*(north) + (1+temp.k)*(not north)
    return [temp.real/mod, temp.i/mod, temp.j/mod]

def __stereo_prj_S2(number:list[float], north:bool=True):
    '''Evaluates the stereographic projection from S^2 to R^2.
    
    Arguments:
    - number[list[float]]: the point in 3D to be projected
    - south[bool]: if set to false, the projection will be evaluate from south pole
    '''
    if number==[0,0,1] and north:
        raise ZeroDivisionError("Can't map the north pole using north-stereographic projection.")
    if number==[0,0,-1] and not north:
        raise ZeroDivisionError("Can't map the south pole using south-stereographic projection.")

    mod = sqrt(pow(number[0],2) + pow(number[1],2) + pow(number[2],2))
    number = [i/mod for i in number]
    den = 1 + ((-1)**north)*number[2]

    return [number[0]/den, number[1]/den]

def __stereo_prj_S1(number:list[float], north:bool=True):
    '''Evaluates the stereographic projection from S^1 to R.
    
    Arguments:
    - number[list[float]]: the point in 2D to be projected
    - south[bool]: if set to false, the projection will be evaluate from south pole
    '''
    if number==[0,1] and north:
        raise ZeroDivisionError("Can't map the north pole using north-stereographic projection.")
    if number==[0,-1] and not north:
        raise ZeroDivisionError("Can't map the south pole using south-stereographic projection.")

    return number[0]/(1 + ((-1)**north)*number[1])


def getPaths(H_points:Iterable[Quaternion]) -> list:
    '''Get the connections among quaternions.
    
    It returns a len(H_points)^2 matrix of 'None's, in which the number 1 in position (i,j)
    represents the link between the i-th and j-th quaternion in the H_points list.
    
    Argument:
    - H_points: an iterable of quaternions
    '''
    length = len(H_points)
    big_links = [[None for _ in range(length)] for _ in range(length)]
    for i in range(length):
        dist = tuple(__distance(H_points[i],H_points[k]) if k!=i else inf for k in range(length))
        minimum = min(dist)
        rep = [k for k in range(length) if dist[k]==minimum]
        for j in rep:
            big_links[i][j] = 1

    return big_links



## Plot functions
@__are_quaternions
def Hplot(H_points:Iterable[Quaternion], /, colored:bool=True):
    '''Draws a 3-dimensional graph of the list of given quaternion.
    
    The three imaginary parts are the coordinates in R3, while the real part determines
    the color of the point.

    Arguments:
    - H_points: an iterable of quaternions
    - colored[bool]: if set to false, the graph will be graduated from black to red
    '''
    ax = __getPicture()
    Colors = __getColors(H_points,colored)
    
    for t,col in zip(H_points, Colors):
        ax.plot(t.i, t.j, t.k, marker='o', c=col)

    plt.show()


@__are_quaternions
def distplot(H_points:Iterable[Quaternion]):
    '''Draws a bar graph of the minimum distances between quaternions, ordered
    according to the order of points in input.

    Arguments:
    - H_points: an iterable of quaternions
    '''
    ans = []
    for i in range(len(H_points)):
        a = H_points[i]
        dist = []
        for j in range(len(H_points)):
            if j != i:
                b = H_points[j]
                dist.append(__distance(a,b))

        ans.append(min((*dist,inf)))

    plt.bar(arange(1,len(H_points)+1,1), ans)
    plt.show()


@__are_quaternions
def pathplot(H_points:Iterable[Quaternion], /, colored:bool=True):
    '''Draws a 3-dimensional graph of the list of quaternion, connected according to
    the minimum mutual distances.
    
    The three imaginary parts are the coordinates in R3, while the real part determines
    the color of the point.

    Arguments:
    - H_points: an iterable of quaternions
    - colored[bool]: if set to false, the graph will be graduated from black to red
    '''
    Colors = __getColors(H_points,colored)
    ax = __getPicture()
    
    # Plotting the (colored) points
    for item, col in zip(H_points, Colors):
            ax.plot(item.i, item.j, item.k, 'o', c=col)

    # Adding the links among points
    for item in H_points:
        dist = tuple(__distance(item,k) if k!=item else inf for k in H_points)
        minimum = min(dist)
        repet = (k for k in range(len(dist)) if dist[k]==minimum)
        
        for p in repet:
            dx = H_points[p]
            ax.plot([item.i,dx.i], [item.j,dx.j], [item.k,dx.k], 'black', linestyle='-')

    plt.show()


@__are_quaternions
def stereo_pjrN(H_points:Iterable[Quaternion], /):
    '''Draws a 3-dimensional graph of the given list of quaternions according to the
    stereographic projection from the north pole of the 3-sphere, that is the point (0,0,0,1).
    
    Arguments:
    - H_points: iterable of quaternions
    '''
    ax = __getPicture()
    for item in H_points:
        ax.plot(*__stereo_prj_S3(item,True), 'o', c='red')

    plt.show()


@__are_quaternions
def stereo_prjS(H_points:Iterable[Quaternion], /):
    '''Draws a 3-dimensional graph of the given list of quaternions according to the
    stereographic projection from the south pole of the 3-sphere, that is the point (0,0,0,-1).
    
    Arguments:
    - H_points: iterable of quaternions
    '''
    ax = __getPicture()
    for item in H_points:
        ax.plot(*__stereo_prj_S3(item,False), 'o', c='red')

    plt.show()
    

@__are_quaternions
def stereo_432(H_points:Iterable[Quaternion], poles:Iterable[str]=('North','North')):
    '''Draws a 2-dimensional graph of the given list of quaternions according to a
    double stereographic projection from H to R^2.
    By default it projects twice from north pole, but you can change with the argument
    'poles'.
    
    Arguments:
    - H_points: iterable of quaternions
    - poles: iterable (of strings) of the poles of the two projections
    '''

    _poles = []
    for s in poles:
        if s in ('North', 'north', 'N', 'n'):
            _poles.append(True)
        elif s in ('South', 'south', 'S', 's'):
            _poles.append(False)
        else:
            raise AttributeError(f'Poles `{s}` is not a valid pole.')
    
    if len(_poles) != 2:
        raise ValueError(f'Wrong length list of poles: it is {len(_poles)} instead of 2.')

    R2 = [__stereo_prj_S2(__stereo_prj_S3(i, _poles[0]), _poles[1]) for i in H_points]
    xx = [p[0] for p in R2]
    yy = [p[1] for p in R2]

    plt.figure()
    plt.plot(xx, yy, '*')
    plt.show()


@__are_quaternions
def imagy_stereo(H_points:Iterable[Quaternion], poles:Iterable[str]=('North','North')):
    '''Draws a graph (x, f(x)) of the given list of quaternions, where
    - x: real part of the quaternion,
    - f(x): double stereographic projection of the imaginary part of the quaternion.

    By default it projects twice from north pole, but you can change with the argument `poles`.

    @Arguments:
    - H_points: iterable of quaternions
    - poles: iterable (of strings) of the poles of the three projections
    '''

    _poles = []
    for s in poles:
        if s in ('North', 'north', 'N', 'n'):
            _poles.append(True)
        elif s in ('South', 'south', 'S', 's'):
            _poles.append(False)
        else:
            raise AttributeError(f'Poles `{s}` is not a valid pole.')
        
    if len(_poles) != 2:
        raise ValueError(f'Wrong length list of poles: it is {len(_poles)} instead of 2.')
    
    real_parts = [i.real for i in H_points]
    R = [__stereo_prj_S1(__stereo_prj_S2(i.vector, _poles[0]), _poles[1]) for i in H_points]

    plt.figure()
    plt.plot(real_parts, R, '*')
    plt.show()


@__are_quaternions
def stereo_4321(H_points:Iterable[Quaternion], poles:Iterable[str]=('North','North','North')):
    '''Draws a 1-dimensional graph of the given list of quaternions according to a
    triple stereographic projection from H to R.
    By default it projects trice from north pole, but you can change with the argument
    'poles'.
    
    Arguments:
    - H_points: iterable of quaternions
    - poles: iterable (of strings) of the poles of the two projections
    '''

    _poles = []
    for s in poles:
        if s in ('North', 'north', 'N', 'n'):
            _poles.append(True)
        elif s in ('South', 'south', 'S', 's'):
            _poles.append(False)
        else:
            raise AttributeError(f'Poles `{s}` is not a valid pole.')
    
    if len(_poles) != 3:
        raise ValueError(f'Wrong length list of poles: it is {len(_poles)} instead of 3.')

    R1 = [__stereo_prj_S1(__stereo_prj_S2(__stereo_prj_S3(i, _poles[0]), _poles[1]), _poles[2]) for i in H_points]

    xx = linspace(0,1,len(R1))
    plt.figure()
    plt.plot(xx, R1, '*')
    plt.show()

# End of Hplot class
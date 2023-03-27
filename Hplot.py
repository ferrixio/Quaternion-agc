# Quaternion plotting class for python 3.11

# Author:     Samuele Ferri (@ferrixio)
# Version:    2.2.2

from Quaternion import Quaternion
import matplotlib.pyplot as plt
from numpy import arange
from matplotlib.colors import hsv_to_rgb
from typing import Iterable
from math import inf, ceil
from functools import wraps

class Hplot:
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
        pic.set_xlabel('i')
        pic.set_ylabel('j')
        pic.set_zlabel('k')
        return pic
    
    def __stereo_prj(number:Quaternion, north:bool=True):
        '''Evaluates the stereographic projection of a given quaternion.
        
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


    ## Plot functions
    @__are_quaternions
    def plot(H_points:Iterable[Quaternion], /, colored:bool=True):
        '''Draws a 3-dimensional graph of the list of given quaternion.
        
        The three imaginary parts are the coordinates in R3, while the real part determines
        the color of the point.

        Arguments:
        - H_points: iterable of quaternions
        - colored[bool]: if set to false, the graph will be graduated from black to red
        '''
        ax = Hplot.__getPicture()
        Colors = Hplot.__getColors(H_points,colored)
        
        for t,col in zip(H_points, Colors):
            ax.plot(t.i, t.j, t.k, marker='o', c=col)

        plt.show()


    @__are_quaternions
    def distplot(H_points:Iterable[Quaternion]):
        '''Draws a bar graph of the minimum distances between quaternions, ordered
        according to the order of points in input.

        Arguments:
        - H_points: iterable of quaternions
        '''
        ans = []
        for i in range(len(H_points)):
            a = H_points[i]
            dist = []
            for j in range(len(H_points)):
                if j != i:
                    b = H_points[j]
                    dist.append(Hplot.__distance(a,b))

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
        - H_points: iterable of quaternions
        - colored[bool]: if set to false, the graph will be graduated from black to red
        '''
        ax = Hplot.__getPicture()
        Colors = Hplot.__getColors(H_points,colored)
        
        for item, col in zip(H_points, Colors):
                ax.plot(item.i, item.j, item.k, 'o', c=col)

        for item in H_points:
            dist = tuple(Hplot.__distance(item,k) if k!=item else inf for k in H_points)
            minimum = min(dist)
            repet = (k for k in range(len(dist)) if dist[k]==minimum)
            
            for p in repet:
                dx = H_points[p]
                ax.plot([item.i,dx.i], [item.j,dx.j], [item.k,dx.k], 'black', linestyle='-')

        plt.show()


    @__are_quaternions
    def stereo_pjrN(H_points:Iterable[Quaternion], /):
        '''Draws a 3-dimensional graph of the given list of quaternion according to the
        stereographic projection from the north pole of the 3-sphere, that is the point (0,0,0,1).
        
        Arguments:
        - H_points: iterable of quaternions
        '''
        ax = Hplot.__getPicture()
        for item in H_points:
            ax.plot(*Hplot.__stereo_prj(item,True), 'o', c='red')

        plt.show()
    

    @__are_quaternions
    def stereo_prjS(H_points:Iterable[Quaternion], /):
        '''Draws a 3-dimensional graph of the given list of quaternion according to the
        stereographic projection from the south pole of the 3-sphere, that is the point (0,0,0,-1).
        
        Arguments:
        - H_points: iterable of quaternions
        '''
        ax = Hplot.__getPicture()
        for item in H_points:
            ax.plot(*Hplot.__stereo_prj(item,False), 'o', c='red')

        plt.show()
    


# End of Hplot class
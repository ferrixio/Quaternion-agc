# Quaternion plotting class for python 3.11

# Author:     Samuele Ferri (@ferrixio)
# Version:    1.1

from Quaternion import Quaternion
import matplotlib.pyplot as plt
from numpy import arange
from matplotlib.colors import hsv_to_rgb
from typing import Iterable
from math import inf, ceil, sqrt


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
        def typo(args, **kw):
            if not len(args):
                raise TypeError('Missing arguments')
            if not all(isinstance(item, Quaternion) for item in args):
                raise ValueError('Invalid type in input: iterable must be of type Quaternion')
            return func(args, **kw)
        
        return typo
    

    ## Useful methods
    def __get_Colors(H_points:Iterable[Quaternion], rainbow:bool):
        '''Returns a list of colors to paint the plot.'''

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
        
    @staticmethod
    def __distance(a:Quaternion,b:Quaternion) -> float:
        '''Returns the euclidean distance between two quaternions.'''
        d = (a.real-b.real)**2 + (a.i-b.i)**2 + (a.j-b.j)**2 + (a.k-b.k)**2
        return sqrt(d)



    # Standard plot in 4D = 3D + color
    @__are_quaternions
    def plot(H_points:Iterable[Quaternion], colored:bool=True):
        '''Draws a 3-dimensional graph of the list of given quaternion.
        
        The three imaginary parts are the coordinates in R3, while the real part determines
        the color of the point.

        Arguments:
        - H_points: iterable of quaternions
        - colored[bool]: if set to false, the graph will be graduated from black to red
        '''
        Colors = Hplot.__get_Colors(H_points,colored)

        fig = plt.figure()
        ax = fig.add_subplot(projection='3d')
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
    def pathplot(H_points:Iterable[Quaternion], colored:bool=True):
        '''Draws a 3-dimensional graph of the list of quaternion, connected according to
        the minimum mutual distances.
        
        The three imaginary parts are the coordinates in R3, while the real part determines
        the color of the point.

        Arguments:
        - H_points: iterable of quaternions
        - colored[bool]: if set to false, the graph will be graduated from black to red
        '''
        fig = plt.figure()
        ax = fig.add_subplot(projection='3d')

        Colors = Hplot.__get_Colors(H_points,colored)
        
        for item, col in zip(H_points, Colors):
                ax.plot(item.i, item.j, item.k, 'o', c=col)

        for item in H_points:
            dist = tuple(Hplot.__distance(item,k) if k!=item else inf for k in H_points)
            p = dist.index(min(dist))
            dx = H_points[p]
            plt.plot([item.i,dx.i], [item.j,dx.j], [item.k,dx.k], 'black', linestyle='-')

        plt.show()


# End of the class
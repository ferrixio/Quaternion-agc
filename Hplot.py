# Quaternion plotting class for python 3.11

# Author:     Samuele Ferri (@ferrixio)
# Version:    1.0

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

    Attributes:
    - points: list of quaternion to be plotted
    - colors: list of colors (sorted according to points' order) to paint the points
    '''


    def __new__(cls, points:Iterable[Quaternion]):
        '''Checking the input'''
        if not len(points):
            raise TypeError('Missing arguments')

        return super().__new__(cls)


    def __init__(self, H_points:Iterable[Quaternion]):
        '''Initializer of graph object.
        
        Input:
        - H_points: list of quaternion
        '''
        self.points = tuple(H_points)
        color_max = ceil(max(max(list(item.q for item in H_points), key=max)))
        self.colors = tuple((t/color_max+1)/2 for t in [item.real for item in self.points])
    

    # Standard plot in 4D = 3D + color
    def plot(self):
        '''Draws a 3-dimensional graph of the list of given quaternion.
        
        The three imaginary parts are the coordinates in R3, while the real part determines
        the color of the point.
        '''
        fig = plt.figure()
        ax = fig.add_subplot(projection='3d')
        for t,c in zip(self.points, self.colors):
            ax.plot(t.i, t.j, t.k, marker='o', c=hsv_to_rgb((c,1,1)))

        plt.show()


    @staticmethod
    def distance(a:Quaternion,b:Quaternion) -> float:
        '''Returns the euclidean distance between two quaternions.'''
        d = (a.real-b.real)**2 + (a.i-b.i)**2 + (a.j-b.j)**2 + (a.k-b.k)**2
        return sqrt(d)

    def distplot(self):
        '''Draws a bar graph of the minimum distances between quaternions, ordered
        according to the order in self.points.
        '''
        ans = []
        for i in range(len(self.points)):
            a = self.points[i]
            dist = []
            for j in range(len(self.points)):
                if j != i:
                    b = self.points[j]
                    dist.append(self.distance(a,b))

            ans.append(min((*dist,inf)))

        plt.bar(arange(1,len(self.points)+1,1), ans)
        plt.show()


    def pathplot(self, colored=True):
        '''Draws a 3-dimensional graph of the list of quaternion, connected according to
        the minimum mutual distances.
        
        The three imaginary parts are the coordinates in R3, while the real part determines
        the color of the point.

        Optional variable:
        - colored[bool]: if set to false, the graph will be graduated from black to red
        '''
        fig = plt.figure()
        ax = fig.add_subplot(projection='3d')
        
        if colored:
            for item, c in zip(self.points, self.colors):
                ax.plot(item.i, item.j, item.k, 'o', c=hsv_to_rgb((c,1,1)))
        else:
            dt = 1/len(self.points)
            new_color = 0
            for item in self.points:
                ax.plot(item.i, item.j, item.k, 'o', c=[new_color,0,0])
                new_color += dt

        for item in self.points:
            dist = tuple(self.distance(item,k) if k!=item else inf for k in self.points)
            p = dist.index(min(dist))
            dx = self.points[p]
            plt.plot([item.i,dx.i], [item.j,dx.j], [item.k,dx.k], 'black', linestyle='-')

        plt.show()


# End of the class
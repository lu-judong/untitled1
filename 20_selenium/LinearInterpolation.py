# -*- coding: utf-8 -*-
"""
Created on Tue Apr 30 10:18:32 2019

@author: Administrator
"""

from scipy import interpolate

class interpolate_standard():
    def interpolation(self,x1,x2,y1,y2,newx):
        """
        return None if error happened, otherwise would return the interpolated value.
        :param x1:
        :type x1:
        :param x2:
        :type x2:
        :param y1:
        :type y1:
        :param y2:
        :type y2:
        :param newx:
        :type newx:
        :return:
        :rtype:
        """
        # x = np.linspace(0, 10, 11)
        x = [x1,x2]
        y = [y1,y2]
        # x=[  0.   1.   2.   3.   4.   5.   6.   7.   8.   9.  10.]
        # y = np.sin(x)
        xnew = [newx]
        # xnew = np.linspace(0, 10, 10)
        f = interpolate.interp1d(x, y, kind='linear',fill_value="extrapolate")
        try:
            ynew = f(xnew)
        except Exception as e:
            ynew=[None]
        return ynew[0]
    
    
r1 = interpolate_standard().interpolation(0,16,1565435,1594096,4)
print(r1)
r2 = interpolate_standard().interpolation(0,34,1594096,1655002,13)
print(r2)
r = r2 - r1
print(r)


#d1 = interpolate_standard().interpolation(1565435,1594096,0,16,7165.25)
#print(d1)
#d2 = interpolate_standard().interpolation(1594096,1655002,0,34,23287)
#print(d2)
#d = d2 - d1
#print(d)
import abc
import numpy as np
from itertools import product, ifilter, izip

class Rotateable():
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def points(self): 
        " Return contructable points in a list. "
        pass

    @abc.abstractmethod
    def set_points(self, points):
        " Construct shape from list of points. "
        pass


    def rotate3D(self, r_angles, origin=np.array([0.0,0.0,0.0])):
        " Rotate the shape by [x,y,z] degrees about origin of [x,y,x]. "
        r_rads = r_angles * np.pi / np.float(180.0)
        x_rot = np.mat([ [                1.0,                0.0,                0.0]
                       , [                0.0,  np.cos(r_rads[0]), -np.sin(r_rads[0])]
                       , [                0.0,  np.sin(r_rads[0]),  np.cos(r_rads[0])]
                       ])
        y_rot = np.mat([ [  np.cos(r_rads[1]),                 0.0,  np.sin(r_rads[1])]
                       , [                0.0,                 1.0,                0.0]
                       , [ -np.sin(r_rads[1]),                 0.0,  np.cos(r_rads[1])]
                       ])
        z_rot = np.mat([ [  np.cos(r_rads[2]), -np.sin(r_rads[2]),                 0.0]
                       , [  np.sin(r_rads[2]),  np.cos(r_rads[2]),                 0.0]
                       , [                0.0,                0.0,                 1.0]
                       ])
        rot_matrix = x_rot * y_rot * z_rot
        new_points = [ origin + (point - origin) * rot_matrix for point in self.points() ]
        self.set_points(new_points)
        return self

class Line(Rotateable):
    def __init__(self, A, B):
        self.A = np.array(A)
        self.B = np.array(B)

    def set_points(self, points):
        self.__init__(points[0], points[1])
        return self

    def shift(self, offset):
        self.__init__( self.A + offset
                     , self.B + offset
                     )
        return self

    def points(self):
        return [self.A, self.B]

    def fill(self, N=4):
        vec = self.B - self.A
        return [self.A + vec * ii for ii in np.linspace(0,1,N)]


class Tri(Rotateable):
    def __init__(self, A, B, C):
        self.A = np.array(A)
        self.B = np.array(B)
        self.C = np.array(C)

        self.AB = self.B - self.A
        self.AC = self.C - self.A

    def set_points(self, points):
        self.__init__(points[0], points[1], points[2])
        return self

    def shift(self, offset):
        self.__init__( self.A + offset
                     , self.B + offset
                     , self.C + offset
                     )
        return self

    def points(self):
        return [self.A, self.B, self.C]

    def point_in_plane(self, u, v):
        return self.A + u * self.AC + v * self.AB

    def point_in_triangle(self, p):
        v0 = self.AC
        v1 = self.AB
        v2 = np.array(p) - self.A

        dot00 = np.dot(v0, v0)
        dot01 = np.dot(v0, v1)
        dot02 = np.dot(v0, v2)
        dot11 = np.dot(v1, v1)
        dot12 = np.dot(v1, v2)

        invDenom = (dot00 * dot11 - dot01 * dot01)
        u = (dot11 * dot02 - dot01 * dot12) / invDenom
        v = (dot00 * dot12 - dot01 * dot02) / invDenom

        return (u >= 0) and (v >= 0) and (u + v <= 1)


    def fill(self, N=4):
        us = np.linspace(0,1,N)
        vs = np.linspace(0,1,N)

        new_points = [ self.point_in_plane(u,v) 
                       for (u,v) in product(us, vs) 
                       if u + v <= 1.0 
                     ]

        return new_points

    def __repr__(self):
        return "{},{},{}".format(self.A, self.B, self.C)


class Tetrahedron(Rotateable):
    def __init__(self, A, B, C, D):
        self.A = np.array(A)
        self.B = np.array(B)
        self.C = np.array(C)
        self.D = np.array(D)

        self.AB = self.B - self.A
        self.AC = self.C - self.A
        self.AD = self.D - self.A

    def set_points(self, points):
        self.__init__(points[0], points[1], points[2], points[3])
        return self

    def shift(self, offset):
        self.__init__( self.A + offset
                     , self.B + offset
                     , self.C + offset
                     , self.D + offset
                     )
        return self

    def points(self):
        return [self.A, self.B, self.C, self.D]

    def point_in_space(self, u, v, w):
        return self.A + u * self.AC + v * self.AB + w * self.AD


    def fill(self, N=4):
        us = np.linspace(0,1,N)
        vs = np.linspace(0,1,N)
        ws = np.linspace(0,1,N)

        new_points = [ self.point_in_space(u,v,w) 
                       for (u,v,w) in product(us, vs, ws) 
                       if u + v + w <= 1.0 
                     ]

        return new_points

    def shell(self, N=4, bottom=True):
        result = []
        result.extend(Tri(self.A,self.B,self.C).fill(N))
        result.extend(Tri(self.A,self.B,self.D).fill(N))
        result.extend(Tri(self.A,self.C,self.D).fill(N))
        if bottom:
            result.extend(Tri(self.B,self.C,self.D).fill(N))
        return result


    def __repr__(self):
        return "{},{},{},{}".format(self.A, self.B, self.C, self.D)



class Cube(Rotateable):
    def __init__(self, center, half_width):
        self.center = np.array(center)
        self.middle = Tetrahedron( (-half_width,-half_width,-half_width)
                                 , ( half_width, half_width,-half_width)
                                 , (-half_width, half_width, half_width)
                                 , ( half_width,-half_width, half_width)
                                 )

        self.A = Tetrahedron( -self.middle.A, self.middle.B, self.middle.C, self.middle.D )
        self.B = Tetrahedron( -self.middle.B, self.middle.A, self.middle.C, self.middle.D )
        self.C = Tetrahedron( -self.middle.C, self.middle.A, self.middle.B, self.middle.D )
        self.D = Tetrahedron( -self.middle.D, self.middle.A, self.middle.B, self.middle.C )

        self.middle.shift(center)
        self.A.shift(center)
        self.B.shift(center)
        self.C.shift(center)
        self.D.shift(center)

    def set_points(self, points):
        self.middle.set_points((points[0], points[1], points[2], points[3]))
        self.A.set_points((points[4], points[1], points[2], points[3]))
        self.B.set_points((points[5], points[0], points[2], points[3]))
        self.C.set_points((points[6], points[0], points[1], points[3]))
        self.D.set_points((points[7], points[0], points[1], points[2]))
        return self

    def points(self):
        result = self.middle.points()
        result.append(self.A.A)
        result.append(self.B.A)
        result.append(self.C.A)
        result.append(self.D.A)
        return result

    def fill(self, N=4):
        result = self.middle.fill(N)
        result.extend(self.A.fill(N))
        result.extend(self.B.fill(N))
        result.extend(self.C.fill(N))
        result.extend(self.D.fill(N))
        return result

    def shell(self, N=4):
        result = []
        result.extend(self.A.shell(N, bottom=False))
        result.extend(self.B.shell(N, bottom=False))
        result.extend(self.C.shell(N, bottom=False))
        result.extend(self.D.shell(N, bottom=False))
        return result

    def __repr__(self):
        return "{}".format(self.points())


if __name__=='__main__':
    A = np.array((0,0,0))
    B = np.array((2,0,0))
    C = np.array((2,2,0))

    p0 = np.array([2.0, 2.0, 0.0])
    p1 = np.array([0.2, 0.2, 0.0])
    p2 = np.array([0.7, 1.0, 0.0])

    T = Tri(A,B,C)

    print T.point_in_triangle(p0)
    print T.point_in_triangle(p1)
    print T.point_in_triangle(p2)

    t = Tri(A,B,C)
    from pprint import pprint
    pprint(t.fill())

    l = Line((10,0,0),(0,10,10))
    pprint(l.fill(20))



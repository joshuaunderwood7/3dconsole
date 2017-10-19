import abc
import numpy as np
from itertools import product, ifilter, izip

from quaternion import Quaternion, Q

def sameside3d(p, ref, A,B,C ):
    cpAB_BC = np.cross(A - B, A - C)

    sameABCr = np.dot(ref - A, cpAB_BC)
    sameABCp = np.dot(  p - A, cpAB_BC)

    sameABC = any(( sameABCr < 0 and sameABCp < 0 
                  , sameABCr > 0 and sameABCp > 0 
                  ))

    if sameABC:
        return True

    return False


class Rotateable():
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def points(self): 
        " Return constructible points in a list. "
        pass

    @abc.abstractmethod
    def set_points(self, points):
        " Construct shape from list of points. "
        pass

    def rotate3D_qua(self, r_angles, origin=np.array([0.0,0.0,0.0])):
        " Rotate the shape by [x,y,z] degrees about origin of [x,y,x], using quaternions"
        r_rads = r_angles * np.pi / np.float(180.0)

        axis_unit = ( np.cos(r_angles[0])
                    , np.sin(r_angles[0]) * np.cos(r_angles[1])
                    , np.sin(r_angles[0]) * np.sin(r_angles[1])
                    )

        rot_q = Q.from_axisangle(r_rads[2], axis_unit)

        new_points = [ (origin + (rot_q * (point - origin)))
                       for point in self.points() 
                     ]
        self.set_points(new_points)
        return self
            

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
        new_points = np.array([ (origin + (point - origin) * rot_matrix).A1 
                                for point in self.points() 
                              ])
        self.set_points(new_points)
        return self

class Obscuring():
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def contains_point(self, point):
        " Test if point is within the shape. "
        pass


class Line(Rotateable):
    def __init__(self, A, B):
        self.A = np.array(A)
        self.B = np.array(B)

        self.center = np.array(( np.mean(map(lambda x: x[0], [A,B]))
                               , np.mean(map(lambda x: x[1], [A,B]))
                               , np.mean(map(lambda x: x[2], [A,B]))
                               ))

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


class Tri(Rotateable, Obscuring):
    def __init__(self, A, B, C):
        self.A = np.array(A)
        self.B = np.array(B)
        self.C = np.array(C)

        self.AB = self.B - self.A
        self.AC = self.C - self.A

        self.center = np.array(( np.mean(map(lambda x: x[0], [A,B,C]))
                               , np.mean(map(lambda x: x[1], [A,B,C]))
                               , np.mean(map(lambda x: x[2], [A,B,C]))
                               ))

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

        denom = (dot00 * dot11 - dot01 * dot01)
        u = (dot11 * dot02 - dot01 * dot12) / denom
        v = (dot00 * dot12 - dot01 * dot02) / denom

        return (u >= 0) and (v >= 0) and (u + v <= 1)

    def contains_point(self, p): 
        return self.point_in_triangle(p)

    def fill(self, N=4):
        us = np.linspace(0,1,N)
        vs = np.linspace(0,1,N)

        new_points = [ self.point_in_plane(u,v) 
                       for (u,v) in product(us, vs) 
                       if u + v <= 1.0 
                     ]

        return new_points

    def __str__(self):
        return "{},{},{}".format(self.A, self.B, self.C)


class Tetrahedron(Rotateable, Obscuring):
    def __init__(self, A, B, C, D):
        self.A = np.array(A)
        self.B = np.array(B)
        self.C = np.array(C)
        self.D = np.array(D)

        self.center = np.array(( np.mean(map(lambda x: x[0], [A,B,C,D]))
                               , np.mean(map(lambda x: x[1], [A,B,C,D]))
                               , np.mean(map(lambda x: x[2], [A,B,C,D]))
                               ))

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


    def contains_point(self, p): 
        ss0 = sameside3d(p, self.A, self.B, self.C, self.D)
        ss1 = sameside3d(p, self.B, self.A, self.C, self.D)
        ss2 = sameside3d(p, self.C, self.B, self.B, self.D)
        ss3 = sameside3d(p, self.D, self.A, self.B, self.C)
        return all([ss0, ss1, ss2, ss3])

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


    def shell_vis(self, eye, N=4, bottom=True):
        result = []
        seeA =  sameside3d(eye, self.A, self.B, self.C, self.D)
        seeB =  sameside3d(eye, self.B, self.C, self.D, self.A)
        seeC =  sameside3d(eye, self.C, self.D, self.A, self.B)
        seeD =  sameside3d(eye, self.D, self.A, self.B, self.C)

        if not seeD : result.extend(Tri(self.A,self.B,self.C).fill(N))
        if not seeB : result.extend(Tri(self.A,self.C,self.D).fill(N))
        if not seeC : result.extend(Tri(self.A,self.B,self.D).fill(N))
        if not seeA and bottom : result.extend(Tri(self.B,self.C,self.D).fill(N))
        return result


    def shell(self, N=4, bottom=True):
        result = []
        result.extend(Tri(self.A,self.B,self.C).fill(N))
        result.extend(Tri(self.A,self.B,self.D).fill(N))
        result.extend(Tri(self.A,self.C,self.D).fill(N))
        if bottom:
            result.extend(Tri(self.B,self.C,self.D).fill(N))
        return result


    def __str__(self):
        return "{},{},{},{}".format(self.A, self.B, self.C, self.D)


class Sphere(Rotateable, Obscuring):
    def __init__(self, center, radius, N=12):
        self.center  = np.array(center)
        self.radius  = np.array(radius)
        self._points = self.points(N, initilize=True)

    def points(self, N=5, initilize=False): 
        " Return constructible points in a list. "
        if not initilize: return self._points

        lats = np.array(np.linspace(-np.pi/2, np.pi/2, N))
        lons = np.array(np.linspace(  -np.pi,   np.pi, N))

        result = np.ndarray(shape=(len(lats) * len(lons), 3), dtype=np.float32)

        for (ii, (lat, lon)) in enumerate(product(lats, lons)):
            result[ii] = np.array(( self.radius * np.cos(lat) * np.cos(lon)
                                  , self.radius * np.cos(lat) * np.sin(lon)
                                  , self.radius * np.sin(lat)
                                  )) + self.center
        return result

    def set_points(self, points):
        " Construct shape from list of points. "
        self._points = points
        return self

    def contains_point(self, point):
        " Test if point is within the shape. "
        return np.linalg.norm(point-center) < self.radius

    def fill(self, N=5):
        return self.points(N)

    def shell_vis(self, eye, N=5):
        np_eye = np.array(eye)
        dist = np.linalg.norm(self.center - np_eye)
        return [ point for point in self.points(N) if np.linalg.norm(point - np_eye) < dist ]

    def shell(self, N=5):
        return self.points(N)

    def clear_points(self):
        self._points = []
        return self

    def set_lat_lon_points(self, lat_lon_points):
        self._points = np.ndarray(shape=(len(lat_lon_points), 3), dtype=np.float32)
        for (ii, point) in enumerate(lat_lon_points):
            self._points[ii] = np.array(( self.radius * np.cos(point.lat * np.pi/180.0) * np.cos(point.lon * np.pi/180.0)
                                        , self.radius * np.cos(point.lat * np.pi/180.0) * np.sin(point.lon * np.pi/180.0)
                                        , self.radius * np.sin(point.lat * np.pi/180.0)
                                        )) + self.center
        return self

    def __str__(self):
        return "{} {} {}".format(self.center, self.radius, self.points())


class Cube(Rotateable, Obscuring):
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

    def contains_point(self, p): 
        return any(( self.middle.contains_point(p)
                   , self.A.contains_point(p)
                   , self.B.contains_point(p)
                   , self.C.contains_point(p)
                   , self.D.contains_point(p)
                   ))

    def fill(self, N=4):
        result = self.middle.fill(N)
        result.extend(self.A.fill(N))
        result.extend(self.B.fill(N))
        result.extend(self.C.fill(N))
        result.extend(self.D.fill(N))
        return result

    def shell_vis(self, eye, N=4):
        result = []
        result.extend(self.A.shell_vis(eye, N, bottom=False))
        result.extend(self.B.shell_vis(eye, N, bottom=False))
        result.extend(self.C.shell_vis(eye, N, bottom=False))
        result.extend(self.D.shell_vis(eye, N, bottom=False))
        return result

    def shell(self, N=4):
        result = []
        result.extend(self.A.shell(N, bottom=False))
        result.extend(self.B.shell(N, bottom=False))
        result.extend(self.C.shell(N, bottom=False))
        result.extend(self.D.shell(N, bottom=False))
        return result

    def __str__(self):
        return "{}".format(self.points())


if __name__=='__main__':

    S = Sphere((0,0,0), 5)

    print S

    # C = Cube(np.array([0,0,0]), 5)

    # p0 = np.array([0.0, 0.0, 0.0])
    # p1 = np.array([7.2, 0.0, 0.0])
    # p2 = np.array([  0, 7.2, 0.0])
    # p3 = np.array([  0,   0, 7.2])
    # p4 = np.array([0.7, 1.0, 0.0])


    # print C.contains_point(p0)
    # print C.contains_point(p1)
    # print C.contains_point(p2)
    # print C.contains_point(p3)
    # print C.contains_point(p4)

    # print C.shell_vis(np.array([0,0,-30]))




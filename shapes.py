import numpy as np
from itertools import product, ifilter

class Line():
    def __init__(self, A, B):
        self.A = np.array(A)
        self.B = np.array(B)

    def points(self):
        return [self.A, self.B]

    def fill(self, N=4):
        vec = self.B - self.A
        return [self.A + vec * ii for ii in np.linspace(0,1,N)]


class Tri():
    def __init__(self, A, B, C):
        self.A = np.array(A)
        self.B = np.array(B)
        self.C = np.array(C)


    def points(self):
        return [self.A, self.B, self.C]


    def point_in_triangle(self, p):
        v0 =      self.C - self.A
        v1 =      self.B - self.A
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
        points = self.points()
        xs = map(lambda x: x[0], points)
        ys = map(lambda x: x[1], points)
        zs = map(lambda x: x[2], points)

        new_points = product( np.linspace(min(xs), max(xs), N)
                            , np.linspace(min(ys), max(ys), N)
                            , np.linspace(min(zs), max(zs), N)
                            )
        new_points = map(np.array, set(new_points))
        result = ifilter(self.point_in_triangle, new_points)

        return list(result)

    def __repr__(self):
        return "{},{},{}".format(self.A, self.B, self.C)


class Cube():
    def __init__(self, center, half_width):
        xpoints = np.array([center[0]-half_width, center[0]+half_width])
        ypoints = np.array([center[0]-half_width, center[0]+half_width])
        zpoints = np.array([center[0]-half_width, center[0]+half_width])

        self.tris = []
        self.tris.append(Tri( np.array((xpoints[0], ypoints[0], zpoints[0])) , np.array((xpoints[0], ypoints[0], zpoints[1])) , np.array((xpoints[0], ypoints[1], zpoints[1]))))
        self.tris.append(Tri( np.array((xpoints[0], ypoints[0], zpoints[0])) , np.array((xpoints[0], ypoints[1], zpoints[0])) , np.array((xpoints[0], ypoints[1], zpoints[1]))))
        self.tris.append(Tri( np.array((xpoints[1], ypoints[0], zpoints[0])) , np.array((xpoints[1], ypoints[0], zpoints[1])) , np.array((xpoints[1], ypoints[1], zpoints[1]))))

        self.tris.append(Tri( np.array((xpoints[1], ypoints[0], zpoints[0])) , np.array((xpoints[1], ypoints[1], zpoints[0])) , np.array((xpoints[1], ypoints[1], zpoints[1]))))
        self.tris.append(Tri( np.array((xpoints[0], ypoints[0], zpoints[0])) , np.array((xpoints[0], ypoints[1], zpoints[0])) , np.array((xpoints[1], ypoints[1], zpoints[0]))))
        self.tris.append(Tri( np.array((xpoints[0], ypoints[0], zpoints[0])) , np.array((xpoints[1], ypoints[0], zpoints[0])) , np.array((xpoints[1], ypoints[1], zpoints[0]))))

        self.tris.append(Tri( np.array((xpoints[0], ypoints[0], zpoints[1])) , np.array((xpoints[0], ypoints[1], zpoints[1])) , np.array((xpoints[1], ypoints[1], zpoints[1]))))
        self.tris.append(Tri( np.array((xpoints[0], ypoints[0], zpoints[1])) , np.array((xpoints[1], ypoints[0], zpoints[1])) , np.array((xpoints[1], ypoints[1], zpoints[1]))))
        self.tris.append(Tri( np.array((xpoints[0], ypoints[0], zpoints[0])) , np.array((xpoints[0], ypoints[0], zpoints[1])) , np.array((xpoints[1], ypoints[0], zpoints[1]))))

        self.tris.append(Tri( np.array((xpoints[0], ypoints[0], zpoints[0])) , np.array((xpoints[1], ypoints[0], zpoints[0])) , np.array((xpoints[1], ypoints[0], zpoints[1]))))
        self.tris.append(Tri( np.array((xpoints[0], ypoints[1], zpoints[0])) , np.array((xpoints[0], ypoints[1], zpoints[1])) , np.array((xpoints[1], ypoints[1], zpoints[1]))))
        self.tris.append(Tri( np.array((xpoints[0], ypoints[1], zpoints[0])) , np.array((xpoints[1], ypoints[1], zpoints[0])) , np.array((xpoints[1], ypoints[1], zpoints[1]))))

    def points(self):
        result = []
        for t in self.tris:
            result.extend(t.points())
        return result

    def fill(self, N=4):
        result = []
        for t in self.tris:
            result.extend(t.fill(N))
        return result


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



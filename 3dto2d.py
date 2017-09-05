import itertools as I
import math
import sys
import time
import random

import numpy as np
import colorama

import console_map
import shapes
import teapot



N = 2
R = 9
V = 1
Size = 4
cubes = [ shapes.Cube((random.randint(-R,R),random.randint(-R,R),random.randint(-R,R)) , Size)  for _ in xrange(N) ]

# Size = 10
# a = Size / 2.0
# r = a * np.tan(np.pi/6.0)
# R = a * np.tan(np.pi/3.0) - r
# cubes = [shapes.Tetrahedron( (0,0,Size), (-r,-a,0), (-r,a,0), (R,0,0) )]


#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

def calc_lim(xy, dist=1.0, vis_angle=45.0):
    lim = np.tan(vis_angle * np.pi / 180.0) * dist
    return lim

def visible_test(point, dist=np.float(1), vis_angle=np.float(45.0)):
    x,y = point
    lim = calc_lim(x, dist, vis_angle)
    if -lim <= x <= lim and -lim <= y <= lim: return True
    return False

def LOS_test(eye, point, shapes):
    vector = point - eye
    for scale in [.9]:
        point = eye + vector * scale
        for shape in shapes:
            if shape.contains_point(point): 
                return False
    return True
        

def rotate2D(point, r_angle, origin=np.array([0.0,0.0])):
    r_rad = r_angle * np.pi / 180.0
    new_point = point - origin
    new_point = np.array([ new_point[0] * np.cos(r_rad) - new_point[1] * np.sin(r_rad)
                         , new_point[1] * np.cos(r_rad) + new_point[0] * np.sin(r_rad)
                         ])
    new_point += origin
    return new_point

def rotate3D(point, r_angles, origin=np.array([0.0,0.0,0.0])):
    r_rads = r_angles * np.pi / np.float(180.0)
    new_point = point - origin
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
    new_point = new_point * x_rot * y_rot * z_rot
    new_point += origin
    return new_point.A1

def perspective_division(eye, point, plane_dist=1.0):
    """
                      |
                      |
              E------>+--------->P
                  e   |    Z
                      |
    """
    new_point = point - eye
    Z = new_point[2]
    e = plane_dist
    return np.array([new_point[0] * e/Z, new_point[1] * e/Z])

def make_plot_points(eye, points3d, shapes, dist = 1.0, zip_depth=False):

    points = points3d
    # points = I.ifilter(lambda p: LOS_test(eye, p, shapes), points)
    points = I.imap(lambda p: perspective_division(eye, p, dist), points)
    points = I.ifilter(lambda p: visible_test(p, dist), points)
    points = I.imap(lambda p: console_map.latlon(p[1], p[0]), points)

    if zip_depth:
        points = I.izip(I.imap(lambda z: z[2], points3d), points)

    return points

#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

HEIGHT, WIDTH = console_map.get_screen_size()
HEIGHT -= 1
dist = 1.0
eye = (0.0, 0.0, -20.0)

matrix_maker   = console_map.get_screen_matrix_maker(-1.0,1.0, -1.0, 1.0, HEIGHT, WIDTH)

rotations = [ np.array((random.randint(-V,V),random.randint(-V,V),random.randint(-V,V))) for _ in xrange(len(cubes)) ]
# rotations = [np.array([1.1, 1.3, 0]) for _ in xrange(len(cubes))]
zipped_rotations_and_cubes = zip(rotations, cubes)

layer_symbols = " #&%$|!;:+*-,."
layer_symbols = " @#+=-:,."
lls = len(layer_symbols)
ldm = 2

def layer(p): 
    return int(len(layer_symbols) * (p[1] - eye[2]) / (20 - eye[2]))

#3Drotate the shapes
while True:

    #rotate shapes
    vert_points = []
    shll_points = []
    for rotation, cube in zipped_rotations_and_cubes:
        cube.rotate3D(rotation, cube.center)
        # vert_points.extend(make_plot_points(eye, cube.points(), cubes, dist))
        shll_points.extend(make_plot_points (eye, cube.shell_vis(eye, N=14)
                                            , cubes, dist, zip_depth=True))

    layers = [matrix_maker(vert_points, 1)]

    shll_points = I.imap(lambda x: (ldm + int((lls-ldm) * (x[0] + 20.0) / 40.0), x[1]), shll_points)
    shll_points_dict = dict((x,[]) for x in xrange(ldm,lls+ldm))
    for k,v in shll_points:
        shll_points_dict[k].append(v)

    for k,v in shll_points_dict.items():
        layers.append(matrix_maker(v,k))

    layers.reverse()
    smat = console_map.join_smat_layers_gen(layers)

    print colorama.Cursor.POS() + console_map.print_screen_matrix_layers(smat, symbols=layer_symbols),
    # time.sleep(0.1)



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



N = 20
R = 20
squares = [ shapes.Cube((random.randint(-R,R),random.randint(-R,R),random.randint(-R,R)) , 2.0)  for _ in xrange(N) ]


#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

def calc_lim(xy, dist=1.0, vis_angle=45.0):
    lim = np.tan(vis_angle * np.pi / 180.0) * dist
    return lim

def visible_test(point, dist=np.float(1), vis_angle=np.float(45.0)):
    x,y = point
    lim = calc_lim(x, dist, vis_angle)
    if -lim <= x <= lim and -lim <= y <= lim: return True
    return False

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
    return new_point

def perspective_division(eye, point, plane_dist=1.0):
    """
                      |
                      |
              E------>+--------->P
                  e   |    Z
                      |
    """
    new_point = point - eye
    Z = new_point[0,2]
    e = plane_dist
    return np.array([new_point[0,0] * e/Z, new_point[0,1] * e/Z])

def make_plot_points(points3d, dist = 1.0):
    visible_points = I.ifilter(lambda p: visible_test(p, dist), points3d)
    plot_points    = I.imap(lambda p: console_map.latlon(p[1], p[0]), visible_points)
    return plot_points

#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

HEIGHT, WIDTH = console_map.get_screen_size()
HEIGHT -= 1
dist = 1.0
eye = (0.0, 0.0, -20.0)

matrix_maker   = console_map.get_screen_matrix_maker(-1.0,1.0, -1.0, 1.0, HEIGHT, WIDTH)

rotations = [ np.array((random.randint(-10,10),random.randint(-10,10),random.randint(-10,10))) for _ in xrange(len(squares)) ]
zipped_rotations_and_cubes = zip(rotations, squares)


#3Drotate the shapes
while True:

    #rotate shapes
    vert_points = []
    shll_points = []
    for rotation, cube in zipped_rotations_and_cubes:
        cube.rotate3D(rotation, cube.center)
        vert_points.extend([perspective_division(eye, point, dist) for point in cube.points()])
        shll_points.extend([perspective_division(eye, point, dist) for point in cube.shell()])

    vert_points = make_plot_points(vert_points, dist)
    shll_points = make_plot_points(shll_points, dist)    

    cntr = I.count(1)

    layers = I.imap(lambda l: matrix_maker(l, next(cntr)), [shll_points, vert_points])
    smat = console_map.join_smat_layers_gen(layers)

    print colorama.Cursor.POS() + console_map.print_screen_matrix_layers(smat, symbols=' -#.'),
    # time.sleep(0.1)



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


# points.extend(square_00.points())
# pFill.extend(square_00.fill())

squares = [ shapes.Cube((x,y,z), 2.0) 
            for x,y,z in I.product([-10,0,10],[-10,0,10],[0]) ]

# tetrahedron_00 = shapes.Tetrahedron((-5,-5,-5),(5,5,-5),(-5,5,5),(5,-5,5))
# points.extend(tetrahedron_00.points())
# pFill.extend(tetrahedron_00.fill(9))

# tetrahedron_01 = shapes.Tetrahedron(( 5, 5, 5),(-5,-5,5),(-5,5,-5),(5,-5,-5))
# points.extend(tetrahedron_01.points())
# pFill.extend(tetrahedron_01.shell(9))


# line_00 = shapes.Line((-5,-5,-5), (5,5,5))
# points.extend(line_00.fill(20))


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

#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

HEIGHT, WIDTH = console_map.get_screen_size()
HEIGHT -= 1
dist = 1.0
eye = (0.0, 0.0, -20.0)

#3Drotate the shapes
matrix_maker   = console_map.get_screen_matrix_maker(-1.0,1.0, -1.0, 1.0, HEIGHT, WIDTH)
for rotation in np.linspace(-8 * np.pi, 8 * np.pi, 500):

    #rotate shapes
    new_points = []
    for cube in squares:
        cube.rotate3D(np.array([10,5,0]), cube.center)
        new_points.extend([perspective_division(eye, point, dist) for point in cube.shell()])

    visible_points = I.ifilter(lambda p: visible_test(p, dist), new_points)
    plot_points    = I.imap(lambda p: console_map.latlon(p[1], p[0]), visible_points)
    
    cntr = I.count(1)

    layers = I.imap(lambda l: matrix_maker(l, next(cntr)), [plot_points])
    smat = console_map.join_smat_layers_gen(layers)

    print colorama.Cursor.POS() + console_map.print_screen_matrix_layers(smat, symbols=' -#.'),
    # time.sleep(0.1)



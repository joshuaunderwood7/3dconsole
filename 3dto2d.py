import itertools as I
import math
import numpy as np
import sys
import time
import colorama

import console_map
import pannom
import shapes
import teapot


origin = np.array([0,0,0])
xpoints = np.array([origin[0]-5.0, origin[0]+5.0])
ypoints = np.array([origin[0]-5.0, origin[0]+5.0])
zpoints = np.array([origin[0]-5.0, origin[0]+5.0])
z_curve_x = pannom.UtilityCurve( xpoints[0]
                               , xpoints[0] + (xpoints[1] - xpoints[0]) * 0.45
                               , xpoints[0] + (xpoints[1] - xpoints[0]) * 0.60
                               , xpoints[0] + (xpoints[1] - xpoints[0]) * 0.95
                               , xpoints[1]
                               , weight = 0.5
                               , bounty = zpoints[1] - zpoints[0]
                               )

z_curve_y = pannom.UtilityCurve( ypoints[0]
                               , ypoints[0] + (ypoints[1] - ypoints[0]) * 0.25
                               , ypoints[0] + (ypoints[1] - ypoints[0]) * 0.60
                               , ypoints[0] + (ypoints[1] - ypoints[0]) * 0.90
                               , ypoints[1]
                               , weight = 0.5
                               , bounty = zpoints[1] - zpoints[0]
                               )

points = []
pFill = []

square_00 = shapes.Cube(origin, 5.0)
points.extend(square_00.points())
pFill.extend(square_00.fill(10))


line_00 = shapes.Line((-5,-5,-5), (5,5,5))
points.extend(line_00.fill(20))


uCurve = []
for x,y in pannom.getMSR_ND([z_curve_x, z_curve_y], N=50):
    uCurve.append((np.float(x),np.float(y), zpoints[0] + z_curve_x(x) + z_curve_y(y)))

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
    new_point = new_point * x_rot 
    new_point = new_point * y_rot
    new_point = new_point * z_rot
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
eye = (0.0, 0.0, -23.0)

#3Drotate the points
for rotation in np.linspace(-8 * np.pi, 8 * np.pi, 500):

    rotated_points = map( lambda p : rotate3D(p, np.array([25, np.sin(rotation) * 45, 0]), origin + np.array([0,0,0])), points)
    new_points     = [ perspective_division(eye, point, dist) for point in rotated_points ]
    visible_points = filter(lambda p: visible_test(p, dist), new_points)
    plot_points    = map(lambda p: console_map.latlon(p[1], p[0]), visible_points)

    rotated_pFill  = map( lambda p : rotate3D(p, np.array([25, np.sin(rotation) * 45, 0]), origin + np.array([0,0,0])), pFill)
    new_pFill      = [ perspective_division(eye, point, dist) for point in rotated_pFill ]
    visible_pFill  = filter(lambda p: visible_test(p, dist), new_pFill)
    plot_pFill     = map(lambda p: console_map.latlon(p[1], p[0]), visible_pFill)

    rotated_uCurve = map( lambda p : rotate3D(p, np.array([25, np.sin(rotation) * 45, 0]), origin + np.array([0,0,0])), uCurve)
    new_uCurve     = [ perspective_division(eye, point, dist) for point in rotated_uCurve ]
    visible_uCurve = filter(lambda p: visible_test(p, dist), new_uCurve)
    plot_uCurve    = map(lambda p: console_map.latlon(p[1], p[0]), visible_uCurve)


    matrix_maker   = console_map.get_screen_matrix_maker(-1.0,1.0, -1.0, 1.0, HEIGHT, WIDTH)
    cntr = I.count(1)
    layers = map(lambda l: matrix_maker(l, next(cntr)), [plot_pFill, plot_points, plot_uCurve])

    smat = console_map.join_smat_layers_gen(layers)

    print colorama.Cursor.POS() + console_map.print_screen_matrix_layers(smat, symbols=' -#.'),
    # time.sleep(0.1)



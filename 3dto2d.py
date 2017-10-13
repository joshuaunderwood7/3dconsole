import functools
import itertools as I
import math
import random
import sys
import time

import numpy as np
import colorama

import console_map
import shapes
import teapot

GREY_SCALE_FULL = "$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,\"^`'. "
GREY_SCALE_10   = "@%#*+=-:. "

N = 9
R = 20
V = 3
Size = 5
# cubes = [ shapes.Cube((random.randint(-R,R),random.randint(-R,R),random.randint(-R,R)) , Size)  for _ in xrange(N) ]
all_cubes = [ shapes.Cube(( -15 , -15 , random.randint(0,R)) , Size)
        , shapes.Cube((   0 , -15 , random.randint(0,R)) , Size)
        , shapes.Cube((  15 , -15 , random.randint(0,R)) , Size)
        , shapes.Cube(( -15 ,   0 , random.randint(0,R)) , Size)
        , shapes.Cube((   0 ,   0 , random.randint(0,R)) , Size)
        , shapes.Cube((  15 ,   0 , random.randint(0,R)) , Size)
        , shapes.Cube(( -15 ,  15 , random.randint(0,R)) , Size)
        , shapes.Cube((   0 ,  15 , random.randint(0,R)) , Size)
        , shapes.Cube((  15 ,  15 , random.randint(0,R)) , Size)
        ]

# Size = 10
# a = Size / 2.0
# r = a * np.tan(np.pi/6.0)
# R = a * np.tan(np.pi/3.0) - r
# cubes = [shapes.Tetrahedron( (0,0,Size), (-r,-a,0), (-r,a,0), (R,0,0) )]


#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

def visible_test(point, dist=np.float(1), vis_angle=np.float(45.0)):
    _lim = np.tan(45.0 * np.pi / 180.0) * dist
    if -_lim <= point[0] <= _lim and -_lim <= point[1] <= _lim: return True
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

# def rotate3D(point, r_angles, origin=np.array([0.0,0.0,0.0])):
#Moved to shapes.py

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
    return (new_point * e/Z)[:2]

def perspective_division_group(eye, points, plane_dist=1.0):
    new_points = points - eye
    Z = new_points[:, 2]
    e = plane_dist
    return (new_points.T * (e/Z)).T[:, [0,1]]


def make_plot_points(eye, points3d, shapes, dist = np.float(1), zip_depth=True):


    points = perspective_division_group(eye, np.array(points3d))

    # points = I.ifilter(lambda p: LOS_test(eye, p, shapes), points) # Too slow

    _lim = np.float(np.tan(45.0 * np.pi / 180.0) * dist)
    points = (console_map.latlon(x,y) for (x,y) in points)
    # points = (console_map.latlon(x,y) for (x,y) in points 
            # if -_lim <= x <= _lim and -_lim <= y <= _lim)

    if zip_depth:
        points = I.izip(I.imap(lambda z: z[2], points3d), points)

    return points

def make_visible_surface(HEIGHT, WIDTH, eye, dist, shapes, grey_scale=GREY_SCALE_10, MAX_DEPTH=20):
    filter_lat = functools.partial(console_map._filter_mm, -1.0, 1.0)
    filter_lon = functools.partial(console_map._filter_mm, -1.0, 1.0)
    normalize  = console_map.__normalize(-1.0, 1.0, -1.0, 1.0)

    len_grey_scale = len(grey_scale)
    gsn_dnm = (MAX_DEPTH - eye[2]) or 1
    bucket = dict()


    for shape in shapes:
        this_data = make_plot_points( eye, shape.shell_vis(eye, N=int(10))
                                    , shapes, dist, zip_depth=True )
        # [(depth, data)]
        for depth, data in this_data:
            if not (filter_lat(data.lat) and filter_lon(data.lon)) : continue
            data = normalize(data)

            index = (int((HEIGHT-1) * data.lat), int((WIDTH-1) * data.lon))
            if bucket.get(index, MAX_DEPTH) > depth:
                bucket.update({index:depth})

    screen = [[bucket.get((i,j), MAX_DEPTH) for j in xrange(WIDTH)] for i in xrange(HEIGHT)]

    for j in xrange(WIDTH):
        for i in xrange(HEIGHT):
            normed = (screen[i][j] - eye[2]) / (gsn_dnm)
            index = int(normed * len_grey_scale) - 1 

            if   index <  0             : index = 0
            elif index >= len_grey_scale: index = len_grey_scale - 1
            screen[i][j] = grey_scale[ index ]

    return '\n'.join(map(lambda s: ''.join(s), reversed(screen)))


#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

HEIGHT, WIDTH = console_map.get_screen_size()
HEIGHT -= 1
dist = 1.0
eye = (0.0, 0.0, -20.0)

#3Drotate the shapes
def run():
    #rotate shapes
    for rotation, cube in zipped_rotations_and_cubes:
        cube.rotate3D(rotation, cube.center)
        # cube.rotate3D_qua(rotation, cube.center)

    vis_surface = make_visible_surface(HEIGHT, WIDTH, eye, dist, cubes)

    print colorama.Cursor.POS() + vis_surface
    #time.sleep(0.1)

Number_of_Cubes = 3
# for _ in range(5):
while True:
    cubes = random.sample([ shapes.Cube(( -15 , -15 , random.randint(0,R)) , Size)
        , shapes.Cube((   0 , -15 , random.randint(0,R)) , Size)
        , shapes.Cube((  15 , -15 , random.randint(0,R)) , Size)
        , shapes.Cube(( -15 ,   0 , random.randint(0,R)) , Size)
        , shapes.Cube((   0 ,   0 , random.randint(0,R)) , Size)
        , shapes.Cube((  15 ,   0 , random.randint(0,R)) , Size)
        , shapes.Cube(( -15 ,  15 , random.randint(0,R)) , Size)
        , shapes.Cube((   0 ,  15 , random.randint(0,R)) , Size)
        , shapes.Cube((  15 ,  15 , random.randint(0,R)) , Size)
        ], Number_of_Cubes)
    rotations = [ np.array((random.randint(-V,V),random.randint(-V,V),random.randint(-V,V))) for _ in xrange(len(cubes)) ]
    # rotations = [np.array([1.1, 1.3, 0]) for _ in xrange(len(cubes))]
    zipped_rotations_and_cubes = zip(rotations, cubes)
    for _ in xrange(random.randint(30,80)):
        run()





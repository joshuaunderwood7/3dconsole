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

import multiprocessing


GREY_SCALE_FULL = "$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,\"^`'. "
GREY_SCALE_10   = "@%#*+=-:. "

N = 9
R = 20
V = 3
Size = 5
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
    if len(points) < 1: return points
    new_points = points - eye
    Z = new_points[:, 2]
    e = plane_dist
    return (new_points.T * (e/Z)).T[:, [0,1]]


def make_plot_points(eye, points3d, shapes, dist = np.float(1), zip_depth=True):
    points = perspective_division_group(eye, np.array(points3d))

    # points = I.ifilter(lambda p: LOS_test(eye, p, shapes), points) # Too slow

    # _lim = np.float(np.tan(45.0 * np.pi / 180.0) * dist)
    _lim = 1.0
    points = (console_map.latlon(x,y) for (x,y) in points)
    # points = (console_map.latlon(x,y) for (x,y) in points 
            # if -_lim <= x <= _lim and -_lim <= y <= _lim)

    if zip_depth:
        points = I.izip(I.imap(lambda z: z[2], points3d), points)

    return points

BLIT_SCREEN = ''
def blit(new_surface, presplit=False):
    global BLIT_SCREEN

    if presplit: NEW_SCREEN = new_surface
    else:        NEW_SCREEN = new_surface.split('\n')

    if BLIT_SCREEN == '':
        if presplit:
            new_surface = '\n'.join(map(lambda s: ''.join(s), reversed(SCREEN)))
        print colorama.Cursor.POS() + new_surface

    else: 
        y = 1
        for o_line, n_line in I.izip(BLIT_SCREEN, NEW_SCREEN):
            x = 1
            for old,new in I.izip(o_line, n_line):
                if old != new:
                    print colorama.Cursor.POS(x,y) + new
                x += 1
            y += 1
    BLIT_SCREEN = NEW_SCREEN

blit_draw = blit

init_SCREEN = True
SCREEN = None
def make_visible_surface(HEIGHT, WIDTH, eye, dist, shapes, grey_scale=GREY_SCALE_10, MAX_DEPTH=20, blit=False):
    global SCREEN, init_SCREEN
    if init_SCREEN: 
        SCREEN = np.zeros(shape=(HEIGHT, WIDTH), dtype='|S1')
        init_SCREEN = False

    len_grey_scale = len(grey_scale)
    gsn_dnm = (MAX_DEPTH - eye[2]) or 1

    filter_lat = functools.partial(console_map._filter_mm, -1.0, 1.0)
    filter_lon = functools.partial(console_map._filter_mm, -1.0, 1.0)
    normalize  = console_map.__normalize(-1.0, 1.0, -1.0, 1.0)

    bucket = dict()
    for shape in shapes:
        shape_data = make_plot_points( eye, shape.shell_vis(eye, N=int(10))
                                     , shapes, dist, zip_depth=True 
                                     )
        for depth, data in shape_data:
            if not (filter_lat(data.lat) and filter_lon(data.lon)) : continue
            data = normalize(data)

            index = (int((HEIGHT-1) * data.lat), int((WIDTH-1) * data.lon))
            if bucket.get(index, MAX_DEPTH) > depth:
                bucket.update({index:depth})

    for j in xrange(WIDTH):
        for i in xrange(HEIGHT):
            data   = bucket.get((i,j), MAX_DEPTH)
            normed = (data - eye[2]) / (gsn_dnm)
            index  = int(normed * len_grey_scale) - 1 

            if   index <  0             : index = 0
            elif index >= len_grey_scale: index = len_grey_scale - 1
            SCREEN[i][j] = grey_scale[ index ]

    if blit: blit_draw(map(lambda s: ''.join(s), reversed(SCREEN)), presplit=True)
    else:    return '\n'.join(map(lambda s: ''.join(s), reversed(SCREEN)))


#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

HEIGHT, WIDTH = console_map.get_screen_size()
HEIGHT -= 1
# WIDTH = HEIGHT * 2
dist = 1.0
eye = (0.0, 0.0, -20.0)
__POOL__=multiprocessing.Pool(multiprocessing.cpu_count())


# ROTATION = (1,1,0)
# sphere = shapes.Sphere((0,0,0), 12, 12)

# data      = [  console_map.latlon( 30, R) for R in np.linspace(-180, 180)]
# data.extend([  console_map.latlon(-30, R) for R in np.linspace(-180, 180)])
# data.extend([console_map.latlon(R, 0) for R in np.linspace(-90, 90)])
# sphere.set_lat_lon_points(data)

# # sys.path.append('/home/underwood/code/gshhg/')
# # import GSHHG
# # polygons = []
# # with open('/home/underwood/code/gshhg/gshhg-bin-2.3.7/gshhs_c.b') as infile:
    # # while infile.read(1):
        # # infile.seek(-1,1)
        # # polygons.append(GSHHG.receive_polygon(infile))
# # data = []
# # for ii, polygon in enumerate(polygons):
    # # data.extend([console_map.latlon(p.y, p.x) for p in  polygon[1]])
    # # if ii > 0: break
# # sphere.set_lat_lon_points(data)


# sphere.rotate3D(np.array((0,-90,0)), sphere.center)
# while True:
    # shape_list  = [sphere]
    # vis_surface = make_visible_surface(HEIGHT, WIDTH, eye, dist, shape_list)
    # print colorama.Cursor.POS() + vis_surface
    # sphere.rotate3D(np.array(ROTATION), sphere.center)


# sys.exit()

#3Drotate the shapes
def run(shapes):
    new_shapes = [shape.rotate3D_qua() for shape in shapes]
    # new_shapes = (shape.rotate3D() for shape in shapes)
    make_visible_surface(HEIGHT, WIDTH, eye, dist, new_shapes, blit=True)
    # print colorama.Cursor.POS() + vis_surface


Number_of_Shapes = 5
max_loops = 20
while max_loops > 0 or max_loops == -42:
    max_loops -= 1 if max_loops != -42 else 0
    shape_list = random.sample(
        [ shapes.Cube(( -15 , -15 , random.randint(0,R)) , Size)
        , shapes.Cube((   0 , -15 , random.randint(0,R)) , Size)
        , shapes.Cube((  15 , -15 , random.randint(0,R)) , Size)
        , shapes.Cube(( -15 ,   0 , random.randint(0,R)) , Size)
        , shapes.Cube((   0 ,   0 , random.randint(0,R)) , Size)
        , shapes.Cube((  15 ,   0 , random.randint(0,R)) , Size)
        , shapes.Cube(( -15 ,  15 , random.randint(0,R)) , Size)
        , shapes.Cube((   0 ,  15 , random.randint(0,R)) , Size)
        , shapes.Cube((  15 ,  15 , random.randint(0,R)) , Size)
        , shapes.Sphere(( -15 , -15 , random.randint(0,R)) , Size)
        , shapes.Sphere((   0 , -15 , random.randint(0,R)) , Size)
        , shapes.Sphere((  15 , -15 , random.randint(0,R)) , Size)
        , shapes.Sphere(( -15 ,   0 , random.randint(0,R)) , Size)
        , shapes.Sphere((   0 ,   0 , random.randint(0,R)) , Size)
        , shapes.Sphere((  15 ,   0 , random.randint(0,R)) , Size)
        , shapes.Sphere(( -15 ,  15 , random.randint(0,R)) , Size)
        , shapes.Sphere((   0 ,  15 , random.randint(0,R)) , Size)
        , shapes.Sphere((  15 ,  15 , random.randint(0,R)) , Size)
        ], Number_of_Shapes)
    for shape in shape_list:
        shape.setOrigin(shape.center)
        shape.setRotationVector((random.random(),random.random(),random.random()))
        shape.setRotationAngle(random.randint(1,6))
        shape.setRotationEucAngles((0,0,10))

    for _ in xrange(50):
        run(shape_list)



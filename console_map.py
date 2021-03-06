import functools
import os
import itertools as I
from exceptions import IndexError

class latlon():
    def __init__(self, lat, lon):
        self.lat = float(lat)
        self.lon = float(lon)
        self.y = self.lat
        self.x = self.lon

    def __repr__(self):
        return '({}, {})'.format(self.lat, self.lon)

    def __getitem__(self,n):
        if n == 0: return self.lat
        if n == 1: return self.lon
        raise IndexError

def _filter_mm(min, max, x): return min <= x <= max

def _normalize(lat_min, lat_max, lon_min, lon_max, d):
    n_lat = float(d.lat - lat_min) / float(lat_max - lat_min)
    n_lon = float(d.lon - lon_min) / float(lon_max - lon_min)
    return latlon(n_lat, n_lon)

def __normalize(lat_min, lat_max, lon_min, lon_max):
    denom_lat = float(lat_max - lat_min)
    denom_lon = float(lon_max - lon_min)
    def normalize(d):
        return latlon( (d.lat - lat_min) / denom_lat
                     , (d.lon - lon_min) / denom_lon
                     )
    return normalize

def get_screen_size():
    HEIGHT, WIDTH = map(int, os.popen('stty size', 'r').read().split())
    return HEIGHT, WIDTH

def print_screen(lat_min, lat_max, lon_min, lon_max, height, width, data,
        symbol='.', filler=' '):
    filter_lat = functools.partial(_filter_mm, lat_min, lat_max)
    filter_lon = functools.partial(_filter_mm, lon_min, lon_max)
    normalize  = __normalize(lat_min, lat_max, lon_min, lon_max)

    this_data = filter(lambda d: filter_lat(d.lat) and filter_lon(d.lon), data)
    this_data = map(normalize, this_data)

    screen = [[filler for _ in xrange(width)] for _ in xrange(height)]
    for d in this_data:
        screen[int((height-1) * d.lat)][int((width-1) * d.lon)] = symbol

    return '\n'.join(map(lambda s: ''.join(s), reversed(screen)))

def get_screen_matrix_maker(lat_min, lat_max, lon_min, lon_max, height, width):
    filter_lat = functools.partial(_filter_mm, lat_min, lat_max)
    filter_lon = functools.partial(_filter_mm, lon_min, lon_max)
    normalize  = __normalize(lat_min, lat_max, lon_min, lon_max)

    def __get_screen_maxrix(data, layer):
        this_data = I.ifilter(lambda d: filter_lat(d.lat) and filter_lon(d.lon), data)
        this_data = I.imap(normalize, this_data)

        screen = [[0 for _ in xrange(width)] for _ in xrange(height)]
        for d in this_data:
            screen[int((height-1) * d.lat)][int((width-1) * d.lon)] = layer
        return screen
    return __get_screen_maxrix

def get_screen_matrix_coord(lat_min, lat_max, lon_min, lon_max, height, width, data, layer=1):
    filter_lat = functools.partial(_filter_mm, lat_min, lat_max)
    filter_lon = functools.partial(_filter_mm, lon_min, lon_max)
    normalize  = __normalize(lat_min, lat_max, lon_min, lon_max)

    this_data = I.ifilter(lambda d: filter_lat(d.lat) and filter_lon(d.lon), data)
    this_data = I.imap(normalize, this_data)
    coords = [ ( int((height-1) * d.lat), int((width-1) * d.lon) )
               for d in this_data
             ]
    return coords

def get_screen_matrix(lat_min, lat_max, lon_min, lon_max, height, width, data, layer=1):
    filter_lat = functools.partial(_filter_mm, lat_min, lat_max)
    filter_lon = functools.partial(_filter_mm, lon_min, lon_max)
    normalize  = __normalize(lat_min, lat_max, lon_min, lon_max)

    this_data = I.ifilter(lambda d: filter_lat(d.lat) and filter_lon(d.lon), data)
    this_data = I.imap(normalize, this_data)

    screen = [[0 for _ in xrange(width)] for _ in xrange(height)]
    for d in this_data:
        screen[int((height-1) * d.lat)][int((width-1) * d.lon)] = layer
    return screen

def join_screen_matrix(core_smat, snd_smat):
    return [ [max(b,a) for (a,b) in I.izip(line_a, line_b)] 
             for (line_a, line_b) in I.izip(core_smat, snd_smat) ]

def join_screen_matrix_with_coords(orig_smat, new_smat):
    coords = []
    for i, (line_a, line_b) in enumerate(I.izip(orig_smat, new_smat)):
        for j, (a,b) in enumerate(I.izip(line_a, line_b)):
            if b > a:
                orig_smat[i][j] = b
                coords.append((i,j))

    return orig_smat, coords


def matrix_move_layer_gen(smat, by):
    return ( (a + by if a > 0 else 0 for a in line) for line in smat )

def join_screen_matrix_gen(core_smat, snd_smat):
    return ( (max(b,a) for (a,b) in I.izip(line_a, line_b)) 
             for (line_a, line_b) in I.izip(core_smat, snd_smat) )
def join_smat_layers_gen(layers):
    return reduce( join_screen_matrix_gen, layers)


def print_screen_matrix(screen_matrix, symbol='.', filler=' '):
    return '\n'.join(( ''.join( (symbol if B else filler for B in line) )
                        for line in reversed(list(screen_matrix))
                     ))

def print_screen_matrix_layers(screen_matrix, symbols=' .'):
    return '\n'.join(( ''.join( symbols[B] for B in line )
                        for line in reversed(list(screen_matrix))
                     ))

def interpolate(p0, p1, N=10):
    # y - y0   y1 - y0
    # ------ = -------
    # x - x0   x1 - x0
    if (p1.x - p0.x) != 0:
        y = lambda x: p0.y + (x - p0.x) * (p1.y - p0.y) / (p1.x - p0.x)
        delta = (p1.x - p0.x) / N
        xs = [p0.x + ii * delta for ii in xrange(N)] 
        return [latlon(y(x),x) for x in xs]
    else: # vertical line
        delta = (p1.y - p0.y) / N
        ys = [p0.y + ii * delta for ii in xrange(N)] 
        return [latlon(y,p0.x) for y in ys]
    
 
class Polygon():
    def __init__(self, points, connect_ends=True):
        self.points       = points
        self.connect_ends = connect_ends

    def raster(self, N=10):
        self.points = list(self.points)
        new_points = []
        #Connect the dots
        for p0, p1 in zip(self.points[:-1], self.points[1:]):
            new_points.extend(interpolate(p0, p1, N))

        #Connect end to beginning
        if self.connect_ends:
            new_points.extend(interpolate(self.points[-1], self.points[0], N))

        self.points = new_points
        return self

    def thin_points(self, two_to_the_N=1):
        self.points = self.points[::2**N]
           
    def __repr__(self):
        return repr(self.points)

class Line(Polygon):
    def __init__(self, points, connect_ends=False):
        self.points       = points
        self.connect_ends = connect_ends


if __name__=='__main__':
    lat_min, lat_max = 0,10
    lon_min, lon_max = 0,10
    height = 48
    width  = 160


    poly = Polygon([latlon(0,0), latlon(0,3), latlon(3,7), latlon(10,10), latlon(9,5)]) 
    line = Line([latlon(0,0), latlon(3,7), latlon(9,5)]) 

    line.raster(N=100)
    data = line.points
    print print_screen(lat_min, lat_max, lon_min, lon_max, height, width, 
            data, symbol='-', filler=' ')

    poly.raster(N=100)
    data = poly.points
    print print_screen(lat_min, lat_max, lon_min, lon_max, height, width, 
            data, symbol='-', filler=' ')



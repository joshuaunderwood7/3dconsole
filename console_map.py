import functools
import os
import itertools as I

class latlon():
    def __init__(self, lat, lon):
        self.lat = float(lat)
        self.lon = float(lon)
        self.y = self.lat
        self.x = self.lon

    def __repr__(self):
        return '({}, {})'.format(self.lat, self.lon)

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
    return [ [b or a for (a,b) in I.izip(line_a, line_b)] 
             for (line_a, line_b) in I.izip(core_smat, snd_smat) ]

def join_screen_matrix_gen(core_smat, snd_smat):
    return ( (b or a for (a,b) in I.izip(line_a, line_b)) 
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
    def __init__(self, points):
        self.points = points

    def raster(self, N=10):
        self.points = list(self.points)
        new_points = []
        for p0, p1 in zip(self.points[:-1], self.points[1:]):
            new_points.extend(interpolate(p0, p1, N))
        new_points.extend(interpolate(self.points[-1], self.points[0], N))
        self.points = new_points
        return self

    def thin_points(self, two_to_the_N=1):
        self.points = self.points[::2**N]
           
    def __repr__(self):
        return repr(self.points)


if __name__=='__main__':
    lat_min, lat_max = 0,10
    lon_min, lon_max = 0,10
    height = 48
    width  = 160

    poly = Polygon([latlon(0,0), latlon(0,3), latlon(3,7), latlon(10,10), latlon(9,5)]) 

    poly.raster(N=100)

    data = poly.points
    print print_screen(lat_min, lat_max, lon_min, lon_max, height, width, 
            data, symbol='-', filler=' ')


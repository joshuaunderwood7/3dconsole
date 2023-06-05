#include <climits>
#include <deque>
#include <fstream>
#include <iostream>
#include <memory>
#include <string>

#include <sys/ioctl.h>
#include <unistd.h>

#include <shapes.h>
#include <screen.h>
#include <gshhs.h>
#include <TLE.h>

using namespace std;

class Polygon
{
public:
    Polygon() {};
    Polygon(ifstream & data_file) 
    {
        data_file.read((char*)&metadata, sizeof(GSHHG));
        gshhs_convert( metadata );

        GSHHG_POINT point;
        for(int ii=0; ii<metadata.n; ++ii)
        {
            data_file.read((char*)&point, sizeof(GSHHG_POINT));
            gshhs_convert( point );

            point.x = ( (180000000+point.x) % 360000000 ) - 180000000;
            point.y = ( ( 90000000+point.y) % 180000000 ) -  90000000;

            points.push_back(point);

            max_lat = (point.y >= max_lat) ? point.y : max_lat;
            min_lat = (point.y <= min_lat) ? point.y : min_lat;
            max_lon = (point.x >= max_lon) ? point.x : max_lon;
            min_lon = (point.x <= min_lon) ? point.x : min_lon;
        }
    };

    GSHHG              metadata;
    deque<GSHHG_POINT> points;

    void print_metadata()
    {
        cout << "id='"        << metadata.id    << "' /* Unique polygon id number, starting at 0 */ " << endl
             << "n='"         << metadata.n     << "' /* Number of points in this polygon */ " << endl
             << "flag='"      << metadata.flag  << "' --- flag contains 5 items, as follows:" << endl
             << "    - level     = '" << ( metadata.flag        & 255) << "' Values: 1 land, 2 lake, 3 island_in_lake, 4 pond_in_island_in_lake" << endl
             << "    - version   = '" << ((metadata.flag >> 8)  & 255) << "' Values: Should be 12 for GSHHG release 12 (i.e., version 2.2)" << endl
             << "    - greenwich = '" << ((metadata.flag >> 16) & 1  ) << "' Values: Greenwich is 1 if Greenwich is crossed" << endl
             << "    - source    = '" << ((metadata.flag >> 24) & 1  ) << "' Values: 0 = CIA WDBII, 1 = WVS" << endl
             << "    - river     = '" << ((metadata.flag >> 25) & 1  ) << "' Values: 0 = not set, 1 = river-lake and level = 2" << endl
             << "west='"      << metadata.west       << "' /* min/max extent in micro-degrees */ " << endl
             << "east='"      << metadata.east       << "' /* min/max extent in micro-degrees */ " << endl
             << "south='"     << metadata.south      << "' /* min/max extent in micro-degrees */ " << endl
             << "north='"     << metadata.north      << "' /* min/max extent in micro-degrees */ " << endl
             << "area='"      << metadata.area       << "' /* Area of polygon in 1/10 km^2 */ " << endl
             << "area_full='" << metadata.area_full  << "' /* Area of original full-resolution polygon in 1/10 km^2 */ " << endl
             << "container='" << metadata.container  << "' /* Id of container polygon that encloses this polygon (-1 if none) */ " << endl
             << "ancestor='"  << metadata.ancestor   << "' /* Id of ancestor polygon in the full resolution set that was the source of this polygon (-1 if none) */ " << endl
             << endl;
    };

    void print_point(size_t index)
    { cout << "{x=" << points[index].x << ",y=" << points[index].y << "}" << endl; };

    void print_point(GSHHG_POINT & point)
    { cout << "{x=" << point.x << ",y=" << point.y << "}" << endl; };

    void print_points()
    { for( auto & point : points ) { print_point(point); } };

    // Here we can set the state for the class to be more easily mapped
    int max_lat = INT_MIN; int max_lon = INT_MIN;
    int min_lat = INT_MAX; int min_lon = INT_MAX;
    int screen_rows = 0, screen_cols = 0;

    void init( int     _max_lat, int _max_lon 
             , int     _min_lat, int _min_lon 
             , int _screen_rows, int _screen_cols 
             )
    {
        max_lat     = _max_lat    ;
        max_lon     = _max_lon    ;
        min_lat     = _min_lat    ;
        min_lon     = _min_lon    ;
        screen_rows = _screen_rows;
        screen_cols = _screen_cols;
    };

    void set_max_lat(int x) { max_lat = x; }
    void set_max_lon(int x) { max_lon = x; }
    void set_min_lat(int x) { min_lat = x; }
    void set_min_lon(int x) { min_lon = x; }
    void set_screen_rows(int x) { screen_rows = x; }
    void set_screen_cols(int x) { screen_cols = x; }

    double get_normal(int x, int max_x, int min_x) { return ( (double)(x - min_x) )/( (double)(max_x-min_x) ); }
    int    get_screen_lat(GSHHG_POINT & p) { return static_cast<int>( (double)screen_rows * get_normal(p.y, max_lat, min_lat) ); } 
    int    get_screen_lon(GSHHG_POINT & p) { return static_cast<int>( (double)screen_cols * get_normal(p.x, max_lon, min_lon) ); } 
};

int main(int argc, const char *argv[])
{
    struct winsize w;
    ioctl(0, TIOCGWINSZ, &w);

    cout << "Screen lines:   '" << w.ws_row << "'" << endl;
    cout << "Screen columns: '" << w.ws_col << "'" << endl;

    int rows = w.ws_row;
    int cols = w.ws_col;
    
    Screen screen(rows, cols);
    screen.clearAll();

    deque<Dot> dots;
    deque<Polygon> polygons;

    // char * numbers = "0123456789";
    // for(int row=0; row < rows; ++row) for(int col=0; col < cols; ++col)
    // { 
    //     if(row < 10 | col < 60 || col > 80) continue;
    //     dots.push_back( Dot({row, col, 0}, numbers[(row+col)%10]) ); 
    // }
    // dots.push_back( Dot({15, 50, 0}, 'X') );
    // for(Dot & dot : dots) { screen.addSprite(&dot); }
    // screen.printSprite();
    // return 0;


    ifstream data_file("./data/gshhs_c.b"); data_file.peek();
    while(data_file.good())
    {
        Polygon new_poly(data_file);
        //new_poly.print_metadata();
        //new_poly.print_points();

        polygons.push_back(new_poly);
        data_file.peek();
    }

    int max_lat = INT_MIN; int max_lon = INT_MIN;
    int min_lat = INT_MAX; int min_lon = INT_MAX;
    for(auto & polygon : polygons)
    {
        max_lat = (polygon.max_lat >= max_lat) ? polygon.max_lat : max_lat;
        min_lat = (polygon.min_lat <= min_lat) ? polygon.min_lat : min_lat;
                                                                
        max_lon = (polygon.max_lon >= max_lon) ? polygon.max_lon : max_lon;
        min_lon = (polygon.min_lon <= min_lon) ? polygon.min_lon : min_lon;
    }
    cout << "max_lat = " << max_lat << " max_lon = " << max_lon << endl;
    cout << "min_lat = " << min_lat << " min_lon = " << min_lon << endl;

    for(auto & polygon : polygons)
    { 
        polygon.init(max_lat, max_lon, min_lat, min_lon, rows, cols); 
        for(auto & point : polygon.points)
        {
            //cout << "lat idx = " << polygon.get_screen_lat(point) << endl
            //     << "lon idx = " << polygon.get_screen_lon(point) << endl;

            dots.push_back( Dot( { polygon.get_screen_lat(point)
                                 , polygon.get_screen_lon(point) 
                                 , 0 }, '+' ));
        }
    }

    for(Dot & dot : dots) { screen.addSprite(&dot); }
    screen.printAll();

    //for(auto & polygon : polygons) polygon.print_metadata();

};


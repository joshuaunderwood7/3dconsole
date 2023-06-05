#ifndef __GSHHS__NOAA__
#define __GSHHS__NOAA__

#include <arpa/inet.h>

struct GSHHG {  /* Global Self-consistent Hierarchical High-resolution Shorelines */
        int id;         /* Unique polygon id number, starting at 0 */
        int n;          /* Number of points in this polygon */
        int flag;       /* = level + version << 8 + greenwich << 16 + source << 24 + river << 25 */
        /* flag contains 5 items, as follows:
         * low byte:    level = flag & 255: Values: 1 land, 2 lake, 3 island_in_lake, 4 pond_in_island_in_lake
         * 2nd byte:    version = (flag >> 8) & 255: Values: Should be 12 for GSHHG release 12 (i.e., version 2.2)
         * 3rd byte:    greenwich = (flag >> 16) & 1: Values: Greenwich is 1 if Greenwich is crossed
         * 4th byte:    source = (flag >> 24) & 1: Values: 0 = CIA WDBII, 1 = WVS
         * 4th byte:    river = (flag >> 25) & 1: Values: 0 = not set, 1 = river-lake and level = 2
         */
        int west, east, south, north;   /* min/max extent in micro-degrees */
        int area;       /* Area of polygon in 1/10 km^2 */
        int area_full;  /* Area of original full-resolution polygon in 1/10 km^2 */
        int container;  /* Id of container polygon that encloses this polygon (-1 if none) */
        int ancestor;   /* Id of ancestor polygon in the full resolution set that was the source of this polygon (-1 if none) */
};

struct GSHHG_POINT {	/* Each lon, lat pair is stored in micro-degrees in 4-byte signed integer format */
	int32_t x;
	int32_t y;
};


// Datafile is in Big Endian, so we need to convert each field.
void gshhs_convert(int & data) { data = ntohl(data); };

void gshhs_convert(GSHHG & data) 
{ 
    gshhs_convert( data.id        );
    gshhs_convert( data.n         );
    gshhs_convert( data.flag      );
    gshhs_convert( data.west      );
    gshhs_convert( data.east      );
    gshhs_convert( data.south     );
    gshhs_convert( data.north     );
    gshhs_convert( data.area      );
    gshhs_convert( data.area_full );
    gshhs_convert( data.container );
    gshhs_convert( data.ancestor  );
};

void gshhs_convert(GSHHG_POINT & data) 
{
    gshhs_convert( data.x );
    gshhs_convert( data.y );
};

#endif

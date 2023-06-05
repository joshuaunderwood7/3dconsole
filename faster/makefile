CC=g++

<<<<<<< HEAD
DEBUGFLAG=-ggdb -Wall
=======
DEBUGFLAG=-ggdb -Wall -w
>>>>>>> b2ac55a (Added GSHHS data to repo, and added console plot of map for C++)
PROFILEFLAG=-pg
CPPFLAGS=-std=c++11
OPTFLAGS=-O3 -s

IDIRS=\
			-I./inc/

STATICLIBS=

LIBS=

SRC=\
    src/shapes.cpp\
    src/screen.cpp\
    src/quaternion.cpp

INC_SRC_LIB=\
	    $(IDIRS) \
	    $(SRC) \
	    $(LIBS)

<<<<<<< HEAD
=======
map:
	$(CC) \
	    $(INC_SRC_LIB) \
	    src/map.cpp \
	    $(STATICLIBS) \
	    $(CPPFLAGS) \
	    $(DEBUGFLAG) \
	    -o bin/map

>>>>>>> b2ac55a (Added GSHHS data to repo, and added console plot of map for C++)
3dconsole:
	$(CC) \
	    $(INC_SRC_LIB) \
	    src/3dconsole.cpp \
	    $(STATICLIBS) \
	    $(CPPFLAGS) \
	    $(DEBUGFLAG) \
	    -o bin/3dconsole

quaternion:
	$(CC) \
	    $(INC_SRC_LIB) \
	    src/test.cpp \
	    $(STATICLIBS) \
	    $(CPPFLAGS) \
	    $(DEBUGFLAG) \
	    -o bin/quaternion

<<<<<<< HEAD
.PHONEY: all clean

all: 3dconsole
=======
sgp4:
	$(CC) \
	    $(INC_SRC_LIB) \
	    src/SGP4.c \
	    src/TLE.cpp \
	    src/TestSGP4.cpp \
	    $(STATICLIBS) \
	    $(CPPFLAGS) \
	    $(DEBUGFLAG) \
	    -o bin/TestSGP4

.PHONEY: all clean

all: map
>>>>>>> b2ac55a (Added GSHHS data to repo, and added console plot of map for C++)

clean:
	rm bin/*
	touch bin/dummyfile


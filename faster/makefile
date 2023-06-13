CC=g++

DEBUGFLAG=-ggdb -Wall -w
PROFILEFLAG=-pg
CPPFLAGS=-std=c++17
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

map:
	$(CC) \
	    $(INC_SRC_LIB) \
	    src/map.cpp \
	    $(STATICLIBS) \
	    $(CPPFLAGS) \
	    $(DEBUGFLAG) \
	    -o bin/map

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

clean:
	rm bin/*
	touch bin/dummyfile


CC=g++

DEBUGFLAG=-ggdb -Wall
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

.PHONEY: all clean

all: 3dconsole

clean:
	rm bin/*
	touch bin/dummyfile


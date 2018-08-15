#ifndef SCREEN_H
#define SCREEN_H

#include <shapes.h>

#include <iostream>
#include <string>

using namespace std;

string GREY_SCALE_FULL  = "$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\\|()1{}[]?-_+~<>i!lI;:,\"^`'. ";
string GREY_SCALE_10    = "@%#*+=-:. ";
const int HEIGHT = (24 * 2) + 6;
const int WIDTH  = 80 * 2;
char      SCREEN[WIDTH*HEIGHT];

/* Printing to the screen */
class Screen
{
    private:
        Vec3   eye;
        int    index;

    public:

        Screen() 
        {
            eye = {0.0, 0.0, -20.0};
        }

        ~Screen() {}

        void setEye(Vec3 eye)     { this->eye  = eye;  }

        void gotoxy(int x, int y) { cout << "\033[" << x << ";" << y << "H"; };
        void clearScreen() { for(int ii=WIDTH*HEIGHT; ii>=0; --ii) SCREEN[ii]=0x7F; }

        void addShape(Shape * shape);

        void printScreen();

};


#endif

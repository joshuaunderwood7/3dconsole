#ifndef SCREEN_H
#define SCREEN_H

#include <shapes.h>

#include <iostream>
#include <string>

using namespace std;


/* Printing to the screen */
class Screen
{
    private:
        Vec3   eye;
        int    index;
        string GREY_SCALE_FULL  = "$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\\|()1{}[]?-_+~<>i!lI;:,\"^`'. ";
        string GREY_SCALE_10    = "@%#*+=-:. ";
        int    HEIGHT = (24 * 2) + 6;
        int    WIDTH  = 80 * 2;
        char*  SCREEN;

    public:

        Screen() 
        {
            eye = {0.0, 0.0, -20.0};
            SCREEN = (char *)malloc(WIDTH*HEIGHT * sizeof(char));
        }

        Screen(int height_in, int width_in) 
        {
            eye = {0.0, 0.0, -20.0};
            HEIGHT = height_in;
            WIDTH  = width_in;
            SCREEN = (char *)malloc(WIDTH*HEIGHT * sizeof(char));
        }

        ~Screen() {}

        void setEye(Vec3 eye)     { this->eye  = eye;  }

        void gotoxy(int x, int y) { cout << "\033[" << x << ";" << y << "H"; };
        void clearScreen() { for(int ii=WIDTH*HEIGHT; ii>=0; --ii) SCREEN[ii]=0x7F; }

        void addShape(Shape * shape);

        void printScreen();

};


#endif

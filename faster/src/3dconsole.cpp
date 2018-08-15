#include <iostream>
#include <string>

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
        double dist;
        int    index;

    public:

        Screen() 
        {
            dist = (1.0); 
            eye = {0.0, 0.0, -20.0};
        }

        ~Screen() {}

        void setEye(Vec3 eye)     { this->eye  = eye;  }
        void setDist(double dist) { this->dist = dist; }

        void gotoxy(int x, int y) { cout << "\033[" << x << ";" << y << "H"; };
        void clearScreen() { for(int ii=WIDTH*HEIGHT; ii>=0; --ii) SCREEN[ii]=0x7F; }

        void addShape(Shape * shape)
        {
            for(Vec3 point : shape->perspectiveDivision(eye))
            {
                if (point[0] < -1.0 || point[0] > 1.0) continue;
                if (point[1] < -1.0 || point[1] > 1.0) continue;

                index = ( int((HEIGHT-1) * ((point[0] + 1) / 2.0) ) * WIDTH ) 
                        + int( (WIDTH-1) * ((point[1] + 1) / 2.0) );

                if (SCREEN[index] > point[2]) SCREEN[index] = point[2];
            }
        }

        void printScreen()
        {
            gotoxy(0,0);
            int outindex;
            int MAX_DEPTH = 69;

            for(int y=0; y<HEIGHT; ++y) 
            {
                for(int x=0; x<WIDTH; ++x) 
                {
                    index = ( y  * WIDTH ) + x ;
                    outindex = SCREEN[index];
                    if (outindex > MAX_DEPTH) outindex = MAX_DEPTH;
                    cout << GREY_SCALE_FULL[outindex];
                }
                cout << endl;
            }
        }

};

void printShape(Shape * shape)
{
    for (auto point : shape->getPoints()) 
    {
        for (auto p : point) 
            cout << p << " ";
        cout << endl;
    }
};

int main(int argc, const char *argv[])
{
    Screen screen;

    Cube testShape({0,0,0}, 9, 10);

    testShape.setRotation({0,0,1}, M_PI/2);
    testShape.rotate();

    testShape.setRotation({1,5,3}, 0.0119);

    int N = 10000;
    for(int ii=0; ii<=N; ++ii)
    {
        screen.clearScreen();
        screen.addShape(&testShape);
        screen.printScreen();
        testShape.rotate();
    }

    return 0;
}

//void draw_square()
//{
    //Screen screen;

    //Line testLine1 ({ 5, 5, 5},{ 5, 5,-5},20);
    //Line testLine2 ({ 5, 5, 5},{ 5,-5, 5},20);
    //Line testLine3 ({ 5, 5, 5},{-5, 5, 5},20);
    //Line testLine4 ({-5,-5,-5},{-5,-5, 5},20);
    //Line testLine5 ({-5,-5,-5},{-5, 5,-5},20);
    //Line testLine6 ({-5,-5,-5},{ 5,-5,-5},20);

    //Line testLine7 ({ 5, 5,-5},{ 5,-5,-5},20);
    //Line testLine8 ({ 5, 5,-5},{-5, 5,-5},20);
    //Line testLine9 ({ 5,-5, 5},{ 5,-5,-5},20);
    //Line testLine10({ 5,-5, 5},{-5,-5, 5},20);
    //Line testLine11({-5, 5, 5},{-5, 5,-5},20);
    //Line testLine12({-5, 5, 5},{-5,-5, 5},20);

    //testLine1.setOrigin({0,0,0});
    //testLine2.setOrigin({0,0,0});
    //testLine3.setOrigin({0,0,0});
    //testLine4.setOrigin({0,0,0});
    //testLine5.setOrigin({0,0,0});
    //testLine6.setOrigin({0,0,0});
    //testLine7.setOrigin({0,0,0});
    //testLine8.setOrigin({0,0,0});
    //testLine9.setOrigin({0,0,0});
    //testLine10.setOrigin({0,0,0});
    //testLine11.setOrigin({0,0,0});
    //testLine12.setOrigin({0,0,0});

    //testLine1.setRotation ({1,2,3}, 0.0015);
    //testLine2.setRotation ({1,2,3}, 0.0015);
    //testLine3.setRotation ({1,2,3}, 0.0015);
    //testLine4.setRotation ({1,2,3}, 0.0015);
    //testLine5.setRotation ({1,2,3}, 0.0015);
    //testLine6.setRotation ({1,2,3}, 0.0015);
    //testLine7.setRotation ({1,2,3}, 0.0015);
    //testLine8.setRotation ({1,2,3}, 0.0015);
    //testLine9.setRotation ({1,2,3}, 0.0015);
    //testLine10.setRotation({1,2,3}, 0.0015);
    //testLine11.setRotation({1,2,3}, 0.0015);
    //testLine12.setRotation({1,2,3}, 0.0015);

    //int N = 10000;
    //for(int ii=0; ii<=N; ++ii)
    //{
        //screen.clearScreen();

        //screen.addShape(testLine1 );
        //screen.addShape(testLine2 );
        //screen.addShape(testLine3 );
        //screen.addShape(testLine4 );
        //screen.addShape(testLine5 );
        //screen.addShape(testLine6 );
        //screen.addShape(testLine7 );
        //screen.addShape(testLine8 );
        //screen.addShape(testLine9 );
        //screen.addShape(testLine10);
        //screen.addShape(testLine11);
        //screen.addShape(testLine12);

        //screen.printScreen();

        //testLine1.rotate();
        //testLine2.rotate();
        //testLine3.rotate();
        //testLine4.rotate();
        //testLine5.rotate();
        //testLine6.rotate();
        //testLine7.rotate();
        //testLine8.rotate();
        //testLine9.rotate();
        //testLine10.rotate();
        //testLine11.rotate();
        //testLine12.rotate();
    //}


//}


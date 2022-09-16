#include <iostream>
#include <string>
#include <deque>
#include <unistd.h>

#include <shapes.h>
#include <screen.h>

#include <iostream>
#include <string>
using namespace std;

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
    Screen screen(24, 80);

    Line line({0,0,0}, {5,5,0});
    Cube cube({-5,-5,0}, 16);
    Dot dot({2,2,0}, '$');

    cube.setRotation({0,.1,1}, M_PI/200);

    int N = 10000;
    for(int ii=0; ii<N; ++ii)
    {
        screen.clearScreen();

        //screen.addShape(&line);
        screen.addShape(&cube);
        screen.addSprite(&dot);

        screen.printScreen();
        //screen.printSprite();

        cube.rotate();

        usleep(1000);
    }
    
    return 0;
}

int main_old(int argc, const char *argv[])
{
    Screen screen(57, 217);

    Cube cubes[2] = { Cube({-5,-5,-5}, 9, 10)
                    , Cube({ 5, 5, 5}, 9, 10)
                    };


    cubes[0].setRotation({0,0,1}, M_PI/2);
    cubes[0].rotate();

    cubes[1].setRotation({1,0,0}, M_PI/3);
    cubes[1].rotate();

    cubes[0].setRotation({ 1, 5,-3}, 0.00819);
    cubes[1].setRotation({-3, 7, 2}, 0.00819);

    int N = 10000;
    for(int ii=0; ii<=N; ++ii)
    {
        screen.clearScreen();

        for (Cube &cube : cubes)
            screen.addShape(&cube);

        screen.printScreen();
        usleep(10000);

        for (Cube &cube : cubes)
            cube.rotate();
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


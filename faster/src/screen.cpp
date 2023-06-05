#include <screen.h>

void Screen::addShape(Shape * shape)
{
    for(Vec3 point : shape->perspectiveDivision(eye))
    {
        if (point[0] < -1.0 || point[0] > 1.0) continue;
        if (point[1] < -1.0 || point[1] > 1.0) continue;

        index = ( int((HEIGHT-1) * ((point[0] + 1) / 2.0) ) * WIDTH ) 
                + int( (WIDTH-1) * ((point[1] + 1) / 2.0) );

        if (SCREEN[index] > point[2]) SCREEN[index] = point[2];
    }
};

void Screen::addSprite(Sprite * sprite)
{
<<<<<<< HEAD
    for(Vec3 point : sprite->perspectiveDivision(eye))
    {
        if (point[0] < -1.0 || point[0] > 1.0) continue;
        if (point[1] < -1.0 || point[1] > 1.0) continue;

        index = ( int((HEIGHT-1) * ((point[0] + 1) / 2.0) ) * WIDTH ) 
                + int( (WIDTH-1) * ((point[1] + 1) / 2.0) );

        SPRITE[index] = point[2];
=======
    
    for(Vec3 point : sprite->getPoints(eye))
    {
        if (point[0] < 0 || point[0] >= HEIGHT) continue;
        if (point[1] < 0 || point[1] >= WIDTH ) continue;

        index = ( point[0] * WIDTH ) + point[1] ;
        SPRITE[index] = sprite->symbol;
>>>>>>> b2ac55a (Added GSHHS data to repo, and added console plot of map for C++)
    }
};

void Screen::printScreen()
{
<<<<<<< HEAD
    gotoxy(0,0);
=======
>>>>>>> b2ac55a (Added GSHHS data to repo, and added console plot of map for C++)
    int outindex;
    int MAX_DEPTH = 69;

    for(int y=0; y<HEIGHT; ++y) 
    {
        for(int x=0; x<WIDTH; ++x) 
        {
<<<<<<< HEAD
=======
            gotoxy(HEIGHT-y,x);
>>>>>>> b2ac55a (Added GSHHS data to repo, and added console plot of map for C++)
            index = ( y  * WIDTH ) + x ;
            outindex = SCREEN[index];
            if (outindex > MAX_DEPTH) outindex = MAX_DEPTH;
            cout << GREY_SCALE_FULL[outindex];
        }
        cout << endl;
    }
};

void Screen::printSprite()
{
<<<<<<< HEAD
    gotoxy(0,0);
=======
>>>>>>> b2ac55a (Added GSHHS data to repo, and added console plot of map for C++)
    for(int y=0; y<HEIGHT; ++y) 
    {
        for(int x=0; x<WIDTH; ++x) 
        {
<<<<<<< HEAD
=======
            gotoxy(HEIGHT-y,x);
>>>>>>> b2ac55a (Added GSHHS data to repo, and added console plot of map for C++)
            index = ( y  * WIDTH ) + x ;
            cout << SPRITE[index];;
        }
        cout << endl;
    }
};


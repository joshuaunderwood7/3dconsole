#ifndef SHAPES_H
#define SHAPES_H

#include <quaternion.h>

#include <cmath>
#include <deque>
#include <vector>

using namespace std;

typedef deque<double> Vec3;

Vec3   add   (Vec3 A, Vec3 B);
Vec3   sub   (Vec3 A, Vec3 B);
double dot   (Vec3 A, Vec3 B);
Vec3   cross (Vec3 A, Vec3 B);

Vec3 scale(double, Vec3);
Vec3 scale(  Vec3, double);

bool sameside3d( Vec3 p    // Perspective Point
               , Vec3 ref  // Reference Point
               , Vec3 A, Vec3 B, Vec3 C  // Shape Plane points
               );

Vec3 perspective_division( Vec3   & eye
                         , Vec3     point
                         , double   plane_dist=1.0
                         );

class Shape
{
    public:

        virtual deque<Vec3> getPoints   (Vec3 & eye)=0;

        deque<Vec3> getPoints   ()                   { return points; };
        void        setPoints   (deque<Vec3> points) { this->points = points; };

        void setRotation        ( Vec3   RotationVector
                                , double RotationAngle
                                );
        void setOrigin          (Vec3 origin)          { this->origin = origin; };
        void rotate             ();                       // Rotate the shape by RotationVector and RotationAngle

        void shift              (Vec3 offset); 

        deque<Vec3> perspectiveDivision(Vec3 & eye, double plane_dist=1.0);

    protected:

        deque<Vec3>         points;
        Vec3                origin;
        Quaternion<double>  q_RotationVector;
        double              RotationAngle;

};

class Sprite : public Shape
{
    public:
        char symbol;
};

class Dot : public Sprite
{
    public:

        Dot(Vec3 A, char symbol);
        virtual deque<Vec3> getPoints   (Vec3 & eye) { return points; }
};

class Line : public Shape
{
    public:

        Line(Vec3 A, Vec3 B, int N=10);
        virtual deque<Vec3> getPoints   (Vec3 & eye) { return points; }
};


class Tri : public Shape
{
    public:

        Tri(Vec3 & A, Vec3 & B, Vec3 & C, int N=10);
        virtual deque<Vec3> getPoints   (Vec3 & eye) { return fill(); };

        deque<Vec3> fill();

        Vec3 getA() { return points[0]; }
        Vec3 getB() { return points[1]; }
        Vec3 getC() { return points[2]; }

        void setA(Vec3 x) { points[0] = x; }
        void setB(Vec3 x) { points[1] = x; }
        void setC(Vec3 x) { points[2] = x; }

    private:
        int  N;
};


class Tetrahedron : public Shape
{
    public:

        Tetrahedron();
        Tetrahedron(const Tetrahedron &original);
        Tetrahedron(Vec3 A, Vec3 B, Vec3 C, Vec3 D, int N=10);
        virtual deque<Vec3> getPoints   (Vec3 & eye) { return shell_vis(eye); };

        deque<Vec3> shell_vis(Vec3 & eye, bool bottom=true);

        Vec3 getA() const { return points[0]; }
        Vec3 getB() const { return points[1]; }
        Vec3 getC() const { return points[2]; }
        Vec3 getD() const { return points[3]; }

        void setA(Vec3 x) { points[0] = x; }
        void setB(Vec3 x) { points[1] = x; }
        void setC(Vec3 x) { points[2] = x; }
        void setD(Vec3 x) { points[3] = x; }

        int  getN() const { return N; }
        void setN(int n)  { N=n; }

    private:
        int  N;
};

class Cube : public Shape
{
    public:

        Cube(const Cube& original);
        Cube(Vec3 center, double side_length, int N=10);
        virtual deque<Vec3> getPoints   (Vec3 & eye);

        void rotate     ();
        void setRotation(Vec3 RotationVector, double RotationAngle);

    private:
        Tetrahedron A,B,C,D, middle;
}; 

#endif

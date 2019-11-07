#include <shapes.h>

Vec3 add     (Vec3 A, Vec3 B)     { return {A[0]+B[0],A[1]+B[1],A[2]+B[2]}; };
Vec3 sub     (Vec3 A, Vec3 B)     { return {A[0]-B[0],A[1]-B[1],A[2]-B[2]}; };

Vec3 scale   (double a,   Vec3 B) { return {a*B[0],a*B[1],a*B[2]}; };
Vec3 scale   (  Vec3 B, double a) { return {a*B[0],a*B[1],a*B[2]}; };

double dot   (Vec3 A, Vec3 B)     { return (A[0]*B[0])+(A[1]*B[1])+(A[2]*B[2]); };
Vec3   cross (Vec3 A, Vec3 B)     { 
    return { (A[1]*B[2])-(A[2]*B[1]) 
           , (A[2]*B[0])-(A[0]*B[2]) 
           , (A[0]*B[1])-(A[1]*B[0]) 
           };
};

bool sameside3d( Vec3 p    // Perspective Point
               , Vec3 ref  // Reference Point
               , Vec3 A, Vec3 B, Vec3 C  // Shape Plane points
               )
{
    Vec3   cpAB_BC  = cross(sub(A,B), sub(A,C));
    double sameABCr = dot(sub(ref,A), cpAB_BC);
    double sameABCp = dot(sub(  p,A), cpAB_BC);

    if ( sameABCr < 0 && sameABCp < 0 ) return true;
    if ( sameABCr > 0 && sameABCp > 0 ) return true;

    return false;
}

Vec3 perspective_division( Vec3   & eye
                         , Vec3     point
                         , double   plane_dist
                         )
{
    point[2] = point[2] - eye[2];
    for(int ii=0; ii<2; ++ii)
      point[ii] = (point[ii] - eye[ii]) * plane_dist/point[2];
    return point;
};

deque<Vec3> Shape::perspectiveDivision(Vec3 & eye, double plane_dist)
{
    deque<Vec3> result;
    for(Vec3 point : this->getPoints(eye))
        result.push_back(perspective_division(eye, point, plane_dist));

    return result;
}


void Shape::setRotation( Vec3   RotationVector
                       , double RotationAngle
                       )
{
    double sqSum = sqrt(RotationVector[0]+RotationVector[1]+RotationVector[2]);
    double halfAngle = RotationAngle/2.0;
    double sinHfAngl = sin(halfAngle);
    q_RotationVector = Quaternion<double>( cos(halfAngle)
                                         , (RotationVector[0]/sqSum)*sinHfAngl
                                         , (RotationVector[1]/sqSum)*sinHfAngl
                                         , (RotationVector[2]/sqSum)*sinHfAngl
                                         );
};


// Rotate the shape by RotationVector and RotationAngle
void Shape::rotate()
{
    double new_point[3];
    int ii;
    for(auto &point : points)
    {
        for (ii=0; ii<3; ++ii) new_point[ii] = point[ii] - origin[ii];

        q_RotationVector.QuatRotation(new_point);

        for (ii=0; ii<3; ++ii) point[ii] = new_point[ii] + origin[ii];
    }
};

void Shape::shift(Vec3 offset) 
{
    for(auto &point : points)
    {
        point[0] += offset[0];
        point[1] += offset[1];
        point[2] += offset[2];
    }
    origin[0] += offset[0];
    origin[1] += offset[1];
    origin[2] += offset[2];
};

Line::Line(Vec3 A, Vec3 B, int N)
{
    double deltaX = (B[0] - A[0])/N;
    double deltaY = (B[1] - A[1])/N;
    double deltaZ = (B[2] - A[2])/N;
    for(int index=0; index<=N; ++index)
    {
        Vec3 point;
        point.push_back(A[0] + (index * deltaX));
        point.push_back(A[1] + (index * deltaY));
        point.push_back(A[2] + (index * deltaZ));
        this->points.push_back(point);
    }
    this->origin = A;
};


Tri::Tri(Vec3 & A, Vec3 & B, Vec3 & C, int N)
{
    this->N = N;

    points.push_back(A);
    points.push_back(B);
    points.push_back(C);

    setOrigin({ (points[0][0]+points[1][0]+points[2][0])/3.0
              , (points[0][1]+points[1][1]+points[2][1])/3.0
              , (points[0][2]+points[1][2]+points[2][2])/3.0
              });
};

deque<Vec3> Tri::fill()
{
    Vec3 AB = sub(points[1], points[0]);
    Vec3 AC = sub(points[2], points[0]);

    deque<Vec3> result;
    for(double u=0.0; u<=1.0; u+=0.99/N)
    {
        for(double v=0.0; v<=1.0; v+=1.0/N)
        {
            if ( (u+v) >= 1.0 ) continue;
            result.push_back(add(points[0],add(scale(u,AC),scale(v,AB))));
        }
    }
    return result;
};


Tetrahedron::Tetrahedron()
{
    N = 0;
    points.push_back({0,0,0});
    points.push_back({0,0,0});
    points.push_back({0,0,0});
    points.push_back({0,0,0});
    setOrigin({0,0,0});
};

Tetrahedron::Tetrahedron(const Tetrahedron &original)
{
    this->setA(original.getA());
    this->setB(original.getB());
    this->setC(original.getC());
    this->setD(original.getD());
    this->setN(original.getN());

    setOrigin({ (points[0][0]+points[1][0]+points[2][0]+points[3][0])/4.0
              , (points[0][1]+points[1][1]+points[2][1]+points[3][1])/4.0
              , (points[0][2]+points[1][2]+points[2][2]+points[3][2])/4.0
              });
};

Tetrahedron::Tetrahedron(Vec3 A, Vec3 B, Vec3 C, Vec3 D, int N)
{
    this->N = N;
    points.push_back(A);
    points.push_back(B);
    points.push_back(C);
    points.push_back(D);

    setOrigin({ (points[0][0]+points[1][0]+points[2][0]+points[3][0])/4.0
              , (points[0][1]+points[1][1]+points[2][1]+points[3][1])/4.0
              , (points[0][2]+points[1][2]+points[2][2]+points[3][2])/4.0
              });
};


deque<Vec3> Tetrahedron::shell_vis(Vec3 & eye, bool bottom)
{
    deque<Vec3> result;
    bool seeA =  sameside3d(eye, points[0], points[1], points[2], points[3]);
    bool seeB =  sameside3d(eye, points[1], points[2], points[3], points[0]);
    bool seeC =  sameside3d(eye, points[2], points[3], points[0], points[1]);
    bool seeD =  sameside3d(eye, points[3], points[0], points[1], points[2]);

    if (!seeD)           for(auto const &point :Tri(points[0],points[1],points[2], N).fill()) { result.push_back(point); }
    if (!seeB)           for(auto const &point :Tri(points[0],points[2],points[3], N).fill()) { result.push_back(point); }
    if (!seeC)           for(auto const &point :Tri(points[0],points[1],points[3], N).fill()) { result.push_back(point); }
    if (!seeA && bottom) for(auto const &point :Tri(points[1],points[2],points[3], N).fill()) { result.push_back(point); }

    return result;
};

Cube::Cube(const Cube& original)
{
    this->A      = original.A;
    this->B      = original.B;
    this->C      = original.C;
    this->D      = original.D;
    this->middle = original.middle;
};

Cube::Cube(Vec3 center, double side_length, int N)
{
    double half_width = side_length/2;
    this->setOrigin(center);

    middle = Tetrahedron( {-half_width,-half_width,-half_width}
                        , { half_width, half_width,-half_width}
                        , {-half_width, half_width, half_width}
                        , { half_width,-half_width, half_width}
                        , N
                        );

    A = Tetrahedron( scale(-1, middle.getA()), middle.getB(), middle.getC(), middle.getD(), N);
    B = Tetrahedron( scale(-1, middle.getB()), middle.getA(), middle.getC(), middle.getD(), N);
    C = Tetrahedron( scale(-1, middle.getC()), middle.getA(), middle.getB(), middle.getD(), N);
    D = Tetrahedron( scale(-1, middle.getD()), middle.getA(), middle.getB(), middle.getC(), N);

    middle.shift(center);
    A.shift(center);
    B.shift(center);
    C.shift(center);
    D.shift(center);

    A.setOrigin(center);
    B.setOrigin(center);
    C.setOrigin(center);
    D.setOrigin(center);
};


deque<Vec3> Cube::getPoints(Vec3 & eye) 
{ 
    deque<Vec3> result;
    for(auto const &point : A.shell_vis(eye, false)) result.push_back(point);
    for(auto const &point : B.shell_vis(eye, false)) result.push_back(point);
    for(auto const &point : C.shell_vis(eye, false)) result.push_back(point);
    for(auto const &point : D.shell_vis(eye, false)) result.push_back(point);
    return result;
};

void Cube::rotate()
{
    middle.rotate();
    A.rotate();
    B.rotate();
    C.rotate();
    D.rotate();
};

void Cube::setRotation(Vec3 RotationVector, double RotationAngle)
{
    middle.setRotation(RotationVector, RotationAngle);
    A.setRotation(RotationVector, RotationAngle);
    B.setRotation(RotationVector, RotationAngle);
    C.setRotation(RotationVector, RotationAngle);
    D.setRotation(RotationVector, RotationAngle);
};


struct vertex3D 
{
	float x;
	float y;
	float z;
};

struct vector3D
{
	float x;
	float y;
	float z;
};

struct face3D
{
	vertex3D v1;
	vertex3D v2;
	vertex3D v3; 
	vertex3D v4;
};

struct colour
{
	float r, g, b;
};

float vertexPlaneDistance(struct vertex3D a, struct vertex3D b)
{
	return sqrt(pow(a.x - b.x, 2) + pow(a.z - b.z, 2));
};

vector3D makeVector(vertex3D a, vertex3D b)
{	vector3D vector;
	vector.x = b.x - a.x;
	vector.y = b.y - a.y;
	vector.z = b.z - a.z;
	return vector;
};

vector3D cross(struct vector3D a, struct vector3D b)
{
	vector3D cross;
	cross.x = a.y*b.z - a.z*b.y;
	cross.y = b.x*a.z - a.x*b.z;
	cross.z = a.x*b.y - a.y*b.x;
	return cross;
};

float magnitude(vector3D a)
{
	return sqrt(pow(a.x, 2) + pow(a.y, 2) + pow(a.z, 2));
}

vector3D unitVector(struct vector3D a)
{
	float mag = magnitude(a);
	a.x = a.x/mag;
	a.y = a.y/mag;
	a.z = a.z/mag;
	return a;
};

vector3D addVector(struct vector3D a, struct vector3D b)
{
	vector3D add;
	add.x = a.x + b.x;
	add.y = a.y + b.y;
	add.z = a.z + b.z;
	return add;
};
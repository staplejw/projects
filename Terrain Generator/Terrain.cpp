#include <stdio.h>
#include <stdlib.h>
#include <iostream>
#include <math.h>
#include "mesh.h"
#include <ctime>

#ifdef __APPLE__
#  include <OpenGL/gl.h>
#  include <OpenGL/glu.h>
#  include <GLUT/glut.h>
#else
#  include <GL/gl.h>
#  include <GL/glu.h>
#  include <GL/freeglut.h>
#endif

int gridsize = 50; // default grid size
vertex3D** grid; // stores x, y and z coordinates for every point on the grid
vector3D** squareVertexNormals; // variable for storing square vertex normal data
vector3D** triangleVertexNormals; // variable for storing triangle vertex normal data
float camPos[3] = {-1.2*gridsize, 1.2*gridsize, -1.2*gridsize}; // determines location of the camera and is scaled based on the chosen gridsize


float light_pos[4] = {2*gridsize, 2*gridsize, -2*gridsize, 1.0}; // determines location of light0
float light_pos1[4] = {-2*gridsize, 2*gridsize, 2*gridsize, 1.0}; // determines location of light1
float amb0[] = {1, 1, 1, 1}; // light0 characteristics 
float diff0[] = {0.5, 0.5, 0.5, 1};
float spec0[] = {1, 1, 1, 1};

float amb1[] = {1, 1, 1, 1}; // light1 characteristics
float diff1[] = {0.5, 0.5, 0.5, 1};
float spec1[] = {1, 1, 1, 1};

float m_amb[] = {0.33, 0.22, 0.03, 1}; // material characteristics 
float m_diff[] = {0.78, 0.57, 0.11, 1};
float m_spec[] = {0.99, 0.91, 0.81, 1};
float shiny = 27.5;

char mode = 's'; // variable which determines the viewing mode (solid, wireframe, or both) default viewing mode is solid
char primitive = 'S'; // default primitive type is squares int foo = 0; 
char shade = 'f';
int foo = 0; // dummy variable for toggling viewing mode
int bar = 0; // dummy variable for toggling shading
int light = 0; // dummy variable for toggling lighting
int which_light = 0; // dummy variable for toggling which light position you are controlling
colour wireframeColour = {1, 0, 0}; // sets the colour to draw wireframe meshes
int iterations = 300; // number of iterations that the circles algorithm will go through
int radius; // radius of each "circle"
int height; // height of each "cirlce"
float maxHeight; // stores the maximum height value for a given mesh
float minHeight; // stores the minimum height value for a given mesh
float range; // defined as (maxHeight - minHeight)
int menu; // ID number for the menu
int window_1, window_2; // ID number for the two windows that open
int sizes[4] = {50, 100, 200, 300}; // 4 possible gridsizes
int radii[4] = {5, 10, 15, 20}; // 4 possible radii
int heights[4] = {3, 5, 8, 12}; // 4 possible heights

// creates a grid of points on the x-z plane, all initialized to a height of 0
void makeGrid(int gridsize)
{

	grid = new vertex3D*[gridsize];
	for(int i = 0; i < gridsize; i++)
	{
		grid[i] = new vertex3D[gridsize];
	}
	for( int i = 0; i < gridsize; i++ )
	{
		for( int j = 0; j < gridsize; j++ )
		{
			vertex3D P = {j, 0, i};
			grid[i][j] = P;
		}
	}
}

// implementation of the cirlces algorithm, iterates through each point on the grid and assigns it a height based on the cirlces
void giveGridHeight(vertex3D** grid)
{
	srand(time(NULL));
	maxHeight = 1;
	minHeight = 1;
	for (int i = 0; i < 4; i++)
	{
		if (gridsize == sizes[i])
		{
			radius = radii[i];
			height = heights[i];
		}
	}
	for(int iter = 1; iter <= iterations; iter++ )
	{
		int rand1 = rand() % gridsize;
		int rand2 = rand() % gridsize;

		for( int i = 0; i < gridsize; i++ )
		{
			for( int j = 0; j < gridsize; j++ )
			{
				float pd = vertexPlaneDistance(grid[i][j], grid[rand1][rand2]);
				if( abs(pd) <= radius )
				{
					grid[i][j].y += height/2 + height/2*cos(pd*3.14159/radius);			
					if (grid[i][j].y > maxHeight)
					{
						maxHeight = grid[i][j].y;
					}
					if (grid[i][j].y < minHeight)
					{
						minHeight = grid[i][j].y;
					}
				}
			}
		}
	}
	range = maxHeight - minHeight;
}


void makeSquareVertexNormals()
{
	squareVertexNormals = new vector3D*[gridsize]; 
	for (int i = 0; i < gridsize; i++)
	{
		squareVertexNormals[i] = new vector3D[gridsize]; 
	}
	for (int i = 0; i < gridsize; i++) // initialize all vectors to (0, 0, 0)
	{
		for (int j = 0; j < gridsize; j++)
		{
			squareVertexNormals[i][j] = {0, 0, 0}; 
		}
	}
	vector3D a, b;
	for (int i = 0; i < gridsize - 1; i++) // use cross products to calculate face normals
	{
		for (int j = 0; j < gridsize - 1; j++)
		{
			a = makeVector(grid[i][j], grid[i + 1][j]); 
			b = makeVector(grid[i][j], grid[i][j + 1]); 
			squareVertexNormals[i][j] = unitVector(cross(a, b)); 
			if (shade == 'o') // if smooth shading is on, the program uses vertex normals instead of face normals
			{
				squareVertexNormals[i + 1][j] = addVector(squareVertexNormals[i+1][j], unitVector(cross(a, b))); 
				squareVertexNormals[i][j + 1] = addVector(squareVertexNormals[i][j+1], unitVector(cross(a, b))); 
				squareVertexNormals[i + 1][j + 1] = addVector(squareVertexNormals[i+1][j+1], unitVector(cross(a, b))); 
			}
		}
	}
	if (shade == 'f')
	{
		for (int i = 0; i < gridsize - 1; i++)
		{
			squareVertexNormals[i][gridsize - 1] = squareVertexNormals[i][gridsize - 2];
		}
	}
	for (int i = 0; i < gridsize; i++) // once loop is done, normalize all the vectors
	{
		for (int j = 0; j < gridsize; j++)
		{
			squareVertexNormals[i][j] = unitVector(squareVertexNormals[i][j]); 
		}
	}
}

// same as square normals, uses face normals for flat shading and vertex normals for smooth
void makeTriangleVertexNormals()
{
	triangleVertexNormals = new vector3D*[gridsize]; 
	for (int i = 0; i < gridsize; i++)
	{
		triangleVertexNormals[i] = new vector3D[gridsize]; 
	}
	for (int i = 0; i < gridsize; i++)
	{
		for (int j = 0; j < gridsize; j++)
		{
			triangleVertexNormals[i][j] = {0, 0, 0}; 
		}
	}
	vector3D a, b, c, d;
	for (int i = 0; i < gridsize - 1; i++)
	{
		for (int j = 0; j < gridsize - 1; j++)
		{
			
			a = makeVector(grid[i][j], grid[i + 1][j]);
			b = makeVector(grid[i][j], grid[i][j + 1]);
			c = makeVector(grid[i+1][j], grid[i + 1][j+1]);
			d = makeVector(grid[i+1][j], grid[i][j + 1]);
			triangleVertexNormals[i][j] = addVector(triangleVertexNormals[i][j], unitVector(cross(a, b))); 
			triangleVertexNormals[i+1][j+1] = addVector(triangleVertexNormals[i+1][j+1], unitVector(cross(c, d))); 
			if (shade == 'o')
			{
				triangleVertexNormals[i+1][j] = addVector(triangleVertexNormals[i+1][j], unitVector(cross(a, b))); 
				triangleVertexNormals[i][j+1] = addVector(triangleVertexNormals[i][j+1], unitVector(cross(a, b))); 
				triangleVertexNormals[i+1][j] = addVector(triangleVertexNormals[i+1][j], unitVector(cross(c, d))); 
				triangleVertexNormals[i][j+1] = addVector(triangleVertexNormals[i][j+1], unitVector(cross(c, d)));
			}
 
		}
	}
	for (int i = 0; i < gridsize; i++)
	{
		for (int j = 0; j < gridsize; j++)
		{
			triangleVertexNormals[i][j] = unitVector(triangleVertexNormals[i][j]); 
		}
	}
}

// simply dellalocates all the memory associated with the variable grid
void deallocateGrid()
{
	for(int i = 0; i < gridsize; i++)
	{
		delete [] grid[i];
	}
	delete [] grid;
}

// same but for the square and vertex normals
void deallocateNormals()
{
	for(int i = 0; i < gridsize; i++)
	{
		delete [] squareVertexNormals[i]; 
	}
	delete [] squareVertexNormals; 
	for(int i = 0; i < gridsize; i++)
	{
		delete [] triangleVertexNormals[i]; 
	}
	delete [] triangleVertexNormals; 
}

// uses lines to draw the mesh in wireframe mode
void drawSquareFaceWireframe(face3D face, vector3D v1, vector3D v2, vector3D v3, vector3D v4)
{
	glColor3f(wireframeColour.r, wireframeColour.g, wireframeColour.b);
	glBegin(GL_LINES);
		glNormal3f(v1.x, v1.y, v1.z);
		glVertex3f(face.v1.x, face.v1.y, face.v1.z);
		glNormal3f(v2.x, v2.y, v2.z);
		glVertex3f(face.v2.x, face.v2.y, face.v2.z);
	glEnd();
	glBegin(GL_LINES);
		glNormal3f(v2.x, v2.y, v2.z);
		glVertex3f(face.v2.x, face.v2.y, face.v2.z);
		glNormal3f(v3.x, v3.y, v3.z);
		glVertex3f(face.v3.x, face.v3.y, face.v3.z);

	glEnd();
	glBegin(GL_LINES);
		glNormal3f(v3.x, v3.y, v3.z);
		glVertex3f(face.v3.x, face.v3.y, face.v3.z);
		glNormal3f(v4.x, v4.y, v4.z);
		glVertex3f(face.v4.x, face.v4.y, face.v4.z);
	glEnd();
	glBegin(GL_LINES);
		glNormal3f(v4.x, v4.y, v4.z);
		glVertex3f(face.v4.x, face.v4.y, face.v4.z);
		glNormal3f(v1.x, v1.y, v1.z);
		glVertex3f(face.v1.x, face.v1.y, face.v1.z);
	glEnd();
}

// uses quads to draw the mesh in solid face mode, this uses colour based on greyscale heights
void drawSquareFaceSolid(face3D face, vector3D v1, vector3D v2, vector3D v3, vector3D v4, colour c1, colour c2, colour c3, colour c4)  
{

	glBegin(GL_QUADS);
		glColor3f(c1.r, c1.g, c1.b);
		glNormal3f(v1.x, v1.y, v1.z);
		glVertex3f(face.v1.x, face.v1.y, face.v1.z);
		glColor3f(c2.r, c2.g, c2.b);
		glNormal3f(v2.x, v2.y, v2.z);
		glVertex3f(face.v2.x, face.v2.y, face.v2.z);
		glColor3f(c3.r, c3.g, c3.b);
		glNormal3f(v3.x, v3.y, v3.z);
		glVertex3f(face.v3.x, face.v3.y, face.v3.z);
		glColor3f(c4.r, c4.g, c4.b);
		glNormal3f(v4.x, v4.y, v4.z);
		glVertex3f(face.v4.x, face.v4.y, face.v4.z);
	glEnd();
}

// uses lines to draw the mesh in wireframe mode
void drawTriangleFaceWireframe(face3D face, vector3D v1, vector3D v2, vector3D v3, vector3D v4)
{
	glColor3f(wireframeColour.r, wireframeColour.g, wireframeColour.b);
	glBegin(GL_LINES);
		glNormal3f(v1.x, v1.y, v1.z);
		glVertex3f(face.v1.x, face.v1.y, face.v1.z);
		glNormal3f(v2.x, v2.y, v2.z);
		glVertex3f(face.v2.x, face.v2.y, face.v2.z);
	glEnd();
	glBegin(GL_LINES);
		glNormal3f(v2.x, v2.y, v2.z);
		glVertex3f(face.v2.x, face.v2.y, face.v2.z);
		glNormal3f(v4.x, v4.y, v4.z);
		glVertex3f(face.v4.x, face.v4.y, face.v4.z);
	glEnd();
	glBegin(GL_LINES);
		glNormal3f(v4.x, v4.y, v4.z);
		glVertex3f(face.v4.x, face.v4.y, face.v4.z);
		glNormal3f(v1.x, v1.y, v1.z);
		glVertex3f(face.v1.x, face.v1.y, face.v1.z);
	glEnd();
	glBegin(GL_LINES);
		glNormal3f(v2.x, v2.y, v2.z);
		glVertex3f(face.v2.x, face.v2.y, face.v2.z);
		glNormal3f(v3.x, v3.y, v3.z);
		glVertex3f(face.v3.x, face.v3.y, face.v3.z);
	glEnd();
	glBegin(GL_LINES);
		glNormal3f(v3.x, v3.y, v3.z);
		glVertex3f(face.v3.x, face.v3.y, face.v3.z);
		glNormal3f(v4.x, v4.y, v4.z);
		glVertex3f(face.v4.x, face.v4.y, face.v4.z);
	glEnd();
}

// uses triangles to draw the mesh in solid face mode, this uses colour based on greyscale heights
void drawTriangleFaceSolid(face3D face, vector3D v1, vector3D v2, vector3D v3, vector3D v4, colour c1, colour c2, colour c3, colour c4)  
{
	glBegin(GL_TRIANGLES);
		glColor3f(c2.r, c2.g, c2.b);
		glNormal3f(v2.x, v2.y, v2.z);
		glVertex3f(face.v2.x, face.v2.y, face.v2.z);
		glColor3f(c4.r, c4.g, c4.b);
		glNormal3f(v4.x, v4.y, v4.z);
		glVertex3f(face.v4.x, face.v4.y, face.v4.z);
		glColor3f(c1.r, c1.g, c1.b);
		glNormal3f(v1.x, v1.y, v1.z);
		glVertex3f(face.v1.x, face.v1.y, face.v1.z);
	glEnd();
	glBegin(GL_TRIANGLES);
		glColor3f(c4.r, c4.g, c4.b);
		glNormal3f(v4.x, v4.y, v4.z);
		glVertex3f(face.v4.x, face.v4.y, face.v4.z);
		glColor3f(c2.r, c2.g, c2.b);
		glNormal3f(v2.x, v2.y, v2.z);
		glVertex3f(face.v2.x, face.v2.y, face.v2.z);
		glColor3f(c3.r, c3.g, c3.b);
		glNormal3f(v3.x, v3.y, v3.z);
		glVertex3f(face.v3.x, face.v3.y, face.v3.z);
	glEnd();
}

// iterates through every face of the mesh and draws it
void Mesh(void)
{
	for(int i = 0; i < gridsize - 1 ; i++ )
	{
		for(int j = 0; j < gridsize - 1 ; j++ )
		{
			face3D f;
			f.v1 = grid[i][j]; // define points for each face
			f.v2 = grid[i+1][j];
			f.v3 = grid[i+1][j+1];
			f.v4 = grid[i][j+1];
			vector3D v1 = squareVertexNormals[i][j]; // define normals for each face
			vector3D v2 = squareVertexNormals[i+1][j]; 
			vector3D v3 = squareVertexNormals[i+1][j+1]; 
			vector3D v4 = squareVertexNormals[i][j+1]; 
			vector3D v5 = triangleVertexNormals[i][j]; 
			vector3D v6 = triangleVertexNormals[i+1][j]; 
			vector3D v7 = triangleVertexNormals[i+1][j+1]; 
			vector3D v8 = triangleVertexNormals[i][j+1];
			colour c1 = {(grid[i][j].y - minHeight)/range, (grid[i][j].y - minHeight)/range, (grid[i][j].y - minHeight)/range}; // define colours for each face
			colour c2 = {(grid[i+1][j].y - minHeight)/range, (grid[i+1][j].y - minHeight)/range, (grid[i+1][j].y - minHeight)/range};
			colour c3 = {(grid[i+1][j+1].y - minHeight)/range, (grid[i+1][j+1].y - minHeight)/range, (grid[i+1][j+1].y - minHeight)/range};
			colour c4 = {(grid[i][j+1].y - minHeight)/range, (grid[i][j+1].y - minHeight)/range, (grid[i][j+1].y - minHeight)/range};
			if (mode == 's') // based on the mode and the primitive type, the correct draw function(s) is used
			{
				if (primitive == 'S')
				{
					drawSquareFaceSolid(f, v1, v2, v3, v4, c1, c2, c3, c4);  
				}
				else 
				{
					drawTriangleFaceSolid(f, v5, v6, v7, v8, c1, c2, c3, c4);  
				}
			}
			if (mode == 'w')
			{
				if (primitive == 'S')
				{
					drawSquareFaceWireframe(f, v1, v2, v3, v4);
				}
				else 
				{
					drawTriangleFaceWireframe(f, v5, v6, v7, v8);
				}
			}
			if (mode == 'b')
			{
				if (primitive == 'S')
				{
					drawSquareFaceSolid(f, v1, v2, v3, v4, c1, c2, c3, c4); 
					drawSquareFaceWireframe(f, v1, v2, v3, v4); 
				}
				else 
				{
					drawTriangleFaceSolid(f, v5, v6, v7, v8, c1, c2, c3, c4);  
					drawTriangleFaceWireframe(f, v5, v6, v7, v8);

				}
			}
		}
	}
}

// this function is used to draw the 2D greyscale map in the second window
void Greyscale(void)
{
	for( int i = 0; i < gridsize; i++ )
	{
		for( int j = 0; j < gridsize; j++ )
		{
			glBegin(GL_POLYGON); // draws a very tiny square (actually 1x1 pixels), which is the right greyscale colour, according to the height
			glColor3f((grid[i][j].y - minHeight)/range, (grid[i][j].y - minHeight)/range, (grid[i][j].y - minHeight)/range);
			glVertex2f(i, j);
			glVertex2f(i + 1, j);
			glVertex2f(i + 1, j + 1);
			glVertex2f(i, j + 1);
			glEnd();
		}
	}
}

// display function for window_1
void display(void)
{
	glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);
	glMatrixMode(GL_MODELVIEW);
	glLoadIdentity();
	gluLookAt(camPos[0], camPos[1], camPos[2], 0, 0, 0, 0, 1, 0); // set the camera
		glLightfv(GL_LIGHT0, GL_POSITION, light_pos); // lighting
		glLightfv(GL_LIGHT0, GL_AMBIENT, amb0);
		glLightfv(GL_LIGHT0, GL_DIFFUSE, diff0);
		glLightfv(GL_LIGHT0, GL_SPECULAR, spec0);
		glLightfv(GL_LIGHT1, GL_POSITION, light_pos1);
		glLightfv(GL_LIGHT1, GL_AMBIENT, amb1);
		glLightfv(GL_LIGHT1, GL_DIFFUSE, diff1);
		glLightfv(GL_LIGHT1, GL_SPECULAR, spec1);
		glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT, m_amb); // materials
		glMaterialfv(GL_FRONT_AND_BACK, GL_DIFFUSE, m_diff);
		glMaterialfv(GL_FRONT_AND_BACK, GL_SPECULAR, m_spec);
		glMaterialf(GL_FRONT_AND_BACK, GL_SHININESS, shiny);	
	glPushMatrix();
		glTranslatef(-(gridsize - 1)/2, 0, -(gridsize - 1)/2); // translate the mesh so that it is centered at the origin
		Mesh();
	glPopMatrix();
	glutSwapBuffers(); // double buffering
}
 // display function for the second window
void display_2(void)
{
	glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);
	Greyscale(); // draws 2D greyscale map
	glutSwapBuffers();
}

// callback which contains essential key bindings
void keyboard(unsigned char key, int x, int y)
{
	switch (key)
	{
		case 'q': // exit the program
		case 27:
			exit (0);
			break;

	}
	switch (key)
	{
		case 'r': // redraw a random grid of the current gridsize
			deallocateGrid();
			deallocateNormals();
			makeGrid(gridsize);
			giveGridHeight(grid);
			makeSquareVertexNormals(); 
			makeTriangleVertexNormals();
			break;
	}
	switch (key)
	{
		case 'w': // toggle viewing mode
			foo++;
			if ((foo % 3) == 0)
			{
				mode = 's';

			}
			else if ((foo % 3) == 1)
			{
				mode = 'w';
			}
			else if ((foo % 3) == 2)
			{
				mode = 'b';
			}
			break;
	}
	switch (key) // draw the mesh with triangles/squares
	{
		case 't':
			primitive = 'T';
			break;
	}
	switch (key)
	{
		case 'y':
			primitive = 'S';
			break;
	}
	switch (key)
	{
		case 's': // toggle shading
			bar++;
			if ((bar % 2) == 0)
			{
				shade = 'f';
				glShadeModel(GL_FLAT);

			}
			if ((bar % 2) == 1)
			{
				shade = 'o';
				glShadeModel(GL_SMOOTH);
			}
			break;
	}
	switch (key)
	{
		case 'l': // toggle lighting
			light++;
			if ((light % 2) == 0)
			{
				glDisable(GL_LIGHTING);
				glDisable(GL_LIGHT0);
				glDisable(GL_LIGHT1);
			}
			if ((light % 2) == 1)
			{
				glEnable(GL_LIGHTING);
				glEnable(GL_LIGHT0);
				glEnable(GL_LIGHT1);
			}
			break;
	}
	switch(key)
	{
		case 'i': // toggles which light you are moving with UHJK, default is light0
		{
			which_light++;
			break;
		}
	}
	switch(key)
	{
		case 'u': // controls location of lights
		{	
			if (which_light % 2 == 0)
			{
				light_pos[0] += gridsize/5;
				printf("The x and z coordinates of Light0 are (%.1f, %.1f)\n", light_pos[0], light_pos[2]);
			}
			if (which_light % 2 == 1)
			{
				light_pos1[0] += gridsize/5;
				printf("The x and z coordinates of Light1 are (%.1f, %.1f)\n", light_pos1[0], light_pos1[2]);
			}
			break;
		}
	}
	switch(key)
	{
		case 'j': // controls location of lights
		{
			if (which_light % 2 == 0)
			{
				light_pos[0] -= gridsize/5;
				printf("The x and z coordinates of Light0 are (%.1f, %.1f)\n", light_pos[0], light_pos[2]);
			}
			if (which_light % 2 == 1)
			{
				light_pos1[0] -= gridsize/5;
				printf("The x and z coordinates of Light1 are (%.1f, %.1f)\n", light_pos1[0], light_pos1[2]);
			}
			break;
		}
	}
	switch(key)
	{
		case 'h': // controls location of lights
		{
			if (which_light % 2 == 0)
			{
				light_pos[2] -= gridsize/5;
				printf("The x and z coordinates of Light0 are (%.1f, %.1f)\n", light_pos[0], light_pos[2]);
			}
			if (which_light % 2 == 1)
			{
				light_pos1[2] -= gridsize/5;
				printf("The x and z coordinates of Light1 are (%.1f, %.1f)\n", light_pos1[0], light_pos1[2]);
			}
			break;
		}
	}
	switch(key)
	{
		case 'k': // controls location of lights
		{
			if (which_light % 2 == 0)
			{
				light_pos[2] += gridsize/5;
				printf("The x and z coordinates of Light0 are (%.1f, %.1f)\n", light_pos[0], light_pos[2]);
			}
			if (which_light % 2 == 1)
			{
				light_pos1[2] += gridsize/5;
				printf("The x and z coordinates of Light1 are (%.1f, %.1f)\n", light_pos1[0], light_pos1[2]);
			}
			break;
		}
	}
	switch(key)
	{
		case 'm': // resets the position of the lights
		{
			light_pos[0] = 2*gridsize;
			light_pos[1] = 2*gridsize;
			light_pos[2] = -2*gridsize;
			light_pos1[0] = -2*gridsize;
			light_pos1[1] = 2*gridsize;
			light_pos1[2] = 2*gridsize;
			break;
		}
	}

	deallocateNormals();
	makeSquareVertexNormals(); 
	makeTriangleVertexNormals();
	glutSetWindow(window_1);
	glutPostRedisplay();
	glutSetWindow(window_2);
	glutPostRedisplay();	
}

// contains key bindings for special (arrow) keys
void special(int key, int x, int y)
{
	switch(key)
	{
		case GLUT_KEY_RIGHT: // uses a custom transformation matrix to rotate the camera coordinates 5 degrees around the y-axis
			float temp1 = 0.996*camPos[0] + 0.087*camPos[2]; 
			float temp2 = -0.087*camPos[0] + 0.996*camPos[2];
			camPos[0] = temp1;
			camPos[2] = temp2;
			break;
	}
	switch(key)
	{
		case GLUT_KEY_LEFT: // other direction
			float temp3 = 0.996*camPos[0] - 0.087*camPos[2];
			float temp4 = 0.087*camPos[0] + 0.996*camPos[2];
			camPos[0] = temp3;
			camPos[2] = temp4;
			break;
	}
	switch(key)
	{
		case GLUT_KEY_UP: // same, but for x-axis
		if (camPos[1] > 0 ||camPos[2] > -1.2*gridsize)
		{
			float temp1 = 0.996*camPos[1] + 0.087*camPos[2];
			float temp2 = -0.087*camPos[1] + 0.996*camPos[2];
			camPos[1] = temp1;
			camPos[2] = temp2;

		}
			break;
	}
	switch(key)
	{
		case GLUT_KEY_DOWN: // other direction
		if (camPos[1] > 0 || camPos[2] < 1.2*gridsize)
		{
			float temp3 = 0.996*camPos[1] - 0.087*camPos[2];
			float temp4 = 0.087*camPos[1] + 0.996*camPos[2];
			camPos[1] = temp3;
			camPos[2] = temp4;
			break;
		}
	}
	glutPostRedisplay();
}


void init(void)
{
	glClearColor(0, 0, 0, 0);
	glMatrixMode(GL_PROJECTION);
	glLoadIdentity();
	gluPerspective(45, 1, 1, 1000); // perspective projection makes the most sense for viewing the mesh
	makeGrid(gridsize);
	giveGridHeight(grid);
	makeSquareVertexNormals(); 
	makeTriangleVertexNormals();
	glShadeModel(GL_FLAT); // default shading is flat
	glEnable(GL_CULL_FACE);
	glCullFace(GL_BACK); // enable backface culling
}

void init_2(void)
{
	glClearColor(0, 0, 0, 0);
	glMatrixMode(GL_PROJECTION);
	glLoadIdentity();
	gluOrtho2D(0, 300, 0, 300); // orthographic projection makes the most sense for viewing the 2D greyscale region
}

// mouse callback used for the 2D greyscale window
void mouse(int btn, int state, int x, int y)
{
	if ((x > gridsize | ((299 - y) > gridsize)))
	{
		printf("Please reselect a point that is actually on the terrain\n");
	}
	else
	{
		if (btn == GLUT_LEFT_BUTTON){

			if (state == GLUT_DOWN){
				maxHeight = 1;
				minHeight = 1;
				for( int i = 0; i < gridsize; i++ ) // reads the mouse coordinates from the second window and creates a new "cirlce" at the correct location
				{
					for( int j = 0; j < gridsize; j++ )
					{
						float pd = vertexPlaneDistance(grid[i][j], grid[x][299 - y]); 
						if( abs(pd) <= radius )
						{
							grid[i][j].y += height/2 + height/2*cos(pd*3.14159/radius);	
						}
						if (grid[i][j].y > maxHeight)
						{
							maxHeight = grid[i][j].y;
						}
						if (grid[i][j].y < minHeight)
						{
							minHeight = grid[i][j].y;
						}
					}
				}
				range = maxHeight - minHeight;
			}
		}
		if (btn == GLUT_RIGHT_BUTTON)
		{
			if (state == GLUT_DOWN)
			{
				maxHeight = 1;
				minHeight = 1;
				for( int i = 0; i < gridsize; i++ ) // same as above but decrements the height on right click
				{
					for( int j = 0; j < gridsize; j++ )
					{
						float pd = vertexPlaneDistance(grid[i][j], grid[x][299 - y]);
						if( abs(pd) <= radius )
						{
							grid[i][j].y -= height/2 + height/2*cos(pd*3.14159/radius);	
						}		
						if (grid[i][j].y > maxHeight)
						{
							maxHeight = grid[i][j].y;
						}
						if (grid[i][j].y < minHeight)
						{
							minHeight = grid[i][j].y;
						}
					}
				}
				range = maxHeight - minHeight;
			}
		}
	}
	deallocateNormals();
	makeSquareVertexNormals(); 
	makeTriangleVertexNormals();
	glutSetWindow(window_1);
	glutPostRedisplay();
	glutSetWindow(window_2);
	glutPostRedisplay();
}

// call back function for initiating the menu, just redraws the mesh with chosen gridsize
void menuProc(int value)
{
	deallocateGrid();
	deallocateNormals();
	if(value == 1)
	{
		gridsize = 50;
	}
	if(value == 2)
	{
		gridsize = 100;
	}
	if(value == 3)
	{
		gridsize = 200;
	}
	if(value == 4)
	{
		gridsize = 300;
	}
	camPos[0] = -1.2*gridsize; // reset cam position
	camPos[1] = 1.2*gridsize, 
	camPos[2] = -1.2*gridsize;
	light_pos[0] = 2*gridsize; // reset the light position
	light_pos[1] = 2*gridsize;
	light_pos[2] = -2*gridsize;
	light_pos1[0] = -2*gridsize;
	light_pos1[1] = 2*gridsize;
	light_pos1[2] = 2*gridsize;
	makeGrid(gridsize);
	giveGridHeight(grid);
	makeSquareVertexNormals(); 
	makeTriangleVertexNormals();
	glutSetWindow(window_1);
	glutPostRedisplay();
	glutSetWindow(window_2);
	glutPostRedisplay();		
}

// main, program entry point, initialize glut, create menus and windows, call backs
int main(int argc, char** argv)
{
	glutInit(&argc, argv);
	glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH);
	glutInitWindowSize(1000, 800);
	glutInitWindowPosition(900,100);	
    window_1 = glutCreateWindow(argv[0]);
    glutSetWindowTitle("Terrain");
    menu = glutCreateMenu(menuProc);
	glutAddMenuEntry("50 X 50 Grid", 1);
	glutAddMenuEntry("100 X 100 Grid", 2);
	glutAddMenuEntry("200 X 200 Grid", 3);
	glutAddMenuEntry("300 X 300 Grid", 4);
	glutAttachMenu(GLUT_RIGHT_BUTTON);
	init();
	glutDisplayFunc(display);
	glutKeyboardFunc(keyboard);
	glutSpecialFunc(special);

	glutInitWindowSize(300, 300);
	glutInitWindowPosition(500, 500);
    window_2 = glutCreateWindow(argv[0]);
	glutSetWindowTitle("Greyscale");
	init_2();
	glutDisplayFunc(display_2);	
	glutMouseFunc(mouse);

	glEnable(GL_DEPTH_TEST);


	glutMainLoop();


	return(0);
}
/*
Title: mandelbrot.cu
Author: Justin Staples
Date: May 12, 2018
Usage: 
	nvcc mandelbrot.cu -lGL -lGLU -lglut -o prog
	./prog
*/

#include <stdio.h>
#include <GL/gl.h> // OpenGL as well as utilities
#include <GL/glu.h>
#include <GL/glut.h>
#include <thrust/complex.h> // for complex numbers in CUDA

using namespace thrust;

typedef struct {float real; float imag;} point; // complex numbers

int MAX_ITER = 255; 
int W = 1024; // image dimensions
int H = 512;
int aspect_ratio = W / H;
int block_dim_x = 4; // 4 * 4 = 16 threads per block
int block_dim_y = 4;
dim3 block(block_dim_x, block_dim_y); // block and grid dimsions
dim3 grid(W / block_dim_x, H / block_dim_y);
float height = 1;
float width = height * aspect_ratio;
float scale = 1;
point center;
point bottom_left;

int * d_out;
int * h_out;
const int ARRAY_SIZE = W * H;
const int ARRAY_BYTES = ARRAY_SIZE * sizeof(int);

__device__ int assignColour(int i) {
	int val = 0;
	val += powf(i, 2); // blue
	val = val << 8; // each integer is 4 bytes but each colour component is only 1, so shift them to the correct positions (RGBA)
	val += powf(i, 2); // green
	val = val << 8;
	val += powf(i, 2); // red

	return val;
}

__device__ int iterations(complex<float> C, int max) {
	complex<float> z0(0, 0); //  mandelbrot set defined for z0 = 0 + 0i
	complex<float> zn; // populated during iteration

	int iter = 0;
	float mag = 0;	
	while (mag < 2 && iter < max) { // ensure the magnitude is bounded by 2
		mag = abs(z0);
		zn = z0 * z0 + C;
		z0 = zn;
		iter++;
	}
	return iter;
}

__global__ void process(int * d_out, point p, float w, float h, float s, int max){
	// map block and grid coordinates to pixel coordinates
	int y_idx = 4 * blockIdx.y + threadIdx.y;
	int x_idx = 4 * blockIdx.x + threadIdx.x;
	int idx = 1024 * y_idx + x_idx;

	// map pixel coordinates to real and imaginary components
	float R = p.real + (x_idx / 1023.0) * w;
	float I = p.imag + (y_idx / 511.0) * h;

	// determine number of iterations for each complex point, bounded the maximum number of iterations
	complex<float> C(R, I); // each thread is responsible for 1 complex point P
	int iter = iterations(C, max);
	
	// use number of iterations to assign colours to each point
	int val = assignColour(iter);

	// write the value to the device output
	d_out[idx] = val;
}

void display() {
    glClearColor(0, 0, 0, 1);
    glClear(GL_COLOR_BUFFER_BIT);

	process<<<grid, block>>>(d_out, bottom_left, width, height, scale, MAX_ITER);

	cudaMemcpy(h_out, d_out, ARRAY_BYTES, cudaMemcpyDeviceToHost);

    glDrawPixels(W, H, GL_RGBA, GL_UNSIGNED_BYTE, h_out);

    glutSwapBuffers();
    glutPostRedisplay();
}

void keyboard(unsigned char key, int x, int y) {
	switch (key) {
		case 'w':
			scale *= 1.07;
			height /= 1.07;
			width /= 1.07;
			bottom_left.real = center.real - width / 2.0;
			bottom_left.imag = center.imag - height / 2.0;
			break;
		case 's':
			scale /= 1.07;
			height *= 1.07;
			width *= 1.07;
			bottom_left.real = center.real - width / 2.0;
			bottom_left.imag = center.imag - height / 2.0;
			break;
	}
}

void special(int key, int x, int y) {
	switch (key) {
		case GLUT_KEY_RIGHT:
			center.real += width / 100;
			bottom_left.real += width / 100;
			break;
		case GLUT_KEY_LEFT:
			center.real -= width / 100;
			bottom_left.real -= width /100;
			break;
		case GLUT_KEY_UP:
			center.imag += width / 100;
			bottom_left.imag += width / 100;
			break;
		case GLUT_KEY_DOWN:
			center.imag -= width / 100;
			bottom_left.imag -= width / 100;
			break;
	}
	glutSwapBuffers();
}

int main(int argc, char **argv)	{
	// initialize globals
	height = 2;
	width = 4;
	center.real = 0.0;
	center.imag = 0.0;
	bottom_left.real = center.real - width / 2.0;
	bottom_left.imag = center.imag - height / 2.0;

	// allocate memory on the CPU for host data and on the GPU for device data
	h_out = (int *) malloc(ARRAY_BYTES);
	cudaMalloc((void **) &d_out, ARRAY_BYTES);

	// initialize GLUT and start the main program
    glutInit(&argc, argv);
    glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE);
    glutInitWindowSize(W, H);
    glutCreateWindow("Mandelbrot");
    glutDisplayFunc(display);
    glutKeyboardFunc(keyboard);
    glutSpecialFunc(special);
    glutMainLoop();

    return 0;
}
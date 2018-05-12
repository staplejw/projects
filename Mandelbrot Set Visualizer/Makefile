all: mandelbrot clean

mandelbrot:
	nvcc mandelbrot.cu -lGL -lGLU -lglut -o mandelbrot
	./mandelbrot

clean:
	rm mandelbrot
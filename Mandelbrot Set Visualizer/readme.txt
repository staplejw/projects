This program is a mandelbrot visualizer. It uses CUDA, which is a C/C++ 
programming extension created by Nvidia. This allows users to get greatly
improved performance by running serial computations in parallel on the GPU. 
It also uses OpenGL for drawing the results to the screen.

The program works by keeping track of a viewport, which determines which rectangular area 
of the complex plane can be viewed. The arrow keys can be used to translate 
the viewport horizontally or vertically. The 'w' and 's' keys can be used to 
change the viewport so as to zoom in or zoom out, respectively. 

Each pixel is assigned a complex point, and then a colour, which is determined 
by how quickly the point converges or diverges. Many interesting colour schemes 
can be discoverd by tweaking the way that iterations are mapped to colours.  

The process of computing the number of iterations for a given pixel is a serial 
one. However, the result for each pixel is entirely independent of the surrounding
pixels. So, I use the power of my GPU to spawn one thread for each pixel (512 x 1024)
and allow them to run in parallel. 

FUTURE WORK:

1) The program currently uses single precision (float) floating point numbers. This 
limits the nature of the program. The mandelbrot set is a fractal shape with truly 
infinite detail. My goal is to extend the program so that it can use arbitrary 
precision floating point numbers. That way, no matter how far the user zooms, the 
program will always be able to render more detail. In its current state, you can 
only zoom so far down before you can see the limits of the single precision numbers.

2) I would also like to enhance the user interaction by adding an interface that lets
the user play around with and customize their own colour scheme. This is one area that
I have not experimented enough with. There are many interesting colour mappings to be 
discovered. I would like to extend the program that the user can have a greater control 
over what colours they see.
LDFLAGS = -lGL -lGLU -lglut
CFLAGS=-g -Wall -std=c++11
CC=g++
EXEEXT=
RM=rm


ifeq "$(OS)" "Windows_NT"
	EXEEXT=.exe 
	RM=del 
    LDFLAGS = -lfreeglut -lglu32 -lopengl32
else
	OS := $(shell uname)
	ifeq ($(OS), Darwin)
	        LDFLAGS = -framework Carbon -framework OpenGL -framework GLUT
	endif
endif

PROGRAM_NAME= Terrain.x


run: $(PROGRAM_NAME)
	./$(PROGRAM_NAME)$(EXEEXT)

$(PROGRAM_NAME): Terrain.o 
	$(CC) -o $@ $^ $(CFLAGS) $(LDFLAGS)

clean:
	$(RM) *.o $(PROGRAM_NAME)$(EXEEXT)
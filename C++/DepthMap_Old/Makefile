CC =  "g++"

PROJECT =  DepthMap
SRC = depthmap.cpp

LIBS = `pkg-config opencv4 --cflags --libs`

$(PROJECT) : $(SRC)
	$(CC) $(SRC) -o $(PROJECT) $(LIBS) 
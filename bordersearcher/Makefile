CC = g++
CFLAGS = -O2 -Wall -std=c++11


play_icfp2015: main.o system.o
	g++ main.o system.o -o bordersearcher

.cpp.o:
	$(CC) $(CFLAGS) -o $@ -c $<

clean:
	rm -rf *.o

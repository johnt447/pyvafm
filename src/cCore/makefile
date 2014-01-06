CC	= gcc
CFLAGS	= -c -w -std=c99 -fpic -O3
LFLAGS	= -w -lm -shared -fpic -O3 -o vafmcore.so


CIRCUITS = core_container.o core_signals.o core_output.o core_maths.o #core_logic.o  core_filters.o

all: container siggen outputs maths main.o  # filters  logics
	$(CC) $(LFLAGS) main.o $(CIRCUITS)
	rm *.o
	cp vafmcore.so ../.
	cp vafmcore.so ../../examples/.
main.o:
	$(CC) $(CFLAGS) main.c
outputs:
	$(CC) $(CFLAGS) core_output.c
maths: 
	$(CC) $(CFLAGS) core_maths.c
logics: 
	$(CC) $(CFLAGS) core_logic.c
siggen: 
	$(CC) $(CFLAGS) core_signals.c
filters: 
	$(CC) $(CFLAGS) core_filters.c
container: 
	$(CC) $(CFLAGS) core_container.c
clean:
	rm -rf *.o vafmcore.so

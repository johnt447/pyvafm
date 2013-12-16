CC	= gcc
CFLAGS	= -c -w -std=c99 -fpic -O3
LFLAGS	= -w -lm -shared -fpic -O3 -o vafmcore.so


CIRCUITS = core_maths.o core_logic.o core_signals.o core_output.o core_filters.o

all: core_filters.o output.o siggen maths.o logic.o main.o
	$(CC) $(LFLAGS) main.o $(CIRCUITS)
	rm *.o
main.o:
	$(CC) $(CFLAGS) main.c
output.o:
	$(CC) $(CFLAGS) core_output.c
maths.o: core_maths.c
	$(CC) $(CFLAGS) core_maths.c
logic.o: core_logic.c
	$(CC) $(CFLAGS) core_logic.c
siggen: core_signals.c
	$(CC) $(CFLAGS) core_signals.c
filters: core_filters.c
	$(CC) $(CFLAGS) core_filters.c
clean:
	rm -rf *.o vafmcore.so

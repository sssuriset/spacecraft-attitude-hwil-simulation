CC = gcc
CFLAGS = -Wall -Wextra -O2

UNAME_S := $(shell uname -s)

ifeq ($(UNAME_S),Darwin)
    SHARED_FLAGS = -dynamiclib
    SCHED_LIB = flight_software/libsched.dylib
else
    SHARED_FLAGS = -shared
    SCHED_LIB = flight_software/libsched.so
endif

FLIGHT_DIR = flight_software

CTRL_SRC = $(FLIGHT_DIR)/main.c $(FLIGHT_DIR)/attitude_controller.c
SCHED_TEST_SRC = $(FLIGHT_DIR)/scheduler_test.c $(FLIGHT_DIR)/scheduler.c

CTRL_BIN = $(FLIGHT_DIR)/ctrl
SCHED_BIN = $(FLIGHT_DIR)/sched_test

all: ctrl sched sched-lib

ctrl:
	$(CC) $(CFLAGS) $(CTRL_SRC) -o $(CTRL_BIN)

sched:
	$(CC) $(CFLAGS) $(SCHED_TEST_SRC) -o $(SCHED_BIN)

sched-lib:
	$(CC) $(CFLAGS) -fPIC $(SHARED_FLAGS) $(FLIGHT_DIR)/scheduler.c -o $(SCHED_LIB)

run: all
	python3 simulation/run_hwil.py

plots:
	python3 simulation/plot.py

baseline:
	python3 simulation/baseline.py

test-ctrl: ctrl
	./$(CTRL_BIN) 0.0 0.3 -0.2 0.15 0.02 -0.01 0.015

test-sched: sched
	./$(SCHED_BIN)

clean:
	rm -f $(CTRL_BIN)
	rm -f $(SCHED_BIN)
	rm -f $(FLIGHT_DIR)/libsched.dylib
	rm -f $(FLIGHT_DIR)/libsched.so
	rm -f *.o

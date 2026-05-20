CC = gcc
CFLAGS = -Wall -Wextra -O2

FLIGHT_DIR = flight_software

CONTROLLER_SRC = $(FLIGHT_DIR)/main.c $(FLIGHT_DIR)/attitude_controller.c
SCHEDULER_SRC = $(FLIGHT_DIR)/scheduler_test.c $(FLIGHT_DIR)/scheduler.c

CONTROLLER_BIN = $(FLIGHT_DIR)/controller_test
SCHEDULER_BIN = $(FLIGHT_DIR)/scheduler_test

all: controller scheduler

controller:
	$(CC) $(CFLAGS) $(CONTROLLER_SRC) -o $(CONTROLLER_BIN)

scheduler:
	$(CC) $(CFLAGS) $(SCHEDULER_SRC) -o $(SCHEDULER_BIN)

run: controller
	python3 simulation/hwil_simulation.py

plots:
	python3 simulation/plot_results.py

test-controller: controller
	./$(CONTROLLER_BIN) 0.0 0.3 -0.2 0.15 0.02 -0.01 0.015

test-scheduler: scheduler
	./$(SCHEDULER_BIN)

clean:
	rm -f $(CONTROLLER_BIN)
	rm -f $(SCHEDULER_BIN)
	rm -f *.o

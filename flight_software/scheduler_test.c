#include <stdio.h>
#include "scheduler.h"

int main(void)
{
    Scheduler scheduler;
    scheduler_init(&scheduler);

    double dt = 0.01;
    double total_time_s = 2.0;

    int sensor_count = 0;
    int control_count = 0;
    int telemetry_count = 0;
    int health_count = 0;

    for (int i = 0; i <= total_time_s / dt; i++) {
        double time_s = i * dt;

        if (sensor_task_due(&scheduler, time_s)) {
            sensor_count++;
        }

        if (control_task_due(&scheduler, time_s)) {
            control_count++;
        }

        if (telemetry_task_due(&scheduler, time_s)) {
            telemetry_count++;
        }

        if (health_task_due(&scheduler, time_s)) {
            health_count++;
        }
    }

    printf("C scheduler test complete\n");
    printf("Simulation time: %.2f s\n", total_time_s);
    printf("Sensor task executions: %d\n", sensor_count);
    printf("Control task executions: %d\n", control_count);
    printf("Telemetry task executions: %d\n", telemetry_count);
    printf("Health task executions: %d\n", health_count);

    return 0;
}
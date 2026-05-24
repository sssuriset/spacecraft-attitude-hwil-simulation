#include <stdio.h>

#include "scheduler.h"

int main(void)
{
    Scheduler scheduler;
    scheduler_init(&scheduler);

    const double dt = 0.01;
    const double total_time_s = 2.0;

    int sensor_count = 0;
    int control_count = 0;
    int telemetry_count = 0;
    int health_count = 0;

    for (int i = 0; i <= total_time_s / dt; i++) {
        double time_s = i * dt;

        if (due_sensor(&scheduler, time_s)) {
            sensor_count++;
        }

        if (due_control(&scheduler, time_s)) {
            control_count++;
        }

        if (due_telemetry(&scheduler, time_s)) {
            telemetry_count++;
        }

        if (due_health(&scheduler, time_s)) {
            health_count++;
        }
    }

    printf("C scheduler test complete\n");
    printf("Simulation time: %.2f s\n", total_time_s);
    printf("Sensor executions: %d\n", sensor_count);
    printf("Control executions: %d\n", control_count);
    printf("Telemetry executions: %d\n", telemetry_count);
    printf("Health executions: %d\n", health_count);

    return 0;
}

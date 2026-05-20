#include "scheduler.h"

void scheduler_init(Scheduler *scheduler)
{
    scheduler->sensor_period_s = 0.01;
    scheduler->control_period_s = 0.02;
    scheduler->telemetry_period_s = 0.10;
    scheduler->health_period_s = 1.00;

    scheduler->next_sensor_time_s = 0.0;
    scheduler->next_control_time_s = 0.0;
    scheduler->next_telemetry_time_s = 0.0;
    scheduler->next_health_time_s = 0.0;
}

int sensor_task_due(Scheduler *scheduler, double time_s)
{
    if (time_s >= scheduler->next_sensor_time_s) {
        scheduler->next_sensor_time_s += scheduler->sensor_period_s;
        return 1;
    }

    return 0;
}

int control_task_due(Scheduler *scheduler, double time_s)
{
    if (time_s >= scheduler->next_control_time_s) {
        scheduler->next_control_time_s += scheduler->control_period_s;
        return 1;
    }

    return 0;
}

int telemetry_task_due(Scheduler *scheduler, double time_s)
{
    if (time_s >= scheduler->next_telemetry_time_s) {
        scheduler->next_telemetry_time_s += scheduler->telemetry_period_s;
        return 1;
    }

    return 0;
}

int health_task_due(Scheduler *scheduler, double time_s)
{
    if (time_s >= scheduler->next_health_time_s) {
        scheduler->next_health_time_s += scheduler->health_period_s;
        return 1;
    }

    return 0;
}
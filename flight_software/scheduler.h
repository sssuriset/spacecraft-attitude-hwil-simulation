#ifndef SCHEDULER_H
#define SCHEDULER_H

typedef struct {
    double sensor_period_s;
    double control_period_s;
    double telemetry_period_s;
    double health_period_s;

    double next_sensor_time_s;
    double next_control_time_s;
    double next_telemetry_time_s;
    double next_health_time_s;
} Scheduler;

void scheduler_init(Scheduler *scheduler);

int sensor_task_due(Scheduler *scheduler, double time_s);
int control_task_due(Scheduler *scheduler, double time_s);
int telemetry_task_due(Scheduler *scheduler, double time_s);
int health_task_due(Scheduler *scheduler, double time_s);

#endif
#ifndef SCHEDULER_H
#define SCHEDULER_H

typedef struct {
    double sensor_dt;
    double ctrl_dt;
    double telem_dt;
    double health_dt;

    double next_sensor;
    double next_ctrl;
    double next_telem;
    double next_health;
} Scheduler;

void scheduler_init(Scheduler *s);

int due_sensor(Scheduler *s, double t);
int due_control(Scheduler *s, double t);
int due_telemetry(Scheduler *s, double t);
int due_health(Scheduler *s, double t);

#endif

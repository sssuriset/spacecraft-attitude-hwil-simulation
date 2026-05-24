#include "scheduler.h"

static int due(double t, double dt, double *next)
{
    if (t + 1.0e-12 < *next) {
        return 0;
    }

    /*
       If the loop falls behind, missed task releases are skipped instead of
       replayed. The simulation records one task execution at the current step.
    */
    while (t + 1.0e-12 >= *next) {
        *next += dt;
    }

    return 1;
}

void scheduler_init(Scheduler *s)
{
    s->sensor_dt = 0.01;
    s->ctrl_dt = 0.02;
    s->telem_dt = 0.10;
    s->health_dt = 1.00;

    s->next_sensor = 0.0;
    s->next_ctrl = 0.0;
    s->next_telem = 0.0;
    s->next_health = 0.0;
}

int due_sensor(Scheduler *s, double t)
{
    return due(t, s->sensor_dt, &s->next_sensor);
}

int due_control(Scheduler *s, double t)
{
    return due(t, s->ctrl_dt, &s->next_ctrl);
}

int due_telemetry(Scheduler *s, double t)
{
    return due(t, s->telem_dt, &s->next_telem);
}

int due_health(Scheduler *s, double t)
{
    return due(t, s->health_dt, &s->next_health);
}

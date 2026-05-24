#ifndef ATTITUDE_CONTROLLER_H
#define ATTITUDE_CONTROLLER_H

#define CTRL_KP 0.8
#define CTRL_KD 2.0

typedef struct {
    double time_s;
    double theta_rad[3];
    double omega_rad_s[3];
} SensorPacket;

typedef struct {
    double torque_Nm[3];
} ActuatorCommand;

void pd_step(SensorPacket sensor, ActuatorCommand *command);

#endif

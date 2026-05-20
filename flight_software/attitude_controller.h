#ifndef ATTITUDE_CONTROLLER_H
#define ATTITUDE_CONTROLLER_H

typedef struct {
    double time_s;
    double theta_rad[3];
    double omega_rad_s[3];
} SensorPacket;

typedef struct {
    double torque_Nm[3];
} ActuatorCommand;

void compute_control_command(SensorPacket sensor, ActuatorCommand *command);

#endif
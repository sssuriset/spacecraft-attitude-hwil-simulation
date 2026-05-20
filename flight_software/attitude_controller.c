#include "attitude_controller.h"

void compute_control_command(SensorPacket sensor, ActuatorCommand *command)
{
    double kp = 0.8;
    double kd = 2.0;

    for (int i = 0; i < 3; i++) {
        command->torque_Nm[i] = -kp * sensor.theta_rad[i] - kd * sensor.omega_rad_s[i];
    }
}
#include "attitude_controller.h"

void pd_step(SensorPacket sensor, ActuatorCommand *command)
{
    for (int i = 0; i < 3; i++) {
        command->torque_Nm[i] =
            -CTRL_KP * sensor.theta_rad[i] - CTRL_KD * sensor.omega_rad_s[i];
    }
}

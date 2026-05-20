#include <stdio.h>
#include <stdlib.h>
#include "attitude_controller.h"

int main(int argc, char *argv[])
{
    if (argc != 8) {
        printf("Usage: controller_test time_s theta_x theta_y theta_z omega_x omega_y omega_z\n");
        return 1;
    }

    SensorPacket sensor;
    ActuatorCommand command;

    sensor.time_s = atof(argv[1]);

    sensor.theta_rad[0] = atof(argv[2]);
    sensor.theta_rad[1] = atof(argv[3]);
    sensor.theta_rad[2] = atof(argv[4]);

    sensor.omega_rad_s[0] = atof(argv[5]);
    sensor.omega_rad_s[1] = atof(argv[6]);
    sensor.omega_rad_s[2] = atof(argv[7]);

    compute_control_command(sensor, &command);

    printf("%.10f %.10f %.10f\n",
           command.torque_Nm[0],
           command.torque_Nm[1],
           command.torque_Nm[2]);

    return 0;
}
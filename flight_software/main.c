#include <errno.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include "attitude_controller.h"

static int parse_double(const char *text, double *value)
{
    char *end = NULL;
    errno = 0;

    *value = strtod(text, &end);

    if (text == end || errno != 0) {
        return 0;
    }

    while (*end == ' ' || *end == '\t' || *end == '\n') {
        end++;
    }

    return *end == '\0';
}

static int fill_packet(char **values, SensorPacket *sensor)
{
    double parsed[7];

    for (int i = 0; i < 7; i++) {
        if (!parse_double(values[i], &parsed[i])) {
            return 0;
        }
    }

    sensor->time_s = parsed[0];

    for (int i = 0; i < 3; i++) {
        sensor->theta_rad[i] = parsed[i + 1];
        sensor->omega_rad_s[i] = parsed[i + 4];
    }

    return 1;
}

static void print_command(SensorPacket sensor)
{
    ActuatorCommand command;

    pd_step(sensor, &command);

    printf("%.10f %.10f %.10f\n",
           command.torque_Nm[0],
           command.torque_Nm[1],
           command.torque_Nm[2]);
    fflush(stdout);
}

static int run_once(int argc, char *argv[])
{
    SensorPacket sensor;

    if (argc != 8) {
        fprintf(stderr,
                "Usage: controller_test time_s theta_x theta_y theta_z omega_x omega_y omega_z\n");
        return 1;
    }

    if (!fill_packet(&argv[1], &sensor)) {
        fprintf(stderr, "Invalid numeric input.\n");
        return 1;
    }

    print_command(sensor);
    return 0;
}

static int run_stream(void)
{
    char line[512];

    while (fgets(line, sizeof(line), stdin) != NULL) {
        char *values[7];
        char *token = strtok(line, " \t\n");
        int count = 0;

        while (token != NULL && count < 7) {
            values[count++] = token;
            token = strtok(NULL, " \t\n");
        }

        if (count != 7 || token != NULL) {
            fprintf(stderr, "Expected 7 numeric fields per controller packet.\n");
            return 1;
        }

        SensorPacket sensor;

        if (!fill_packet(values, &sensor)) {
            fprintf(stderr, "Invalid numeric input.\n");
            return 1;
        }

        print_command(sensor);
    }

    return 0;
}

int main(int argc, char *argv[])
{
    if (argc == 1) {
        return run_stream();
    }

    return run_once(argc, argv);
}

// La ruta simulada del robot, sin ROS: la misma que route.py.
#pragma once

#include <cmath>

namespace proyecto_dominio_cpp {

struct RoutePose {
  double x_m;
  double yaw_rad;
};

// Ida y vuelta por una recta de length_m: a la ida avanza por +x con yaw 0;
// a la vuelta retrocede hacia el origen con yaw pi.
inline RoutePose route_pose(double distance_m, double length_m) {
  const double lap = std::fmod(distance_m, 2.0 * length_m);
  if (lap < length_m) {
    return RoutePose{lap, 0.0};
  }
  return RoutePose{2.0 * length_m - lap, M_PI};
}

}  // namespace proyecto_dominio_cpp

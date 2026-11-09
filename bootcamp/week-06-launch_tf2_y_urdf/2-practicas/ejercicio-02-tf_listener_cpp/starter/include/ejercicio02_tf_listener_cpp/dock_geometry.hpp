// Ejercicio 02, Semana 06 — dónde está el dock visto desde el robot, sin ROS.
#pragma once

#include "geometry_msgs/msg/transform.hpp"

namespace ejercicio02_tf_listener_cpp {

struct DockReading {
  double distance_m;   // distancia en el suelo (plano xy), en metros
  double bearing_rad;  // 0 = delante, positivo = a la izquierda (REP 103)
};

// base_to_dock: la transformación que devuelve
// lookupTransform("base_link", "dock", ...): la posición del dock expresada
// en el marco del robot.
DockReading dock_reading(const geometry_msgs::msg::Transform& base_to_dock);

}  // namespace ejercicio02_tf_listener_cpp

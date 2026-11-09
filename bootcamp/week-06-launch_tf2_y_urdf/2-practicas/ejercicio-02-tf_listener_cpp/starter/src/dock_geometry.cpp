#include "ejercicio02_tf_listener_cpp/dock_geometry.hpp"

#include <cmath>

namespace ejercicio02_tf_listener_cpp {

DockReading dock_reading(const geometry_msgs::msg::Transform& base_to_dock) {
  // ============================================
  // PASO 1: distancia y rumbo desde base_link
  // ============================================
  // La traslación ya está en el marco del robot: x hacia delante, y hacia la
  // izquierda. La distancia es la hipotenusa; el rumbo, el ángulo de ese
  // vector respecto al eje x. La rotación del dock no importa aquí.
  // Descomenta las siguientes líneas para el Paso 1:
  //
  // const double x = base_to_dock.translation.x;
  // const double y = base_to_dock.translation.y;
  // return DockReading{std::hypot(x, y), std::atan2(y, x)};
  static_cast<void>(base_to_dock);  // elimina en el Paso 1
  return DockReading{0.0, 0.0};     // elimina en el Paso 1
}

}  // namespace ejercicio02_tf_listener_cpp

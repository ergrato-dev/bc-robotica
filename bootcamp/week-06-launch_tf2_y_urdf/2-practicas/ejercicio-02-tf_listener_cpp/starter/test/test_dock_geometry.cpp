// Paso 1 — distancia y rumbo, con transformaciones escritas a mano.
#include "ejercicio02_tf_listener_cpp/dock_geometry.hpp"
#include "gtest/gtest.h"

#include <cmath>

using ejercicio02_tf_listener_cpp::dock_reading;

namespace {

geometry_msgs::msg::Transform at(double x, double y) {
  geometry_msgs::msg::Transform transform;
  transform.translation.x = x;
  transform.translation.y = y;
  return transform;
}

}  // namespace

TEST(DockReading, DelanteDelRobot) {
  const auto reading = dock_reading(at(2.0, 0.0));
  EXPECT_DOUBLE_EQ(reading.distance_m, 2.0);
  EXPECT_DOUBLE_EQ(reading.bearing_rad, 0.0);
}

TEST(DockReading, ALaIzquierdaEsRumboPositivo) {
  const auto reading = dock_reading(at(0.0, 1.5));
  EXPECT_DOUBLE_EQ(reading.distance_m, 1.5);
  EXPECT_DOUBLE_EQ(reading.bearing_rad, M_PI / 2);
}

TEST(DockReading, DetrasYALaDerecha) {
  const auto reading = dock_reading(at(-3.0, -4.0));
  EXPECT_DOUBLE_EQ(reading.distance_m, 5.0);
  EXPECT_NEAR(reading.bearing_rad, std::atan2(-4.0, -3.0), 1e-12);
}

TEST(DockReading, LaAlturaNoCuenta) {
  auto transform = at(3.0, 4.0);
  transform.translation.z = 10.0;
  EXPECT_DOUBLE_EQ(dock_reading(transform).distance_m, 5.0);
}

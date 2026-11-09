// Lo que hace el Buffer por ti: componer la cadena de marcos. Sin nodo ni red:
// tf2::BufferCore es el mismo almacén que usa tf2_ros::Buffer por dentro.
#include "ejercicio02_tf_listener_cpp/dock_geometry.hpp"
#include "geometry_msgs/msg/transform_stamped.hpp"
#include "gtest/gtest.h"
#include "tf2/buffer_core.h"
#include "tf2/exceptions.h"

#include <cmath>
#include <string>

using ejercicio02_tf_listener_cpp::dock_reading;

namespace {

geometry_msgs::msg::TransformStamped make(const std::string& parent, const std::string& child,
                                          double x, double y, double yaw) {
  geometry_msgs::msg::TransformStamped msg;
  msg.header.frame_id = parent;
  msg.child_frame_id = child;
  msg.transform.translation.x = x;
  msg.transform.translation.y = y;
  // Cuaternión de un giro solo en z, la misma fórmula que yaw_to_quaternion
  // del Ejercicio 01.
  msg.transform.rotation.z = std::sin(yaw / 2.0);
  msg.transform.rotation.w = std::cos(yaw / 2.0);
  return msg;
}

class TfBuffer : public ::testing::Test {
 protected:
  void SetUp() override {
    // El dock, fijo a 3 m del origen de odom (static = true: /tf_static).
    buffer_.setTransform(make("odom", "dock", 3.0, 0.0, 0.0), "test", true);
  }
  tf2::BufferCore buffer_;
};

}  // namespace

TEST_F(TfBuffer, RobotEnElOrigenMirandoAlDock) {
  buffer_.setTransform(make("odom", "base_link", 0.0, 0.0, 0.0), "test");
  const auto t = buffer_.lookupTransform("base_link", "dock", tf2::TimePointZero);
  const auto reading = dock_reading(t.transform);
  EXPECT_NEAR(reading.distance_m, 3.0, 1e-9);
  EXPECT_NEAR(reading.bearing_rad, 0.0, 1e-9);
}

TEST_F(TfBuffer, RobotGiradoNoventaGradosTieneElDockALaDerecha) {
  // En odom el dock sigue "delante" (eje x), pero el robot mira hacia +y:
  // desde base_link el dock queda a su derecha, rumbo -90 grados.
  buffer_.setTransform(make("odom", "base_link", 1.0, 0.0, M_PI / 2), "test");
  const auto t = buffer_.lookupTransform("base_link", "dock", tf2::TimePointZero);
  const auto reading = dock_reading(t.transform);
  EXPECT_NEAR(reading.distance_m, 2.0, 1e-9);
  EXPECT_NEAR(reading.bearing_rad, -M_PI / 2, 1e-9);
}

TEST_F(TfBuffer, SinCadenaLanzaExcepcion) {
  // Nadie ha publicado odom -> base_link: no hay camino entre los marcos.
  EXPECT_THROW(buffer_.lookupTransform("base_link", "dock", tf2::TimePointZero),
               tf2::TransformException);
}

// Ejercicio 02, Semana 06 — listener TF en rclcpp.
// Pregunta a TF dónde está el marco `dock` visto desde base_link, 10 veces
// por segundo, y publica la distancia en robot/dock_distance_m.
#include "ejercicio02_tf_listener_cpp/dock_geometry.hpp"
#include "geometry_msgs/msg/transform_stamped.hpp"
#include "rclcpp/rclcpp.hpp"
#include "std_msgs/msg/float64.hpp"
#include "tf2/exceptions.h"
#include "tf2_ros/buffer.h"
#include "tf2_ros/transform_listener.h"

#include <chrono>
#include <cmath>
#include <functional>
#include <memory>
#include <string>

using namespace std::chrono_literals;
using ejercicio02_tf_listener_cpp::dock_reading;
using std_msgs::msg::Float64;

class DockMonitor : public rclcpp::Node {
 public:
  DockMonitor() : Node("dock_monitor") {
    dock_frame_ = declare_parameter<std::string>("dock_frame", "dock");
    publisher_ = create_publisher<Float64>("robot/dock_distance_m", 10);
    // ============================================
    // PASO 2: un listener TF en rclcpp
    // ============================================
    // Buffer guarda las transformaciones de los últimos 10 s (por defecto).
    // TransformListener se suscribe a /tf y /tf_static y llena el Buffer en
    // segundo plano, con su propio hilo: este nodo solo consulta el Buffer.
    // Descomenta las siguientes líneas para el Paso 2:
    //
    // buffer_ = std::make_unique<tf2_ros::Buffer>(get_clock());
    // listener_ = std::make_shared<tf2_ros::TransformListener>(*buffer_);
    // timer_ = create_wall_timer(100ms, std::bind(&DockMonitor::on_timer, this));
  }

 private:
  void on_timer() {
    // Descomenta las siguientes líneas para el Paso 2:
    //
    // geometry_msgs::msg::TransformStamped base_to_dock;
    // try {
    //   // ("base_link", dock): expresa el dock en el marco del robot.
    //   // TimePointZero: la transformación más reciente disponible.
    //   base_to_dock = buffer_->lookupTransform("base_link", dock_frame_, tf2::TimePointZero);
    // } catch (const tf2::TransformException& error) {
    //   // Normal en el arranque: aún no ha llegado ningún mensaje de /tf.
    //   RCLCPP_WARN_THROTTLE(get_logger(), *get_clock(), 2000, "Sin TF base_link -> %s: %s",
    //                        dock_frame_.c_str(), error.what());
    //   return;
    // }
    // const auto reading = dock_reading(base_to_dock.transform);
    // Float64 msg;
    // msg.data = reading.distance_m;
    // publisher_->publish(msg);
    // RCLCPP_INFO_THROTTLE(get_logger(), *get_clock(), 2000, "Dock a %.2f m, rumbo %+.0f grados",
    //                      reading.distance_m, reading.bearing_rad * 180.0 / M_PI);
  }

  std::string dock_frame_;
  rclcpp::Publisher<Float64>::SharedPtr publisher_;
  std::unique_ptr<tf2_ros::Buffer> buffer_;
  std::shared_ptr<tf2_ros::TransformListener> listener_;
  rclcpp::TimerBase::SharedPtr timer_;
};

int main(int argc, char** argv) {
  rclcpp::init(argc, argv);
  rclcpp::spin(std::make_shared<DockMonitor>());
  rclcpp::shutdown();
  return 0;
}

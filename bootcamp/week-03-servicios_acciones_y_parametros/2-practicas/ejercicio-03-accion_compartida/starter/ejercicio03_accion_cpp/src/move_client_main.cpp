// Uso: ros2 run ejercicio03_accion_cpp move_client <distancia_m>
#include "ejercicio03_accion_cpp/move_client.hpp"

#include <chrono>
#include <memory>
#include <stdexcept>
#include <string>

int main(int argc, char* argv[]) {
  rclcpp::init(argc, argv);
  // remove_ros_arguments quita los --ros-args; queda {programa, distancia}.
  const auto args = rclcpp::remove_ros_arguments(argc, argv);
  const double distance_m = args.size() > 1 ? std::stod(args[1]) : 1.0;
  auto node = std::make_shared<MoveClient>();
  try {
    node->send(distance_m);
  } catch (const std::runtime_error& error) {
    RCLCPP_ERROR(node->get_logger(), "%s", error.what());
    rclcpp::shutdown();
    return 1;
  }
  // Spin hasta que llega el resultado (o el rechazo); luego el programa termina.
  rclcpp::executors::SingleThreadedExecutor executor;
  executor.add_node(node);
  while (rclcpp::ok() && !node->done()) {
    executor.spin_once(std::chrono::milliseconds(100));
  }
  rclcpp::shutdown();
  return 0;
}

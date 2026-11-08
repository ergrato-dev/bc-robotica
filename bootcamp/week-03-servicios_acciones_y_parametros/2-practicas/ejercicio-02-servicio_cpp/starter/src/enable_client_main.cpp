// Uso: ros2 run ejercicio02_servicio_cpp enable_client true|false
#include "ejercicio02_servicio_cpp/enable_client.hpp"

#include <chrono>
#include <memory>
#include <stdexcept>
#include <string>

int main(int argc, char* argv[]) {
  rclcpp::init(argc, argv);
  // remove_ros_arguments quita los --ros-args; queda {programa, true|false}.
  const auto args = rclcpp::remove_ros_arguments(argc, argv);
  const bool enable = args.size() > 1 && args[1] == "true";
  auto node = std::make_shared<EnableClient>();
  rclcpp::Client<EnableClient::SetBool>::SharedFuture future;
  try {
    future = node->send(enable);
  } catch (const std::runtime_error& error) {
    RCLCPP_ERROR(node->get_logger(), "%s", error.what());
    rclcpp::shutdown();
    return 1;
  }
  // Hace spin solo hasta que llega la response; luego el programa termina.
  if (rclcpp::spin_until_future_complete(node, future, std::chrono::seconds(5)) ==
      rclcpp::FutureReturnCode::SUCCESS) {
    const auto result = future.get();
    RCLCPP_INFO(node->get_logger(), "success=%d message='%s'", result->success,
                result->message.c_str());
  } else {
    RCLCPP_ERROR(node->get_logger(), "sin respuesta en 5 segundos");
  }
  rclcpp::shutdown();
  return 0;
}

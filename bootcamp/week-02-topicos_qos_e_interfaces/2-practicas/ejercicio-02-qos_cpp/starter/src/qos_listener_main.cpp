#include "ejercicio02_qos_cpp/qos_listener.hpp"

#include <memory>

int main(int argc, char* argv[]) {
  rclcpp::init(argc, argv);
  rclcpp::spin(std::make_shared<QosListener>());
  rclcpp::shutdown();
  return 0;
}

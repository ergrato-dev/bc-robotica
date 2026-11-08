#include "ejercicio02_servicio_cpp/enable_server.hpp"

#include <memory>

int main(int argc, char* argv[]) {
  rclcpp::init(argc, argv);
  rclcpp::spin(std::make_shared<EnableServer>());
  rclcpp::shutdown();
  return 0;
}

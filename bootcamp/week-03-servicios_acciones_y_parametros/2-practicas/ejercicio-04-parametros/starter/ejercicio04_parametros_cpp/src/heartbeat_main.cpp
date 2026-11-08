#include "ejercicio04_parametros_cpp/heartbeat.hpp"

#include <memory>

int main(int argc, char* argv[]) {
  rclcpp::init(argc, argv);
  rclcpp::spin(std::make_shared<Heartbeat>());
  rclcpp::shutdown();
  return 0;
}

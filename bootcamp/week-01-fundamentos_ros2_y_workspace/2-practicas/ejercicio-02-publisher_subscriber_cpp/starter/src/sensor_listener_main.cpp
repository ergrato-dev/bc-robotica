#include "ejercicio02_pubsub_cpp/sensor_listener.hpp"

int main(int argc, char *argv[]) {
  rclcpp::init(argc, argv);
  rclcpp::spin(std::make_shared<SensorListener>());
  rclcpp::shutdown();
  return 0;
}

#include "ejercicio03_reading_cpp/reading_listener.hpp"

#include <memory>

int main(int argc, char* argv[]) {
  rclcpp::init(argc, argv);
  rclcpp::spin(std::make_shared<ReadingListener>());
  rclcpp::shutdown();
  return 0;
}

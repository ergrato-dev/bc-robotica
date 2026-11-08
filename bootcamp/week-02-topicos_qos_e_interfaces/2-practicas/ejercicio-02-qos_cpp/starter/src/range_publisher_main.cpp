#include "ejercicio02_qos_cpp/range_publisher.hpp"

#include <memory>

int main(int argc, char* argv[]) {
  rclcpp::init(argc, argv);
  rclcpp::spin(std::make_shared<RangePublisher>());
  rclcpp::shutdown();
  return 0;
}

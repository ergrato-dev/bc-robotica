// Ejercicio 02, Semana 05 — el filtro de distancia del Ejercicio 01 en C++.
// Escucha robot/range_raw_m y publica en robot/range_m la mediana de las
// últimas `window` lecturas, recortada a [min_range_m, max_range_m].
#include "ejercicio02_gtest_rosbag2_cpp/filtering.hpp"
#include "rclcpp/rclcpp.hpp"
#include "std_msgs/msg/float64.hpp"

#include <cstdint>
#include <deque>
#include <memory>
#include <vector>

using ejercicio02_gtest_rosbag2_cpp::filter_range;
using std_msgs::msg::Float64;

class RangeFilter : public rclcpp::Node {
 public:
  RangeFilter()
      : Node("range_filter"),
        window_size_(static_cast<std::size_t>(declare_parameter<int64_t>("window", 5))),
        min_m_(declare_parameter<double>("min_range_m", 0.05)),
        max_m_(declare_parameter<double>("max_range_m", 4.0)) {
    publisher_ = create_publisher<Float64>("robot/range_m", 10);
    subscription_ = create_subscription<Float64>("robot/range_raw_m", 10,
                                                 [this](const Float64& msg) { on_raw(msg); });
  }

 private:
  void on_raw(const Float64& msg) {
    window_.push_back(msg.data);
    if (window_.size() > window_size_) {
      window_.pop_front();  // la lectura más vieja sale de la ventana
    }
    Float64 out;
    out.data = filter_range({window_.begin(), window_.end()}, min_m_, max_m_);
    publisher_->publish(out);
  }

  std::size_t window_size_;
  double min_m_;
  double max_m_;
  std::deque<double> window_;
  rclcpp::Publisher<Float64>::SharedPtr publisher_;
  rclcpp::Subscription<Float64>::SharedPtr subscription_;
};

int main(int argc, char** argv) {
  rclcpp::init(argc, argv);
  rclcpp::spin(std::make_shared<RangeFilter>());
  rclcpp::shutdown();
  return 0;
}

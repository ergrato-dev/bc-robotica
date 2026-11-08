// Ejercicio 03, Semana 05 — monitor de batería en C++ con fallos a propósito.
// Compila sin un solo warning, pero clang-format encuentra un fallo de formato
// y clang-tidy, cuatro problemas. Cada línea marcada con "elimina" tiene encima
// su versión corregida, comentada.
#include "rclcpp/rclcpp.hpp"
#include "std_msgs/msg/float32.hpp"

#include <cmath>
#include <memory>
#include <string>
#include <vector>

using std_msgs::msg::Float32;

namespace {

// Descomenta la versión corregida (formato: espacios alrededor de "="):
// constexpr int kLowPercent = 20;
constexpr int kLowPercent=20;  // elimina en el Paso 3

// performance-unnecessary-value-param: copia el string en cada llamada.
// Descomenta la versión corregida:
// std::string with_unit(const std::string& label) {
//   return label + " %";
// }
std::string with_unit(std::string label) {  // elimina en el Paso 3
  return label + " %";                      // elimina en el Paso 3
}  // elimina en el Paso 3

double average(const std::vector<int>& values) {
  // readability-braces-around-statements: un if sin llaves invita a añadirle
  // una segunda línea que no queda dentro.
  // Descomenta la versión corregida:
  // if (values.empty()) {
  //   return 0.0;
  // }
  if (values.empty())  // elimina en el Paso 3
    return 0.0;        // elimina en el Paso 3
  double sum = 0.0;
  // modernize-loop-convert: el for con índice se puede salir del vector.
  // Descomenta la versión corregida:
  // for (const int value : values) {
  //   sum += value;
  // }
  for (std::size_t i = 0; i < values.size(); ++i) {  // elimina en el Paso 3
    sum += values[i];                                // elimina en el Paso 3
  }  // elimina en el Paso 3
  return sum / static_cast<double>(values.size());
}

}  // namespace

class BatteryMonitor : public rclcpp::Node {
 public:
  BatteryMonitor() : Node("battery_monitor") {
    subscription_ = create_subscription<Float32>("robot/battery_percent", 10,
                                                 [this](const Float32& msg) { on_battery(msg); });
  }

 private:
  void on_battery(const Float32& msg) {
    // bugprone-narrowing-conversions: float a int pierde los decimales sin
    // avisar (el compilador no lo marca con -Wall -Wextra).
    // Descomenta la versión corregida:
    // const int percent = static_cast<int>(std::lround(msg.data));
    const int percent = msg.data;  // elimina en el Paso 3
    history_.push_back(percent);
    const std::string level = percent < kLowPercent ? "baja" : "ok";
    RCLCPP_INFO(get_logger(), "batería %s (%s, media %.1f)", level.c_str(),
                with_unit(std::to_string(percent)).c_str(), average(history_));
  }

  std::vector<int> history_;
  rclcpp::Subscription<Float32>::SharedPtr subscription_;
};

int main(int argc, char** argv) {
  rclcpp::init(argc, argv);
  rclcpp::spin(std::make_shared<BatteryMonitor>());
  rclcpp::shutdown();
  return 0;
}

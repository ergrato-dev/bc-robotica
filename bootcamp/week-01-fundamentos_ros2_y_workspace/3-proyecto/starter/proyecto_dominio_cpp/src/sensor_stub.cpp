// Proyecto — Semana 01 — capa C++.
//
// NOTA PARA EL APRENDIZ: adapta el topic y el contenido del mensaje a tu
// dominio asignado. Ver la tabla de adaptación en el README de este proyecto.
#include <chrono>
#include <memory>
#include <string>

#include "rclcpp/rclcpp.hpp"
#include "std_msgs/msg/string.hpp"

using namespace std::chrono_literals;

class SensorStub : public rclcpp::Node {
public:
  SensorStub() : Node("sensor_stub_cpp"), counter_{0} {
    // TODO: cambia "dominio/state" por el topic de tu misión.
    publisher_ = create_publisher<std_msgs::msg::String>("dominio/state", 10);
    timer_ = create_wall_timer(1000ms, std::bind(&SensorStub::on_timer, this));
  }

private:
  void on_timer() {
    // TODO: reemplaza este texto plano por el estado simulado real de tu
    // dominio. Por ahora basta con un contador — el mensaje custom llega en
    // la Semana 02.
    auto msg = std_msgs::msg::String();
    msg.data = "estado simulado #" + std::to_string(counter_);
    publisher_->publish(msg);
    counter_++;
  }

  rclcpp::Publisher<std_msgs::msg::String>::SharedPtr publisher_;
  rclcpp::TimerBase::SharedPtr timer_;
  int counter_;
};

int main(int argc, char *argv[]) {
  rclcpp::init(argc, argv);
  rclcpp::spin(std::make_shared<SensorStub>());
  rclcpp::shutdown();
  return 0;
}

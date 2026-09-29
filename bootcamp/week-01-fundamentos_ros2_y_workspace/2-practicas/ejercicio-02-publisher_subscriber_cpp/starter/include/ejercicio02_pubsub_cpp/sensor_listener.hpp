// Ejercicio 02, Semana 01 — subscriber mínimo en rclcpp.
#pragma once

#include <atomic>
#include <string>

#include "rclcpp/rclcpp.hpp"
#include "std_msgs/msg/string.hpp"

class SensorListener : public rclcpp::Node {
public:
  SensorListener() : Node("sensor_listener"), received_count_{0} {
    // ============================================
    // PASO 3: Inicializar la subscripción
    // ============================================
    // Descomenta las siguientes líneas para el Paso 3:
    //
    // subscription_ = create_subscription<std_msgs::msg::String>(
    //     "sensor/state", 10,
    //     std::bind(&SensorListener::on_message, this, std::placeholders::_1));
  }

  int received_count() const { return received_count_.load(); }
  std::string last_message() const { return last_message_; }

private:
  void on_message(const std_msgs::msg::String &msg) {
    received_count_++;
    last_message_ = msg.data;
    RCLCPP_INFO(get_logger(), "Recibido: %s", msg.data.c_str());
  }

  rclcpp::Subscription<std_msgs::msg::String>::SharedPtr subscription_;
  std::atomic<int> received_count_;
  std::string last_message_;
};

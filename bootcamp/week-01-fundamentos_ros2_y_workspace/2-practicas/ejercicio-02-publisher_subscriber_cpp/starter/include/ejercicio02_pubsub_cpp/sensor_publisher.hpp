// Ejercicio 02, Semana 01 — publisher mínimo en rclcpp.
//
// Completa los pasos en orden. Cada paso tiene un test en test/test_pubsub.cpp
// que falla hasta que descomentas el bloque correspondiente.
#pragma once

#include <chrono>
#include <string>

#include "rclcpp/rclcpp.hpp"
#include "std_msgs/msg/string.hpp"

using namespace std::chrono_literals;

class SensorPublisher : public rclcpp::Node {
public:
  SensorPublisher() : Node("sensor_publisher"), counter_{0} {
    // ============================================
    // PASO 1: Inicializar el publisher
    // ============================================
    // Descomenta la siguiente línea para el Paso 1:
    //
    // publisher_ = create_publisher<std_msgs::msg::String>("sensor/state", 10);

    // ============================================
    // PASO 2: Inicializar el timer que dispara la publicación
    // ============================================
    // Descomenta la siguiente línea para el Paso 2
    // (requiere el Paso 1 ya hecho, si no publisher_ sigue siendo nullptr):
    //
    // timer_ = create_wall_timer(500ms, std::bind(&SensorPublisher::on_timer, this));
  }

  // Expuesto para que los tests puedan comprobar el estado sin depender de logs.
  rclcpp::Publisher<std_msgs::msg::String>::SharedPtr publisher() const { return publisher_; }

private:
  void on_timer() {
    auto msg = std_msgs::msg::String();
    msg.data = "lectura #" + std::to_string(counter_);
    publisher_->publish(msg);
    RCLCPP_INFO(get_logger(), "Publicado: %s", msg.data.c_str());
    counter_++;
  }

  rclcpp::Publisher<std_msgs::msg::String>::SharedPtr publisher_;
  rclcpp::TimerBase::SharedPtr timer_;
  int counter_;
};

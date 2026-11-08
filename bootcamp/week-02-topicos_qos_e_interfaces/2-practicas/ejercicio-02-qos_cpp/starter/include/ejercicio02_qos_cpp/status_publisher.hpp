// Ejercicio 02, Semana 02 — publisher latched (TRANSIENT_LOCAL) en rclcpp.
#pragma once

#include "rclcpp/rclcpp.hpp"
#include "std_msgs/msg/string.hpp"

// Perfil latched compartido por el publisher y por qos_listener.hpp.
// depth=1 porque solo importa el último estado.
inline rclcpp::QoS latched_qos() {
  return rclcpp::QoS(1).reliable().transient_local();
}

class StatusPublisher : public rclcpp::Node {
 public:
  StatusPublisher() : Node("status_publisher") {
    // ============================================
    // PASO 3: Publicar una sola vez con QoS latched
    // ============================================
    // El mensaje queda guardado para cualquier subscriber TRANSIENT_LOCAL que
    // se conecte después.
    // Descomenta las siguientes líneas para el Paso 3:
    //
    // publisher_ = create_publisher<std_msgs::msg::String>("robot/status", latched_qos());
    // std_msgs::msg::String msg;
    // msg.data = "ready";
    // publisher_->publish(msg);
    // RCLCPP_INFO(get_logger(), "Estado publicado una vez: ready");
  }

 private:
  rclcpp::Publisher<std_msgs::msg::String>::SharedPtr publisher_;
};

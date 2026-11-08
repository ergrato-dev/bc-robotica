// Ejercicio 02, Semana 02 — subscriber que pide el mismo QoS que cada publisher.
#pragma once

#include "ejercicio02_qos_cpp/status_publisher.hpp"
#include "rclcpp/rclcpp.hpp"
#include "sensor_msgs/msg/range.hpp"
#include "std_msgs/msg/string.hpp"

#include <functional>
#include <string>

class QosListener : public rclcpp::Node {
 public:
  QosListener() : Node("qos_listener") {
    // ============================================
    // PASO 4: Suscribirse con el QoS de cada publisher
    // ============================================
    // Con rclcpp::QoS(10) (RELIABLE) en sensor/range no recibirías nada; con
    // QoS(10) (VOLATILE) en robot/status te perderías el "ready" ya publicado.
    // Descomenta las siguientes líneas para el Paso 4:
    //
    // range_sub_ = create_subscription<sensor_msgs::msg::Range>(
    //     "sensor/range", rclcpp::SensorDataQoS(),
    //     std::bind(&QosListener::on_range, this, std::placeholders::_1));
    // status_sub_ = create_subscription<std_msgs::msg::String>(
    //     "robot/status", latched_qos(),
    //     std::bind(&QosListener::on_status, this, std::placeholders::_1));
  }

  // Expuestos para que los tests comprueben el estado sin depender de logs.
  int range_count() const { return range_count_; }
  const std::string& last_frame_id() const { return last_frame_id_; }
  const std::string& status() const { return status_; }

 private:
  void on_range(const sensor_msgs::msg::Range& msg) {
    range_count_++;
    last_frame_id_ = msg.header.frame_id;
    // throttle: a 10 Hz, un log por segundo basta.
    RCLCPP_INFO_THROTTLE(get_logger(), *get_clock(), 1000, "%s: %.2f m",
                         msg.header.frame_id.c_str(), static_cast<double>(msg.range));
  }

  void on_status(const std_msgs::msg::String& msg) {
    status_ = msg.data;
    RCLCPP_INFO(get_logger(), "Estado del robot: %s", msg.data.c_str());
  }

  rclcpp::Subscription<sensor_msgs::msg::Range>::SharedPtr range_sub_;
  rclcpp::Subscription<std_msgs::msg::String>::SharedPtr status_sub_;
  int range_count_{0};
  std::string last_frame_id_;
  std::string status_;
};

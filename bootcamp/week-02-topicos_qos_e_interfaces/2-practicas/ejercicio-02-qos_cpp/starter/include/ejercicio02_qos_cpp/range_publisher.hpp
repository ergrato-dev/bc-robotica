// Ejercicio 02, Semana 02 — publisher de sensor con QoS sensor_data en rclcpp.
//
// Completa los pasos en orden. Cada paso tiene un test en test/test_qos.cpp
// que falla hasta que descomentas el bloque correspondiente.
#pragma once

#include "rclcpp/rclcpp.hpp"
#include "sensor_msgs/msg/range.hpp"

#include <chrono>
#include <functional>

class RangePublisher : public rclcpp::Node {
 public:
  RangePublisher() : Node("range_publisher") {
    // ============================================
    // PASO 1: Publisher con el preset de sensores
    // ============================================
    // rclcpp::SensorDataQoS() = KEEP_LAST 5, BEST_EFFORT, VOLATILE.
    // Descomenta las siguientes líneas para el Paso 1:
    //
    // publisher_ = create_publisher<sensor_msgs::msg::Range>("sensor/range", rclcpp::SensorDataQoS());
    // timer_ = create_wall_timer(std::chrono::milliseconds(100),
    //                            std::bind(&RangePublisher::on_timer, this));
  }

 private:
  void on_timer() {
    sensor_msgs::msg::Range msg;

    // ============================================
    // PASO 2: Rellenar el Header
    // ============================================
    // now() devuelve rclcpp::Time, que se convierte solo a builtin_interfaces/Time.
    // Descomenta las siguientes líneas para el Paso 2:
    //
    // msg.header.stamp = now();
    // msg.header.frame_id = "range_sensor";

    msg.radiation_type = sensor_msgs::msg::Range::ULTRASOUND;
    msg.field_of_view = 0.5F;  // rad
    msg.min_range = 0.02F;     // m
    msg.max_range = 4.0F;      // m
    msg.range = distance_m_;
    publisher_->publish(msg);
    // Distancia simulada: sube de 1.0 a 3.0 m y vuelve a empezar.
    distance_m_ = distance_m_ >= 3.0F ? 1.0F : distance_m_ + 0.1F;
  }

  rclcpp::Publisher<sensor_msgs::msg::Range>::SharedPtr publisher_;
  rclcpp::TimerBase::SharedPtr timer_;
  float distance_m_{1.0F};
};

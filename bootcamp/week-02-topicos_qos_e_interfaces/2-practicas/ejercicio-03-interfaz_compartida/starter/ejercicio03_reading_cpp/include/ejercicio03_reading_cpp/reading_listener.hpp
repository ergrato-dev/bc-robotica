// Ejercicio 03, Semana 02 — listener C++ de la interfaz propia SensorReading.
//
// Requiere los Pasos 1 y 2 hechos en ejercicio03_interfaces y compilados: hasta
// entonces el header generado no tiene los campos y este archivo no compila.
#pragma once

#include "rclcpp/rclcpp.hpp"

#include <functional>
#include <string>
// Regla del header: tipo SensorReading -> archivo sensor_reading.hpp
#include "ejercicio03_interfaces/msg/sensor_reading.hpp"

class ReadingListener : public rclcpp::Node {
 public:
  ReadingListener() : Node("reading_listener") {
    // ============================================
    // PASO 4: Suscribirse a SensorReading
    // ============================================
    // Mismo topic y mismo tipo que el publisher Python: el lenguaje no importa.
    // Descomenta las siguientes líneas para el Paso 4:
    //
    // subscription_ = create_subscription<ejercicio03_interfaces::msg::SensorReading>(
    //     "sensor/reading", 10, std::bind(&ReadingListener::on_reading, this, std::placeholders::_1));
  }

  // Expuestos para que los tests comprueben el estado sin depender de logs.
  int received_count() const { return received_count_; }
  int warning_count() const { return warning_count_; }
  const std::string& last_sensor_id() const { return last_sensor_id_; }

 private:
  void on_reading(const ejercicio03_interfaces::msg::SensorReading& msg) {
    using ejercicio03_interfaces::msg::SensorReading;
    received_count_++;
    last_sensor_id_ = msg.sensor_id;
    // Constante del .msg en lugar de un número mágico.
    if (msg.status != SensorReading::STATUS_OK) {
      warning_count_++;
      RCLCPP_WARN(get_logger(), "%s fuera de rango: %.2f %s", msg.sensor_id.c_str(), msg.value,
                  msg.unit.c_str());
      return;
    }
    RCLCPP_INFO(get_logger(), "%s: %.2f %s", msg.sensor_id.c_str(), msg.value, msg.unit.c_str());
  }

  rclcpp::Subscription<ejercicio03_interfaces::msg::SensorReading>::SharedPtr subscription_;
  int received_count_{0};
  int warning_count_{0};
  std::string last_sensor_id_;
};

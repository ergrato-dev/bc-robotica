// Ejercicio 04, Semana 04 — el driver lifecycle del Ejercicio 03 en rclcpp.
//
// Mismo nombre de nodo, parámetro, topic y transiciones que la versión
// Python: los mismos comandos `ros2 lifecycle` controlan las dos.
#pragma once

#include "rclcpp/rclcpp.hpp"
#include "rclcpp_lifecycle/lifecycle_node.hpp"
#include "std_msgs/msg/float64.hpp"

#include <chrono>
#include <cmath>
#include <memory>

namespace ejercicio04_lifecycle_cpp {

using CallbackReturn = rclcpp_lifecycle::node_interfaces::LifecycleNodeInterface::CallbackReturn;

class RangeDriver : public rclcpp_lifecycle::LifecycleNode {
 public:
  explicit RangeDriver(const rclcpp::NodeOptions& options = rclcpp::NodeOptions())
      : LifecycleNode("range_driver", options) {
    // Se declara aquí para poder fijarlo con -p antes de configurar.
    declare_parameter<double>("rate_hz", 5.0);
  }

  CallbackReturn on_configure(const rclcpp_lifecycle::State& /*previous*/) override {
    // ============================================
    // PASO 1: configure — validar y reservar recursos
    // ============================================
    // FAILURE deja el nodo en unconfigured. create_publisher de un
    // LifecycleNode devuelve un LifecyclePublisher: solo entrega en active.
    // Descomenta las siguientes líneas para el Paso 1:
    //
    // const double rate_hz = get_parameter("rate_hz").as_double();
    // if (rate_hz <= 0.0) {
    //   RCLCPP_ERROR(get_logger(), "rate_hz debe ser > 0, llegó %.2f", rate_hz);
    //   return CallbackReturn::FAILURE;
    // }
    // publisher_ = create_publisher<std_msgs::msg::Float64>("robot/range_m", 10);
    // RCLCPP_INFO(get_logger(), "Configurado a %.1f Hz", rate_hz);
    return CallbackReturn::SUCCESS;
  }

  CallbackReturn on_activate(const rclcpp_lifecycle::State& previous) override {
    // ============================================
    // PASO 2 (parte A): activate — empezar a trabajar
    // ============================================
    // LifecycleNode::on_activate activa los publishers lifecycle. Sin esa
    // llamada, publish() solo escribe un warning y descarta el mensaje.
    // Descomenta las siguientes líneas para el Paso 2:
    //
    // const double rate_hz = get_parameter("rate_hz").as_double();
    // const auto period = std::chrono::duration<double>(1.0 / rate_hz);
    // timer_ = create_wall_timer(period, [this]() { on_timer(); });
    // RCLCPP_INFO(get_logger(), "Activo");
    // return LifecycleNode::on_activate(previous);
    (void)previous;                  // elimina esta línea al completar el Paso 2
    return CallbackReturn::SUCCESS;  // elimina esta línea al completar el Paso 2
  }

  CallbackReturn on_deactivate(const rclcpp_lifecycle::State& previous) override {
    // ============================================
    // PASO 2 (parte B): deactivate — parar sin soltar recursos
    // ============================================
    // reset() destruye el timer; el publisher queda creado e inactivo.
    // Descomenta las siguientes líneas para el Paso 2:
    //
    // timer_.reset();
    // RCLCPP_INFO(get_logger(), "Inactivo");
    // return LifecycleNode::on_deactivate(previous);
    (void)previous;                  // elimina esta línea al completar el Paso 2
    return CallbackReturn::SUCCESS;  // elimina esta línea al completar el Paso 2
  }

  CallbackReturn on_cleanup(const rclcpp_lifecycle::State& /*previous*/) override {
    // ============================================
    // PASO 3: cleanup y shutdown — soltar lo reservado en configure
    // ============================================
    // Descomenta las siguientes líneas para el Paso 3:
    //
    // publisher_.reset();
    // RCLCPP_INFO(get_logger(), "Recursos liberados");
    return CallbackReturn::SUCCESS;
  }

  CallbackReturn on_shutdown(const rclcpp_lifecycle::State& previous) override {
    timer_.reset();
    return on_cleanup(previous);
  }

  bool has_timer() const { return timer_ != nullptr; }

 private:
  void on_timer() {
    // Misma distancia simulada que en Python: entre 0.5 y 2.5 m.
    ++readings_;
    std_msgs::msg::Float64 msg;
    msg.data = 1.5 + std::sin(readings_ / 10.0);
    publisher_->publish(msg);
  }

  rclcpp_lifecycle::LifecyclePublisher<std_msgs::msg::Float64>::SharedPtr publisher_;
  rclcpp::TimerBase::SharedPtr timer_;
  int readings_{0};
};

}  // namespace ejercicio04_lifecycle_cpp

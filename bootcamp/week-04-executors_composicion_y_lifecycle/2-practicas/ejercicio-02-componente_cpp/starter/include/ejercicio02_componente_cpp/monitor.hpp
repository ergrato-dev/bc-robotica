// Ejercicio 02, Semana 04 — el monitor del Ejercicio 01 en rclcpp, como
// componente.
//
// Mismo nombre de nodo, mismo servicio y misma respuesta que la versión
// Python: robot/slow_check tarda 0.5 s y cuenta los ticks del timer que
// hubo mientras trabajaba.
#pragma once

#include "rclcpp/rclcpp.hpp"
#include "std_srvs/srv/trigger.hpp"

#include <atomic>
#include <chrono>
#include <functional>
#include <memory>
#include <string>
#include <thread>

namespace ejercicio02_componente_cpp {

using namespace std::chrono_literals;

class Monitor : public rclcpp::Node {
 public:
  using Trigger = std_srvs::srv::Trigger;

  // Un componente necesita este constructor: el container le pasa sus
  // NodeOptions (nombre, parámetros, intra-process...). El valor por defecto
  // permite también crearlo a mano, como hace el test.
  explicit Monitor(const rclcpp::NodeOptions& options = rclcpp::NodeOptions())
      : Node("monitor", options) {
    // ============================================
    // PASO 1: Un grupo para cada callback
    // ============================================
    // Un nullptr significa "grupo por defecto del nodo", que es
    // MutuallyExclusive: el timer esperaría a que acabe el servicio.
    // Descomenta las siguientes líneas para el Paso 1:
    //
    // timer_group_ = create_callback_group(rclcpp::CallbackGroupType::MutuallyExclusive);
    // service_group_ = create_callback_group(rclcpp::CallbackGroupType::MutuallyExclusive);

    timer_ = create_wall_timer(100ms, [this]() { ++ticks_; }, timer_group_);
    service_ = create_service<Trigger>(
        "robot/slow_check",
        std::bind(&Monitor::on_slow_check, this, std::placeholders::_1, std::placeholders::_2),
        rclcpp::ServicesQoS(), service_group_);
  }

  rclcpp::CallbackGroup::SharedPtr timer_group() const { return timer_group_; }
  rclcpp::CallbackGroup::SharedPtr service_group() const { return service_group_; }

 private:
  void on_slow_check(const std::shared_ptr<Trigger::Request> /*request*/,
                     std::shared_ptr<Trigger::Response> response) {
    const int start = ticks_;
    // Simula un trabajo pesado: bloquea el hilo que ejecuta este callback.
    std::this_thread::sleep_for(500ms);
    response->success = true;
    response->message = "ticks durante la comprobación: " + std::to_string(ticks_ - start);
    RCLCPP_INFO(get_logger(), "%s", response->message.c_str());
  }

  rclcpp::CallbackGroup::SharedPtr timer_group_;
  rclcpp::CallbackGroup::SharedPtr service_group_;
  rclcpp::TimerBase::SharedPtr timer_;
  rclcpp::Service<Trigger>::SharedPtr service_;
  // Atómico: con executor multihilo, el timer lo escribe y el servicio lo lee
  // desde hilos distintos.
  std::atomic<int> ticks_{0};
};

}  // namespace ejercicio02_componente_cpp

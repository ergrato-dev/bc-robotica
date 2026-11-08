// Proyecto — Semana 02 — capa C++.
//
// Evolución del sensor_stub de la Semana 01: mismo nodo, topic, tipo y QoS que
// la capa Python, para que sigan siendo intercambiables. Adapta los TODO.
#pragma once

#include "rclcpp/rclcpp.hpp"

#include <chrono>
#include <functional>
// TODO: si renombraste DomainState.msg, cambia el include (snake_case).
#include "proyecto_dominio_interfaces/msg/domain_state.hpp"

// Mismo perfil que STATE_QOS en sensor_stub.py. TODO: justifícalo en tu README.
inline rclcpp::QoS state_qos() {
  return rclcpp::QoS(10).reliable().durability_volatile();
}

class SensorStub : public rclcpp::Node {
 public:
  SensorStub() : Node("sensor_stub") {
    // TODO: cambia "dominio/state" por el topic de tu misión (relativo, sin "/").
    publisher_ = create_publisher<proyecto_dominio_interfaces::msg::DomainState>("dominio/state",
                                                                                 state_qos());
    timer_ = create_wall_timer(std::chrono::seconds(1), std::bind(&SensorStub::on_timer, this));
  }

 private:
  void on_timer() {
    using proyecto_dominio_interfaces::msg::DomainState;
    DomainState msg;
    msg.header.stamp = now();
    // TODO: frame del robot de tu dominio; en la Semana 06 lo conectas con TF2.
    msg.header.frame_id = "base_link";
    // TODO: valores simulados con sentido en tu misión.
    msg.location = "pasillo_A";
    msg.pending_tasks = 3;
    msg.battery_percent = battery_percent_;
    msg.mode = DomainState::MODE_WORKING;
    publisher_->publish(msg);
    // Batería simulada: baja 0.5 % por segundo y se "recarga" al llegar a 20 %.
    battery_percent_ = battery_percent_ <= 20.0F ? 100.0F : battery_percent_ - 0.5F;
  }

  rclcpp::Publisher<proyecto_dominio_interfaces::msg::DomainState>::SharedPtr publisher_;
  rclcpp::TimerBase::SharedPtr timer_;
  float battery_percent_{100.0F};
};

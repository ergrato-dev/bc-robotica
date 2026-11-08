// Proyecto — Semana 03 — capa C++.
//
// Evolución del sensor_stub de la Semana 02: mismo nodo, topic, tipo, QoS,
// servicio y parámetro que la capa Python, para que sigan siendo
// intercambiables. Adapta los TODO.
#pragma once

#include "rcl_interfaces/msg/floating_point_range.hpp"
#include "rcl_interfaces/msg/parameter_descriptor.hpp"
#include "rclcpp/rclcpp.hpp"

#include <chrono>
#include <functional>
#include <memory>
#include <string>
#include <vector>
// TODO: si renombraste DomainState.msg o SetMode.srv, cambia los includes (snake_case).
#include "proyecto_dominio_interfaces/msg/domain_state.hpp"
#include "proyecto_dominio_interfaces/srv/set_mode.hpp"

// Mismo perfil que STATE_QOS en sensor_stub.py. TODO: justifícalo en tu README.
inline rclcpp::QoS state_qos() {
  return rclcpp::QoS(10).reliable().durability_volatile();
}

class SensorStub : public rclcpp::Node {
 public:
  using DomainState = proyecto_dominio_interfaces::msg::DomainState;
  using SetMode = proyecto_dominio_interfaces::srv::SetMode;

  SensorStub() : Node("sensor_stub") {
    // TODO: cambia "dominio/state" por el topic de tu misión (relativo, sin "/").
    publisher_ = create_publisher<DomainState>("dominio/state", state_qos());

    // Mismo rango que en Python. TODO: ajústalo a tu misión.
    rcl_interfaces::msg::FloatingPointRange range;
    range.from_value = 0.1;
    range.to_value = 10.0;
    rcl_interfaces::msg::ParameterDescriptor descriptor;
    descriptor.description = "Segundos entre dos estados publicados";
    descriptor.floating_point_range.push_back(range);
    restart_timer(declare_parameter<double>("publish_period_s", 1.0, descriptor));
    post_set_handle_ =
        add_post_set_parameters_callback([this](const std::vector<rclcpp::Parameter>& parameters) {
          for (const auto& parameter : parameters) {
            if (parameter.get_name() == "publish_period_s") {
              restart_timer(parameter.as_double());
            }
          }
        });

    // TODO: cambia "dominio/set_mode" por el servicio de tu misión.
    service_ = create_service<SetMode>(
        "dominio/set_mode", std::bind(&SensorStub::on_set_mode, this, std::placeholders::_1,
                                      std::placeholders::_2));
  }

 private:
  void restart_timer(double period_s) {
    timer_ = create_wall_timer(std::chrono::duration<double>(period_s),
                               std::bind(&SensorStub::on_timer, this));
  }

  void on_timer() {
    DomainState msg;
    msg.header.stamp = now();
    // TODO: frame del robot de tu dominio; en la Semana 06 lo conectas con TF2.
    msg.header.frame_id = "base_link";
    // TODO: valores simulados con sentido en tu misión.
    msg.location = "pasillo_A";
    msg.pending_tasks = 3;
    msg.battery_percent = battery_percent_;
    msg.mode = mode_;
    publisher_->publish(msg);
    // Batería simulada: baja 0.5 % por estado y se "recarga" al llegar a 20 %.
    battery_percent_ = battery_percent_ <= 20.0F ? 100.0F : battery_percent_ - 0.5F;
  }

  void on_set_mode(const std::shared_ptr<SetMode::Request> request,
                   std::shared_ptr<SetMode::Response> response) {
    // TODO: los MODE_* de tu tipo.
    const bool valid = request->mode == DomainState::MODE_IDLE ||
                       request->mode == DomainState::MODE_WORKING ||
                       request->mode == DomainState::MODE_CHARGING;
    if (!valid) {
      response->accepted = false;
      response->message = "modo desconocido: " + std::to_string(request->mode);
      return;
    }
    mode_ = request->mode;
    response->accepted = true;
    response->message = "modo " + std::to_string(request->mode);
    RCLCPP_INFO(get_logger(), "Nuevo modo: %u", static_cast<unsigned>(mode_));
  }

  rclcpp::Publisher<DomainState>::SharedPtr publisher_;
  rclcpp::TimerBase::SharedPtr timer_;
  rclcpp::Service<SetMode>::SharedPtr service_;
  PostSetParametersCallbackHandle::SharedPtr post_set_handle_;
  float battery_percent_{100.0F};
  uint8_t mode_{DomainState::MODE_WORKING};
};

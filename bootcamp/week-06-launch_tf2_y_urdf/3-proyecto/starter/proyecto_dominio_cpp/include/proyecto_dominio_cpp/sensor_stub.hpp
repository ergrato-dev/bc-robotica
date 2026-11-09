// Proyecto — Semana 06 — capa C++.
//
// Nodo lifecycle y componente de la Semana 04. Mismo nodo, topic, tipo, QoS,
// servicio, parámetro y transiciones que la capa Python, para que sigan siendo
// intercambiables en bringup.launch.py (impl:=py o impl:=cpp). Esta semana la
// capa Python publica además odom -> base_link en /tf; aquí lo añades tú
// (Requisito 4 del README). Adapta los TODO.
#pragma once

#include "proyecto_dominio_cpp/route.hpp"
#include "rcl_interfaces/msg/floating_point_range.hpp"
#include "rcl_interfaces/msg/parameter_descriptor.hpp"
#include "rclcpp/rclcpp.hpp"
#include "rclcpp_lifecycle/lifecycle_node.hpp"

#include <chrono>
#include <functional>
#include <memory>
#include <string>
#include <vector>
// TODO: si renombraste DomainState.msg o SetMode.srv, cambia los includes (snake_case).
#include "proyecto_dominio_interfaces/msg/domain_state.hpp"
#include "proyecto_dominio_interfaces/srv/set_mode.hpp"

namespace proyecto_dominio_cpp {

// Mismo perfil que STATE_QOS en sensor_stub.py. TODO: justifícalo en tu README.
inline rclcpp::QoS state_qos() {
  return rclcpp::QoS(10).reliable().durability_volatile();
}

// La ruta simulada: los mismos valores que ROUTE_LENGTH_M y SPEED_MPS en
// sensor_stub.py. TODO: los de tu misión.
constexpr double kRouteLengthM = 10.0;
constexpr double kSpeedMps = 0.5;

using CallbackReturn = rclcpp_lifecycle::node_interfaces::LifecycleNodeInterface::CallbackReturn;

class SensorStub : public rclcpp_lifecycle::LifecycleNode {
 public:
  using DomainState = proyecto_dominio_interfaces::msg::DomainState;
  using SetMode = proyecto_dominio_interfaces::srv::SetMode;

  explicit SensorStub(const rclcpp::NodeOptions& options = rclcpp::NodeOptions())
      : LifecycleNode("sensor_stub", options) {
    // El parámetro existe desde el arranque, como en Python. TODO: ajusta el rango.
    rcl_interfaces::msg::FloatingPointRange range;
    range.from_value = 0.1;
    range.to_value = 10.0;
    rcl_interfaces::msg::ParameterDescriptor descriptor;
    descriptor.description = "Segundos entre dos estados publicados";
    descriptor.floating_point_range.push_back(range);
    declare_parameter<double>("publish_period_s", 1.0, descriptor);
    post_set_handle_ =
        add_post_set_parameters_callback([this](const std::vector<rclcpp::Parameter>& parameters) {
          for (const auto& parameter : parameters) {
            // Sin timer (no active), el valor nuevo se usará en el próximo activate.
            if (parameter.get_name() == "publish_period_s" && timer_) {
              start_timer(parameter.as_double());
            }
          }
        });
  }

  // --- Transiciones ----------------------------------------------------------

  CallbackReturn on_configure(const rclcpp_lifecycle::State& /*previous*/) override {
    // TODO: cambia "dominio/state" y "dominio/set_mode" por los de tu misión.
    publisher_ = create_publisher<DomainState>("dominio/state", state_qos());
    // El servicio responde ya en inactive: se puede elegir el modo antes de
    // empezar a publicar.
    service_ = create_service<SetMode>(
        "dominio/set_mode",
        std::bind(&SensorStub::on_set_mode, this, std::placeholders::_1, std::placeholders::_2));
    return CallbackReturn::SUCCESS;
  }

  CallbackReturn on_activate(const rclcpp_lifecycle::State& previous) override {
    start_timer(get_parameter("publish_period_s").as_double());
    // Activa el publisher lifecycle; sin esta llamada no sale nada.
    return LifecycleNode::on_activate(previous);
  }

  CallbackReturn on_deactivate(const rclcpp_lifecycle::State& previous) override {
    timer_.reset();
    return LifecycleNode::on_deactivate(previous);
  }

  CallbackReturn on_cleanup(const rclcpp_lifecycle::State& /*previous*/) override {
    publisher_.reset();
    service_.reset();
    // Volver a unconfigured es volver al principio: batería y modo también.
    battery_percent_ = 100.0F;
    mode_ = DomainState::MODE_WORKING;
    distance_m_ = 0.0;
    return CallbackReturn::SUCCESS;
  }

  CallbackReturn on_shutdown(const rclcpp_lifecycle::State& previous) override {
    timer_.reset();
    return on_cleanup(previous);
  }

  bool has_timer() const { return timer_ != nullptr; }

 private:
  // rclcpp no cambia el periodo de un timer existente: se crea otro.
  void start_timer(double period_s) {
    timer_ = create_wall_timer(std::chrono::duration<double>(period_s),
                               std::bind(&SensorStub::on_timer, this));
  }

  void on_timer() {
    DomainState msg;
    msg.header.stamp = now();
    // El estado describe al robot entero: va en su marco del cuerpo.
    msg.header.frame_id = "base_link";
    // TODO: valores simulados con sentido en tu misión.
    msg.location = "pasillo_A";
    msg.pending_tasks = 3;
    msg.battery_percent = battery_percent_;
    msg.mode = mode_;
    publisher_->publish(msg);
    // Batería simulada: baja 0.5 % por estado y se "recarga" al llegar a 20 %.
    battery_percent_ = battery_percent_ <= 20.0F ? 100.0F : battery_percent_ - 0.5F;
    // TODO (Requisito 4): publica odom -> base_link en /tf con el mismo stamp
    // que el estado, igual que _broadcast_pose en sensor_stub.py: avanza
    // distance_m_ lo recorrido en un periodo, calcula route_pose y envíalo con
    // un tf2_ros::TransformBroadcaster creado en el constructor.
  }

  void on_set_mode(const std::shared_ptr<SetMode::Request>& request,
                   const std::shared_ptr<SetMode::Response>& response) {
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

  rclcpp_lifecycle::LifecyclePublisher<DomainState>::SharedPtr publisher_;
  rclcpp::TimerBase::SharedPtr timer_;
  rclcpp::Service<SetMode>::SharedPtr service_;
  PostSetParametersCallbackHandle::SharedPtr post_set_handle_;
  float battery_percent_{100.0F};
  uint8_t mode_{DomainState::MODE_WORKING};
  // Metros recorridos por la ruta simulada (Requisito 4).
  double distance_m_{0.0};
};

}  // namespace proyecto_dominio_cpp

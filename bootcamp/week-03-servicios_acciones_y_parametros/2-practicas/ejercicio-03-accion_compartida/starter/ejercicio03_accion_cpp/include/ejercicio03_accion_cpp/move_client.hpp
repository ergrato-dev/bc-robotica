// Ejercicio 03, Semana 03 — action client de robot/move_distance en rclcpp.
//
// El server está escrito en Python (ejercicio03_accion_py); el cliente solo
// conoce el contrato MoveDistance.action.
#pragma once

#include "ejercicio03_interfaces/action/move_distance.hpp"
#include "rclcpp/rclcpp.hpp"
#include "rclcpp_action/rclcpp_action.hpp"

#include <chrono>
#include <memory>
#include <stdexcept>

class MoveClient : public rclcpp::Node {
 public:
  using MoveDistance = ejercicio03_interfaces::action::MoveDistance;
  using GoalHandle = rclcpp_action::ClientGoalHandle<MoveDistance>;

  MoveClient() : Node("move_client") {
    // ============================================
    // PASO 4: Crear el action client
    // ============================================
    // Descomenta la siguiente línea para el Paso 4:
    //
    // client_ = rclcpp_action::create_client<MoveDistance>(this, "robot/move_distance");
  }

  // Envía el goal sin bloquear. Las tres callbacks llegan durante el spin de
  // quien llame; done() pasa a true con el resultado o con el rechazo.
  void send(double distance_m) {
    // ============================================
    // PASO 5: Enviar el goal con sus callbacks
    // ============================================
    // goal_response: aceptado o rechazado (handle nulo = rechazado).
    // feedback: una llamada por cada publish_feedback del server.
    // result: una sola vez, con el código final (SUCCEEDED, CANCELED...).
    // Descomenta las siguientes líneas para el Paso 5:
    //
    // if (!client_->wait_for_action_server(std::chrono::seconds(2))) {
    //   throw std::runtime_error("el action server robot/move_distance no está disponible");
    // }
    // MoveDistance::Goal goal;
    // goal.distance_m = distance_m;
    // rclcpp_action::Client<MoveDistance>::SendGoalOptions options;
    // options.goal_response_callback = [this](const GoalHandle::SharedPtr& handle) {
    //   accepted_ = static_cast<bool>(handle);
    //   if (!accepted_) {
    //     RCLCPP_WARN(get_logger(), "Goal rechazado");
    //     done_ = true;
    //   }
    // };
    // options.feedback_callback = [this](GoalHandle::SharedPtr,
    //                                    const std::shared_ptr<const MoveDistance::Feedback> fb) {
    //   ++feedback_count_;
    //   RCLCPP_INFO(get_logger(), "Faltan %.2f m", fb->remaining_m);
    // };
    // options.result_callback = [this](const GoalHandle::WrappedResult& result) {
    //   code_ = result.code;
    //   traveled_m_ = result.result->traveled_m;
    //   done_ = true;
    //   RCLCPP_INFO(get_logger(), "Terminado: %.2f m recorridos", traveled_m_);
    // };
    // client_->async_send_goal(goal, options);
    (void)distance_m;                              // elimina esta línea al completar el Paso 5
    throw std::logic_error("completa el Paso 5");  // elimina esta línea al completar el Paso 5
  }

  bool done() const { return done_; }
  bool accepted() const { return accepted_; }
  int feedback_count() const { return feedback_count_; }
  double traveled_m() const { return traveled_m_; }
  rclcpp_action::ResultCode code() const { return code_; }

 private:
  rclcpp_action::Client<MoveDistance>::SharedPtr client_;
  bool done_{false};
  bool accepted_{false};
  int feedback_count_{0};
  double traveled_m_{0.0};
  rclcpp_action::ResultCode code_{rclcpp_action::ResultCode::UNKNOWN};
};

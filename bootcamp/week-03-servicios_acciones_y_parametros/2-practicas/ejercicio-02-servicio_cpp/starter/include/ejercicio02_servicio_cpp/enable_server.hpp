// Ejercicio 02, Semana 03 — server del servicio robot/enable en rclcpp.
#pragma once

#include "rclcpp/rclcpp.hpp"
#include "std_srvs/srv/set_bool.hpp"

#include <functional>
#include <memory>
#include <string>

class EnableServer : public rclcpp::Node {
 public:
  using SetBool = std_srvs::srv::SetBool;

  EnableServer() : Node("enable_server") {
    // ============================================
    // PASO 1: Crear el servicio
    // ============================================
    // Mismo tipo y nombre que el server de Python: un cliente no distingue
    // en qué lenguaje está escrito el server.
    // Descomenta las siguientes líneas para el Paso 1:
    //
    // service_ = create_service<SetBool>(
    //     "robot/enable", std::bind(&EnableServer::on_enable, this, std::placeholders::_1,
    //                               std::placeholders::_2));
  }

  bool enabled() const { return enabled_; }

 private:
  void on_enable(const std::shared_ptr<SetBool::Request> request,
                 std::shared_ptr<SetBool::Response> response) {
    // ============================================
    // PASO 2: Atender la petición
    // ============================================
    // La response llega creada: se rellena y rclcpp la envía al volver.
    // Descomenta las siguientes líneas para el Paso 2:
    //
    // const std::string wanted = request->data ? "habilitado" : "deshabilitado";
    // if (request->data == enabled_) {
    //   response->success = false;
    //   response->message = "ya estaba " + wanted;
    // } else {
    //   enabled_ = request->data;
    //   response->success = true;
    //   response->message = wanted;
    // }
    // RCLCPP_INFO(get_logger(), "Petición data=%d: %s", request->data,
    //             response->message.c_str());
    (void)request;   // elimina esta línea al completar el Paso 2
    (void)response;  // elimina esta línea al completar el Paso 2
  }

  bool enabled_{false};
  rclcpp::Service<SetBool>::SharedPtr service_;
};

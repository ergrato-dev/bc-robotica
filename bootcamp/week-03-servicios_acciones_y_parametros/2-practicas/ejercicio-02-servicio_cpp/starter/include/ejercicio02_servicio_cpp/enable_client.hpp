// Ejercicio 02, Semana 03 — cliente del servicio robot/enable en rclcpp.
#pragma once

#include "rclcpp/rclcpp.hpp"
#include "std_srvs/srv/set_bool.hpp"

#include <chrono>
#include <memory>
#include <stdexcept>

class EnableClient : public rclcpp::Node {
 public:
  using SetBool = std_srvs::srv::SetBool;

  EnableClient() : Node("enable_client") {
    // ============================================
    // PASO 3: Crear el cliente
    // ============================================
    // Descomenta la siguiente línea para el Paso 3:
    //
    // client_ = create_client<SetBool>("robot/enable");
  }

  // Envía la petición sin bloquear; la response llega en el future.
  rclcpp::Client<SetBool>::SharedFuture send(bool enable) {
    // ============================================
    // PASO 4: Llamada asíncrona
    // ============================================
    // async_send_request devuelve enseguida; quien llame hace spin hasta que
    // el future esté listo.
    // Descomenta las siguientes líneas para el Paso 4:
    //
    // if (!client_->wait_for_service(std::chrono::seconds(2))) {
    //   throw std::runtime_error("el servicio robot/enable no está disponible");
    // }
    // auto request = std::make_shared<SetBool::Request>();
    // request->data = enable;
    // return client_->async_send_request(request).future.share();
    (void)enable;                                   // elimina esta línea al completar el Paso 4
    throw std::logic_error("completa el Paso 4");  // elimina esta línea al completar el Paso 4
  }

 private:
  rclcpp::Client<SetBool>::SharedPtr client_;
};

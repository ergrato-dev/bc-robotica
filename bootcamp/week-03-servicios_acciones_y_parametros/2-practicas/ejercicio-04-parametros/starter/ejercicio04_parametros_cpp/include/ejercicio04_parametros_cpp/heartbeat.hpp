// Ejercicio 04, Semana 03 — latido configurable con parámetros en rclcpp.
//
// Mismo nombre de nodo y mismos parámetros que la versión Python: el mismo
// config/heartbeat.yaml sirve para las dos.
#pragma once

#include "rcl_interfaces/msg/floating_point_range.hpp"
#include "rcl_interfaces/msg/parameter_descriptor.hpp"
#include "rclcpp/rclcpp.hpp"
#include "std_msgs/msg/string.hpp"

#include <chrono>
#include <string>
#include <vector>

class Heartbeat : public rclcpp::Node {
 public:
  Heartbeat() : Node("heartbeat") {
    publisher_ = create_publisher<std_msgs::msg::String>("robot/heartbeat", 10);

    // ============================================
    // PASO 1: Declarar los parámetros
    // ============================================
    // El descriptor es un mensaje: se rellena campo a campo. ROS2 hace
    // cumplir read_only y floating_point_range en cada set.
    // Descomenta las siguientes líneas para el Paso 1:
    //
    // rcl_interfaces::msg::ParameterDescriptor name_descriptor;
    // name_descriptor.description = "Nombre en cada latido";
    // name_descriptor.read_only = true;
    // declare_parameter<std::string>("robot_name", "robot", name_descriptor);
    //
    // rcl_interfaces::msg::FloatingPointRange range;
    // range.from_value = 0.1;
    // range.to_value = 5.0;
    // rcl_interfaces::msg::ParameterDescriptor period_descriptor;
    // period_descriptor.description = "Segundos entre latidos";
    // period_descriptor.floating_point_range.push_back(range);
    // declare_parameter<double>("period_s", 1.0, period_descriptor);

    // ============================================
    // PASO 2: Leer los parámetros y usarlos
    // ============================================
    // Descomenta las siguientes líneas para el Paso 2:
    //
    // robot_name_ = get_parameter("robot_name").as_string();
    // period_s_ = get_parameter("period_s").as_double();
    // restart_timer();

    // ============================================
    // PASO 3: Reaccionar a cambios en marcha
    // ============================================
    // Guarda el handle: si se destruye, rclcpp deja de llamar a la callback.
    // Descomenta las siguientes líneas para el Paso 3:
    //
    // post_set_handle_ = add_post_set_parameters_callback(
    //     [this](const std::vector<rclcpp::Parameter>& parameters) {
    //       for (const auto& parameter : parameters) {
    //         if (parameter.get_name() == "period_s") {
    //           period_s_ = parameter.as_double();
    //           restart_timer();
    //           RCLCPP_INFO(get_logger(), "Nuevo periodo: %.2f s", period_s_);
    //         }
    //       }
    //     });
  }

  const std::string& robot_name() const { return robot_name_; }
  double period_s() const { return period_s_; }

 private:
  // rclcpp no cambia el periodo de un timer existente: se crea otro y el
  // anterior se destruye al reasignar timer_.
  void restart_timer() {
    timer_ = create_wall_timer(std::chrono::duration<double>(period_s_), [this]() {
      std_msgs::msg::String msg;
      msg.data = robot_name_ + ": alive";
      publisher_->publish(msg);
    });
  }

  rclcpp::Publisher<std_msgs::msg::String>::SharedPtr publisher_;
  rclcpp::TimerBase::SharedPtr timer_;
  PostSetParametersCallbackHandle::SharedPtr post_set_handle_;
  std::string robot_name_;
  double period_s_{0.0};
};

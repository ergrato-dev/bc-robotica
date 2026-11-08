// Tests del Ejercicio 02. No los edites: pasan solos al completar los pasos.
#include "ament_index_cpp/get_resource.hpp"
#include "ejercicio02_componente_cpp/monitor.hpp"
#include "gtest/gtest.h"

#include <chrono>
#include <future>
#include <memory>
#include <string>
#include <thread>
#include <unistd.h>

using namespace std::chrono_literals;
using ejercicio02_componente_cpp::Monitor;

TEST(MonitorTest, UsaGruposPropios) {
  auto node = std::make_shared<Monitor>();
  ASSERT_NE(node->timer_group(), nullptr) << "falta crear el grupo del timer";
  ASSERT_NE(node->service_group(), nullptr) << "falta crear el grupo del servicio";
  EXPECT_NE(node->timer_group(), node->service_group());
}

TEST(MonitorTest, TimerSigueDuranteLaComprobacion) {
  auto node = std::make_shared<Monitor>();
  auto probe = std::make_shared<rclcpp::Node>("probe_monitor");
  auto client = probe->create_client<Monitor::Trigger>("robot/slow_check");
  // El test ya usa un executor multihilo: solo faltan los grupos del Paso 1.
  rclcpp::executors::MultiThreadedExecutor executor(rclcpp::ExecutorOptions(), 4);
  executor.add_node(node);
  executor.add_node(probe);
  std::thread spinner([&executor]() { executor.spin(); });

  ASSERT_TRUE(client->wait_for_service(2s));
  auto future = client->async_send_request(std::make_shared<Monitor::Trigger::Request>()).future;
  const bool answered = future.wait_for(3s) == std::future_status::ready;
  executor.cancel();
  spinner.join();

  ASSERT_TRUE(answered) << "el servicio no respondió en 3 segundos";
  const std::string message = future.get()->message;
  const int ticks = std::stoi(message.substr(message.rfind(':') + 1));
  // 0.5 s a 10 Hz son unos 5 ticks; 3 deja margen a una máquina lenta.
  EXPECT_GE(ticks, 3) << "el timer estuvo bloqueado: " << ticks << " ticks";
}

TEST(MonitorTest, SeRegistraComoComponente) {
  // rclcpp_components_register_node escribe este recurso en el índice de
  // ament; es lo que lee `ros2 component types`.
  std::string content;
  ASSERT_TRUE(
      ament_index_cpp::get_resource("rclcpp_components", "ejercicio02_componente_cpp", content))
      << "el paquete no registra ningún componente";
  EXPECT_NE(content.find("ejercicio02_componente_cpp::Monitor"), std::string::npos);
}

int main(int argc, char** argv) {
  // Dominio DDS propio por proceso: colcon test corre paquetes en paralelo
  // y así los nodos de otros tests no se mezclan con los de este.
  rclcpp::InitOptions options;
  options.set_domain_id(static_cast<size_t>(getpid() % 100 + 1));
  rclcpp::init(argc, argv, options);
  ::testing::InitGoogleTest(&argc, argv);
  int result = RUN_ALL_TESTS();
  rclcpp::shutdown();
  return result;
}

// Tests del Ejercicio 02. No los edites: pasan solos al completar los pasos.
#include "ejercicio02_servicio_cpp/enable_client.hpp"
#include "ejercicio02_servicio_cpp/enable_server.hpp"
#include "gtest/gtest.h"

#include <chrono>
#include <memory>
#include <unistd.h>

using namespace std::chrono_literals;
using std_srvs::srv::SetBool;

TEST(EnableServerTest, AnunciaElServicio) {
  auto node = std::make_shared<EnableServer>();
  const auto services = node->get_service_names_and_types();
  ASSERT_EQ(services.count("/robot/enable"), 1U) << "no existe /robot/enable";
  EXPECT_EQ(services.at("/robot/enable").at(0), "std_srvs/srv/SetBool");
}

TEST(EnableServerTest, CambiaEstadoUnaVez) {
  auto server = std::make_shared<EnableServer>();
  auto probe = std::make_shared<rclcpp::Node>("probe_enable");
  auto client = probe->create_client<SetBool>("robot/enable");
  rclcpp::executors::SingleThreadedExecutor executor;
  executor.add_node(server);
  executor.add_node(probe);
  ASSERT_TRUE(client->wait_for_service(2s));

  auto call = [&](bool data) {
    auto request = std::make_shared<SetBool::Request>();
    request->data = data;
    auto future = client->async_send_request(request).future.share();
    EXPECT_EQ(executor.spin_until_future_complete(future, 3s), rclcpp::FutureReturnCode::SUCCESS);
    return future.get();
  };

  auto first = call(true);
  EXPECT_TRUE(first->success);
  EXPECT_EQ(first->message, "habilitado");
  EXPECT_TRUE(server->enabled());
  auto again = call(true);
  EXPECT_FALSE(again->success);
  EXPECT_EQ(again->message, "ya estaba habilitado");
}

TEST(EnableClientTest, RecibeRespuesta) {
  auto server = std::make_shared<EnableServer>();
  auto client = std::make_shared<EnableClient>();
  rclcpp::executors::SingleThreadedExecutor executor;
  executor.add_node(server);
  executor.add_node(client);
  auto future = client->send(true);
  ASSERT_EQ(executor.spin_until_future_complete(future, 3s), rclcpp::FutureReturnCode::SUCCESS);
  EXPECT_TRUE(future.get()->success);
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

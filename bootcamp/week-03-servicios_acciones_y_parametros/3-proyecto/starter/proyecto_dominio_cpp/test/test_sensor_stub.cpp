// Tests mínimos del proyecto. Actualízalos cuando renombres topic, servicio y tipos.
#include "gtest/gtest.h"
#include "proyecto_dominio_cpp/sensor_stub.hpp"

#include <chrono>
#include <memory>
#include <string>
#include <thread>
#include <unistd.h>
#include <utility>

using namespace std::chrono_literals;
using proyecto_dominio_interfaces::msg::DomainState;
using proyecto_dominio_interfaces::srv::SetMode;

namespace {

std::string state_topic(const rclcpp::Node& node) {
  std::string found;
  for (const auto& [name, types] : node.get_topic_names_and_types()) {
    const std::string suffix = "/state";
    if (name.size() >= suffix.size() &&
        name.compare(name.size() - suffix.size(), suffix.size(), suffix) == 0) {
      found = name;
    }
  }
  return found;
}

}  // namespace

TEST(SensorStubTest, PublicaTipoPropio) {
  auto node = std::make_shared<SensorStub>();
  const auto topic = state_topic(*node);
  ASSERT_FALSE(topic.empty()) << "no hay ningún topic */state";
  auto types = node->get_topic_names_and_types().at(topic);
  // Si renombraste DomainState, actualiza este valor.
  EXPECT_EQ(types.at(0), "proyecto_dominio_interfaces/msg/DomainState");
}

TEST(SensorStubTest, EstadoLlevaHeader) {
  auto node = std::make_shared<SensorStub>();
  auto probe = std::make_shared<rclcpp::Node>("probe_state");
  DomainState received;
  bool got = false;
  auto sub = probe->create_subscription<DomainState>(state_topic(*node), state_qos(),
                                                     [&](const DomainState& msg) {
                                                       received = msg;
                                                       got = true;
                                                     });

  auto deadline = std::chrono::steady_clock::now() + 3s;
  while (std::chrono::steady_clock::now() < deadline && !got) {
    rclcpp::spin_some(node);
    rclcpp::spin_some(probe);
    std::this_thread::sleep_for(20ms);
  }
  ASSERT_TRUE(got) << "no llegó ningún estado en 3 segundos";
  EXPECT_FALSE(received.header.frame_id.empty());
  EXPECT_GT(received.header.stamp.sec, 0);
}

TEST(SensorStubTest, ServicioCambiaModoYRechazaDesconocido) {
  auto node = std::make_shared<SensorStub>();
  auto probe = std::make_shared<rclcpp::Node>("probe_set_mode");
  std::string service;
  for (const auto& [name, types] : node->get_service_names_and_types()) {
    if (name.size() >= 9 && name.compare(name.size() - 9, 9, "/set_mode") == 0) {
      service = name;
    }
  }
  ASSERT_FALSE(service.empty()) << "no hay ningún servicio */set_mode";
  auto client = probe->create_client<SetMode>(service);
  ASSERT_TRUE(client->wait_for_service(2s));
  rclcpp::executors::SingleThreadedExecutor executor;
  executor.add_node(node);
  executor.add_node(probe);
  for (const auto& [mode, accepted] : {std::pair<uint8_t, bool>{DomainState::MODE_IDLE, true},
                                       std::pair<uint8_t, bool>{99, false}}) {
    auto request = std::make_shared<SetMode::Request>();
    request->mode = mode;
    auto future = client->async_send_request(request).future.share();
    ASSERT_EQ(executor.spin_until_future_complete(future, 3s), rclcpp::FutureReturnCode::SUCCESS);
    EXPECT_EQ(future.get()->accepted, accepted);
  }
}

TEST(SensorStubTest, PeriodoRespetaSuRango) {
  auto node = std::make_shared<SensorStub>();
  EXPECT_FALSE(node->set_parameter(rclcpp::Parameter("publish_period_s", 0.0)).successful);
  EXPECT_TRUE(node->set_parameter(rclcpp::Parameter("publish_period_s", 0.5)).successful);
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

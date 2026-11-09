// Tests mínimos del proyecto. Actualízalos cuando renombres topic, servicio y tipos.
#include "gtest/gtest.h"
#include "proyecto_dominio_cpp/sensor_stub.hpp"

#include <chrono>
#include <memory>
#include <string>
#include <thread>
#include <unistd.h>
#include <utility>
#include <vector>

using namespace std::chrono_literals;
using proyecto_dominio_cpp::SensorStub;
using proyecto_dominio_interfaces::msg::DomainState;
using proyecto_dominio_interfaces::srv::SetMode;

namespace {

bool ends_with(const std::string& text, const std::string& suffix) {
  return text.size() >= suffix.size() &&
         text.compare(text.size() - suffix.size(), suffix.size(), suffix) == 0;
}

std::string state_topic(SensorStub& node) {
  std::string found;
  for (const auto& [name, types] : node.get_topic_names_and_types()) {
    if (ends_with(name, "/state")) {
      found = name;
    }
  }
  return found;
}

std::string set_mode_service(SensorStub& node) {
  std::string found;
  for (const auto& [name, types] : node.get_service_names_and_types()) {
    if (ends_with(name, "/set_mode")) {
      found = name;
    }
  }
  return found;
}

std::vector<DomainState> received_during(const std::shared_ptr<SensorStub>& node,
                                         std::chrono::milliseconds duration) {
  auto probe = std::make_shared<rclcpp::Node>("probe_state");
  std::vector<DomainState> received;
  auto sub = probe->create_subscription<DomainState>(
      state_topic(*node), proyecto_dominio_cpp::state_qos(),
      [&](const DomainState& msg) { received.push_back(msg); });
  const auto deadline = std::chrono::steady_clock::now() + duration;
  while (std::chrono::steady_clock::now() < deadline) {
    rclcpp::spin_some(node->get_node_base_interface());
    rclcpp::spin_some(probe);
    std::this_thread::sleep_for(20ms);
  }
  return received;
}

}  // namespace

TEST(SensorStubTest, PublicaTipoPropio) {
  auto node = std::make_shared<SensorStub>();
  node->configure();
  const auto topic = state_topic(*node);
  ASSERT_FALSE(topic.empty()) << "no hay ningún topic */state";
  auto types = node->get_topic_names_and_types().at(topic);
  // Si renombraste DomainState, actualiza este valor.
  EXPECT_EQ(types.at(0), "proyecto_dominio_interfaces/msg/DomainState");
}

TEST(SensorStubTest, PublicaSoloEnActiveYConHeader) {
  auto node = std::make_shared<SensorStub>();
  node->configure();
  EXPECT_TRUE(received_during(node, 1500ms).empty()) << "publica sin estar activo";
  node->activate();
  const auto received = received_during(node, 3000ms);
  ASSERT_FALSE(received.empty()) << "activo, pero no llegó ningún estado en 3 segundos";
  EXPECT_FALSE(received.front().header.frame_id.empty());
  EXPECT_GT(received.front().header.stamp.sec, 0);
}

TEST(SensorStubTest, ServicioCambiaModoYRechazaDesconocido) {
  auto node = std::make_shared<SensorStub>();
  EXPECT_TRUE(set_mode_service(*node).empty()) << "el servicio existe antes de configure";
  node->configure();
  const auto service = set_mode_service(*node);
  ASSERT_FALSE(service.empty()) << "no hay ningún servicio */set_mode tras configure";
  auto probe = std::make_shared<rclcpp::Node>("probe_set_mode");
  auto client = probe->create_client<SetMode>(service);
  ASSERT_TRUE(client->wait_for_service(2s));
  rclcpp::executors::SingleThreadedExecutor executor;
  executor.add_node(node->get_node_base_interface());
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
  node->configure();
  node->activate();
  EXPECT_TRUE(node->set_parameter(rclcpp::Parameter("publish_period_s", 0.5)).successful);
  EXPECT_TRUE(node->has_timer());
}

TEST(SensorStubTest, CleanupDejaElNodoComoAlArrancar) {
  auto node = std::make_shared<SensorStub>();
  node->configure();
  node->cleanup();
  const auto graph = node->get_node_graph_interface();
  for (const auto& [name, types] :
       graph->get_publisher_names_and_types_by_node("sensor_stub", "/")) {
    EXPECT_FALSE(ends_with(name, "/state")) << "cleanup no destruyó el publisher";
  }
  EXPECT_TRUE(set_mode_service(*node).empty()) << "cleanup no destruyó el servicio";
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

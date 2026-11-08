// Tests mínimos del proyecto. Actualízalos cuando renombres topic y tipo.
#include "gtest/gtest.h"
#include "proyecto_dominio_cpp/sensor_stub.hpp"

#include <chrono>
#include <memory>
#include <string>
#include <thread>
#include <unistd.h>

using namespace std::chrono_literals;
using proyecto_dominio_interfaces::msg::DomainState;

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

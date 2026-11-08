// Tests del Ejercicio 04. No los edites: pasan solos al completar los pasos de
// range_driver.hpp. configure(), activate()... son las mismas transiciones que
// pide `ros2 lifecycle set`, llamadas sin pasar por el servicio.
#include "ejercicio04_lifecycle_cpp/range_driver.hpp"
#include "gtest/gtest.h"
#include "lifecycle_msgs/msg/state.hpp"

#include <chrono>
#include <memory>
#include <thread>
#include <unistd.h>
#include <vector>

using namespace std::chrono_literals;
using ejercicio04_lifecycle_cpp::RangeDriver;
using lifecycle_msgs::msg::State;

namespace {

const char* const kTopic = "/robot/range_m";

std::vector<double> received_during(const std::shared_ptr<RangeDriver>& node,
                                    std::chrono::milliseconds duration) {
  auto probe = std::make_shared<rclcpp::Node>("probe_range");
  std::vector<double> received;
  auto sub = probe->create_subscription<std_msgs::msg::Float64>(
      kTopic, 10, [&](const std_msgs::msg::Float64& msg) { received.push_back(msg.data); });
  const auto deadline = std::chrono::steady_clock::now() + duration;
  while (std::chrono::steady_clock::now() < deadline) {
    rclcpp::spin_some(node->get_node_base_interface());
    rclcpp::spin_some(probe);
    std::this_thread::sleep_for(20ms);
  }
  return received;
}

}  // namespace

TEST(RangeDriverTest, ConfigureCreaElPublisher) {
  auto node = std::make_shared<RangeDriver>();
  EXPECT_EQ(node->count_publishers(kTopic), 0U);
  EXPECT_EQ(node->configure().id(), State::PRIMARY_STATE_INACTIVE);
  EXPECT_EQ(node->count_publishers(kTopic), 1U) << "configure no creó el publisher";
}

TEST(RangeDriverTest, ConfigureFallaConRateInvalido) {
  auto node = std::make_shared<RangeDriver>(
      rclcpp::NodeOptions().parameter_overrides({rclcpp::Parameter("rate_hz", 0.0)}));
  EXPECT_EQ(node->configure().id(), State::PRIMARY_STATE_UNCONFIGURED);
  EXPECT_EQ(node->count_publishers(kTopic), 0U);
}

TEST(RangeDriverTest, PublicaSoloEnActive) {
  auto node = std::make_shared<RangeDriver>();
  node->configure();
  EXPECT_TRUE(received_during(node, 1000ms).empty()) << "publica sin estar activo";
  EXPECT_EQ(node->activate().id(), State::PRIMARY_STATE_ACTIVE);
  const auto received = received_during(node, 2000ms);
  ASSERT_FALSE(received.empty()) << "activo, pero no llegó ninguna lectura en 2 segundos";
  EXPECT_GE(received.front(), 0.5);
  EXPECT_LE(received.front(), 2.5);
  EXPECT_EQ(node->deactivate().id(), State::PRIMARY_STATE_INACTIVE);
  EXPECT_FALSE(node->has_timer()) << "deactivate no destruyó el timer";
}

TEST(RangeDriverTest, CleanupLiberaElPublisher) {
  auto node = std::make_shared<RangeDriver>();
  node->configure();
  ASSERT_EQ(node->count_publishers(kTopic), 1U) << "configure no creó el publisher";
  EXPECT_EQ(node->cleanup().id(), State::PRIMARY_STATE_UNCONFIGURED);
  EXPECT_EQ(node->count_publishers(kTopic), 0U) << "cleanup no destruyó el publisher";
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

// Tests del Ejercicio 04 (parte C++). No los edites: pasan solos al completar
// los pasos de heartbeat.hpp.
#include "ejercicio04_parametros_cpp/heartbeat.hpp"
#include "gtest/gtest.h"

#include <chrono>
#include <memory>
#include <thread>
#include <unistd.h>

using namespace std::chrono_literals;

TEST(HeartbeatTest, DeclaraParametrosConDescriptor) {
  auto node = std::make_shared<Heartbeat>();
  ASSERT_TRUE(node->has_parameter("robot_name")) << "falta declarar robot_name";
  ASSERT_TRUE(node->has_parameter("period_s")) << "falta declarar period_s";
  EXPECT_EQ(node->get_parameter("robot_name").as_string(), "robot");
  EXPECT_DOUBLE_EQ(node->get_parameter("period_s").as_double(), 1.0);
  EXPECT_TRUE(node->describe_parameter("robot_name").read_only);
}

TEST(HeartbeatTest, RechazaValoresInvalidos) {
  auto node = std::make_shared<Heartbeat>();
  ASSERT_TRUE(node->has_parameter("period_s"));
  EXPECT_FALSE(node->set_parameter(rclcpp::Parameter("period_s", 10.0)).successful);
  EXPECT_FALSE(node->set_parameter(rclcpp::Parameter("robot_name", "otro")).successful);
}

TEST(HeartbeatTest, PublicaLatidoConNombre) {
  auto node = std::make_shared<Heartbeat>();
  auto probe = std::make_shared<rclcpp::Node>("probe_heartbeat");
  std::string received;
  auto sub = probe->create_subscription<std_msgs::msg::String>(
      "robot/heartbeat", 10, [&](const std_msgs::msg::String& msg) { received = msg.data; });
  const auto deadline = std::chrono::steady_clock::now() + 3s;
  while (std::chrono::steady_clock::now() < deadline && received.empty()) {
    rclcpp::spin_some(node);
    rclcpp::spin_some(probe);
    std::this_thread::sleep_for(20ms);
  }
  EXPECT_EQ(received, "robot: alive");
}

TEST(HeartbeatTest, CambioDePeriodoEnMarcha) {
  auto node = std::make_shared<Heartbeat>();
  ASSERT_TRUE(node->has_parameter("period_s"));
  EXPECT_TRUE(node->set_parameter(rclcpp::Parameter("period_s", 0.2)).successful);
  EXPECT_DOUBLE_EQ(node->period_s(), 0.2);
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

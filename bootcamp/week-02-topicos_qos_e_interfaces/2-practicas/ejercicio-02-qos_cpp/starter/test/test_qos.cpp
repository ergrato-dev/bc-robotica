// Tests del Ejercicio 02. No los edites: pasan solos al completar los pasos
// de los headers en include/ejercicio02_qos_cpp/.
#include "ejercicio02_qos_cpp/qos_listener.hpp"
#include "ejercicio02_qos_cpp/range_publisher.hpp"
#include "ejercicio02_qos_cpp/status_publisher.hpp"
#include "gtest/gtest.h"

#include <chrono>
#include <memory>
#include <string>
#include <thread>
#include <unistd.h>
#include <vector>

using namespace std::chrono_literals;

namespace {

// spin_some repetido sobre varios nodos hasta que condition() sea true o se
// agote el timeout. Equivalente al _spin_until del test Python.
template <typename Condition>
bool spin_until(const std::vector<rclcpp::Node::SharedPtr>& nodes, Condition condition,
                std::chrono::milliseconds timeout = 3000ms) {
  auto deadline = std::chrono::steady_clock::now() + timeout;
  while (std::chrono::steady_clock::now() < deadline) {
    for (const auto& n : nodes) {
      rclcpp::spin_some(n);
    }
    if (condition()) {
      return true;
    }
    std::this_thread::sleep_for(20ms);
  }
  return false;
}

}  // namespace

TEST(RangePublisherTest, EsBestEffort) {
  // Paso 1: /sensor/range existe y se ofrece con BEST_EFFORT.
  auto node = std::make_shared<RangePublisher>();
  auto infos = node->get_publishers_info_by_topic("/sensor/range");
  ASSERT_EQ(infos.size(), 1u) << "no hay publisher en /sensor/range";
  EXPECT_EQ(infos[0].qos_profile().reliability(), rclcpp::ReliabilityPolicy::BestEffort);
}

TEST(RangePublisherTest, LlevaHeader) {
  // Paso 2: cada Range lleva stamp y frame_id.
  auto pub_node = std::make_shared<RangePublisher>();
  auto probe = std::make_shared<rclcpp::Node>("probe_range_header");
  std::vector<sensor_msgs::msg::Range> received;
  auto sub = probe->create_subscription<sensor_msgs::msg::Range>(
      "sensor/range", rclcpp::SensorDataQoS(),
      [&received](const sensor_msgs::msg::Range& msg) { received.push_back(msg); });

  ASSERT_TRUE(spin_until({pub_node, probe}, [&received]() { return !received.empty(); }))
      << "no llegó ningún Range en 3 segundos";
  EXPECT_EQ(received[0].header.frame_id, "range_sensor");
  EXPECT_GT(received[0].header.stamp.sec, 0) << "header.stamp sigue a cero";
}

TEST(StatusPublisherTest, LlegaASuscriptorTardio) {
  // Paso 3: un subscriber que arranca después recibe el "ready" guardado.
  auto pub_node = std::make_shared<StatusPublisher>();
  auto infos = pub_node->get_publishers_info_by_topic("/robot/status");
  ASSERT_EQ(infos.size(), 1u) << "no hay publisher en /robot/status";
  EXPECT_EQ(infos[0].qos_profile().durability(), rclcpp::DurabilityPolicy::TransientLocal);

  // Deja pasar tiempo para que el publish del constructor ya sea "pasado".
  spin_until({pub_node}, []() { return false; }, 500ms);

  auto probe = std::make_shared<rclcpp::Node>("probe_status_tardio");
  std::string received;
  auto sub = probe->create_subscription<std_msgs::msg::String>(
      "robot/status", latched_qos(),
      [&received](const std_msgs::msg::String& msg) { received = msg.data; });

  ASSERT_TRUE(spin_until({pub_node, probe}, [&received]() { return !received.empty(); }))
      << "el subscriber tardío no recibió el estado guardado";
  EXPECT_EQ(received, "ready");
}

TEST(QosListenerTest, RecibeAmbosTopics) {
  // Paso 4: el listener recibe Range (BEST_EFFORT) y el estado latched.
  auto range_node = std::make_shared<RangePublisher>();
  auto status_node = std::make_shared<StatusPublisher>();
  auto listener = std::make_shared<QosListener>();

  bool ok = spin_until({range_node, status_node, listener}, [&listener]() {
    return listener->range_count() >= 2 && listener->status() == "ready";
  });
  EXPECT_TRUE(ok) << "range_count=" << listener->range_count() << ", status='" << listener->status()
                  << "': revisa el QoS de cada subscripción";
  EXPECT_EQ(listener->last_frame_id(), "range_sensor");
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

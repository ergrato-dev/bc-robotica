// Tests del Ejercicio 02. No los edites: pasan solos al completar los pasos
// de los headers en include/ejercicio02_pubsub_cpp/.
#include <chrono>
#include <memory>
#include <thread>
#include <vector>

#include "gtest/gtest.h"
#include "ejercicio02_pubsub_cpp/sensor_publisher.hpp"
#include "ejercicio02_pubsub_cpp/sensor_listener.hpp"

using namespace std::chrono_literals;

namespace {

// Hace spin_some repetido sobre varios nodos hasta que condition() sea true o
// se agote el timeout. Equivalente al _spin_until del test Python.
template <typename Condition>
bool spin_until(const std::vector<rclcpp::Node::SharedPtr> &nodes, Condition condition,
                 std::chrono::milliseconds timeout = 3000ms) {
  auto deadline = std::chrono::steady_clock::now() + timeout;
  while (std::chrono::steady_clock::now() < deadline) {
    for (const auto &n : nodes) {
      rclcpp::spin_some(n);
    }
    if (condition()) return true;
    std::this_thread::sleep_for(20ms);
  }
  return false;
}

}  // namespace

TEST(PublisherTest, PublisherExiste) {
  // Paso 1: el nodo debe exponer un publisher sobre /sensor/state.
  auto node = std::make_shared<SensorPublisher>();
  auto topics = node->get_topic_names_and_types();
  ASSERT_TRUE(topics.count("/sensor/state") == 1);
  auto types = topics.at("/sensor/state");
  ASSERT_FALSE(types.empty());
  EXPECT_EQ(types[0], "std_msgs/msg/String");
}

TEST(PublisherTest, PublicaMensajes) {
  // Paso 2: el timer debe disparar al menos un mensaje en 3 segundos.
  auto pub_node = std::make_shared<SensorPublisher>();
  auto probe = std::make_shared<rclcpp::Node>("probe_publica_mensajes");

  int received = 0;
  auto sub = probe->create_subscription<std_msgs::msg::String>(
      "sensor/state", 10, [&received](const std_msgs::msg::String &) { received++; });

  bool ok = spin_until({pub_node, probe}, [&received]() { return received >= 1; });
  EXPECT_TRUE(ok) << "no se recibió ningún mensaje en /sensor/state en 3 segundos";
}

TEST(ListenerTest, RecibeMensajesDelPublisher) {
  // Paso 3: el listener debe incrementar received_count al llegar mensajes.
  auto pub_node = std::make_shared<SensorPublisher>();
  auto sub_node = std::make_shared<SensorListener>();

  bool ok = spin_until({pub_node, sub_node},
                        [&sub_node]() { return sub_node->received_count() >= 2; });
  EXPECT_TRUE(ok) << "el listener no recibió al menos 2 mensajes en 3 segundos";
  EXPECT_NE(sub_node->last_message().find("lectura #"), std::string::npos);
}

int main(int argc, char **argv) {
  rclcpp::init(argc, argv);
  ::testing::InitGoogleTest(&argc, argv);
  int result = RUN_ALL_TESTS();
  rclcpp::shutdown();
  return result;
}

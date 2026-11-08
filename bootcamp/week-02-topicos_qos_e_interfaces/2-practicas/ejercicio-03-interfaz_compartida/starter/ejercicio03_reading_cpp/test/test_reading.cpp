// Tests del listener C++ del Ejercicio 03. No los edites.
#include "ejercicio03_reading_cpp/reading_listener.hpp"
#include "gtest/gtest.h"

#include <chrono>
#include <memory>
#include <thread>

using namespace std::chrono_literals;
using ejercicio03_interfaces::msg::SensorReading;

TEST(ReadingListenerTest, RecibeYClasificaLecturas) {
  // Paso 4: el listener cuenta las lecturas y separa las que no son STATUS_OK.
  auto listener = std::make_shared<ReadingListener>();
  auto probe = std::make_shared<rclcpp::Node>("probe_reading_pub");
  auto pub = probe->create_publisher<SensorReading>("sensor/reading", 10);

  auto deadline = std::chrono::steady_clock::now() + 3s;
  int sent = 0;
  while (std::chrono::steady_clock::now() < deadline && listener->received_count() < 2) {
    SensorReading msg;
    msg.sensor_id = "test";
    msg.value = 9.0;
    // Alterna OK / WARN para comprobar que el listener las distingue.
    msg.status = (sent % 2 == 0) ? SensorReading::STATUS_OK : SensorReading::STATUS_WARN;
    pub->publish(msg);
    sent++;
    rclcpp::spin_some(listener);
    std::this_thread::sleep_for(50ms);
  }
  ASSERT_GE(listener->received_count(), 2) << "el listener no recibió 2 lecturas en 3 s";
  EXPECT_GE(listener->warning_count(), 1);
  EXPECT_EQ(listener->last_sensor_id(), "test");
}

int main(int argc, char** argv) {
  rclcpp::init(argc, argv);
  ::testing::InitGoogleTest(&argc, argv);
  int result = RUN_ALL_TESTS();
  rclcpp::shutdown();
  return result;
}

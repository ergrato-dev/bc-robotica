// Tests del Ejercicio 03 (parte C++). No los edites: pasan solos al completar
// los pasos de move_client.hpp. El server de prueba es un doble mínimo en C++
// para que el test no dependa del paquete Python.
#include "ejercicio03_accion_cpp/move_client.hpp"
#include "gtest/gtest.h"

#include <chrono>
#include <memory>
#include <unistd.h>

using namespace std::chrono_literals;
using MoveDistance = ejercicio03_interfaces::action::MoveDistance;
using ServerGoalHandle = rclcpp_action::ServerGoalHandle<MoveDistance>;

namespace {

// Acepta distancias positivas y completa el goal en 3 pasos de 50 ms.
class FakeMoveServer : public rclcpp::Node {
 public:
  FakeMoveServer() : Node("fake_move_server") {
    server_ = rclcpp_action::create_server<MoveDistance>(
        this, "robot/move_distance",
        [](const rclcpp_action::GoalUUID&, std::shared_ptr<const MoveDistance::Goal> goal) {
          return goal->distance_m > 0.0 ? rclcpp_action::GoalResponse::ACCEPT_AND_EXECUTE
                                        : rclcpp_action::GoalResponse::REJECT;
        },
        [](const std::shared_ptr<ServerGoalHandle>) {
          return rclcpp_action::CancelResponse::ACCEPT;
        },
        [this](const std::shared_ptr<ServerGoalHandle> handle) { active_ = handle; });
    timer_ = create_wall_timer(50ms, [this]() { step(); });
  }

 private:
  void step() {
    if (!active_) {
      return;
    }
    auto feedback = std::make_shared<MoveDistance::Feedback>();
    feedback->remaining_m = active_->get_goal()->distance_m * (3 - ++steps_) / 3.0;
    active_->publish_feedback(feedback);
    if (steps_ == 3) {
      auto result = std::make_shared<MoveDistance::Result>();
      result->traveled_m = active_->get_goal()->distance_m;
      active_->succeed(result);
      active_.reset();
    }
  }

  rclcpp_action::Server<MoveDistance>::SharedPtr server_;
  rclcpp::TimerBase::SharedPtr timer_;
  std::shared_ptr<ServerGoalHandle> active_;
  int steps_{0};
};

void spin_until_done(rclcpp::Executor& executor, const MoveClient& client) {
  const auto deadline = std::chrono::steady_clock::now() + 5s;
  while (!client.done() && std::chrono::steady_clock::now() < deadline) {
    executor.spin_once(20ms);
  }
}

}  // namespace

TEST(MoveClientTest, RecibeFeedbackYResultado) {
  auto server = std::make_shared<FakeMoveServer>();
  auto client = std::make_shared<MoveClient>();
  rclcpp::executors::SingleThreadedExecutor executor;
  executor.add_node(server);
  executor.add_node(client);
  client->send(1.5);
  spin_until_done(executor, *client);
  ASSERT_TRUE(client->done()) << "no llegó el resultado en 5 segundos";
  EXPECT_TRUE(client->accepted());
  EXPECT_EQ(client->code(), rclcpp_action::ResultCode::SUCCEEDED);
  EXPECT_DOUBLE_EQ(client->traveled_m(), 1.5);
  EXPECT_GE(client->feedback_count(), 1);
}

TEST(MoveClientTest, RechazoTerminaSinResultado) {
  auto server = std::make_shared<FakeMoveServer>();
  auto client = std::make_shared<MoveClient>();
  rclcpp::executors::SingleThreadedExecutor executor;
  executor.add_node(server);
  executor.add_node(client);
  client->send(-1.0);
  spin_until_done(executor, *client);
  ASSERT_TRUE(client->done());
  EXPECT_FALSE(client->accepted());
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

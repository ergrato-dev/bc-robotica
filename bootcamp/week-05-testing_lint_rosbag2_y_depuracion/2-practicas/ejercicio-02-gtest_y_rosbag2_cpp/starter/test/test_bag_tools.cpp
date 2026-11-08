// Paso 2 — read_ranges contra una bag escrita por el propio test, y el filtro
// aplicado a lo que se reproduce de ella. No los edites: pasan solos al
// completar el Paso 2.
#include "ejercicio02_gtest_rosbag2_cpp/bag_tools.hpp"
#include "ejercicio02_gtest_rosbag2_cpp/filtering.hpp"
#include "gtest/gtest.h"
#include "rclcpp/time.hpp"
#include "rosbag2_cpp/writer.hpp"
#include "std_msgs/msg/float64.hpp"

#include <filesystem>
#include <string>
#include <vector>

using ejercicio02_gtest_rosbag2_cpp::filter_range;
using ejercicio02_gtest_rosbag2_cpp::read_ranges;

namespace {

const std::string kRawTopic = "/robot/range_raw_m";

// Escribe una bag nueva (MCAP, el formato por defecto) con `values` en
// kRawTopic y un mensaje de ruido en otro topic.
std::string write_bag(const std::string& name, const std::vector<double>& values) {
  const auto uri = std::filesystem::temp_directory_path() / name;
  std::filesystem::remove_all(uri);
  rosbag2_cpp::Writer writer;
  writer.open(uri.string());
  std_msgs::msg::Float64 msg;
  msg.data = 100.0;
  writer.write(msg, "/otro_topic", rclcpp::Time(0));
  for (std::size_t i = 0; i < values.size(); ++i) {
    msg.data = values[i];
    writer.write(msg, kRawTopic, rclcpp::Time(static_cast<int64_t>(i + 1) * 100'000'000));
  }
  return uri.string();  // el destructor del writer cierra el archivo
}

}  // namespace

TEST(BagToolsTest, LeeSoloElTopicPedidoEnOrden) {
  const auto uri = write_bag("ej02_bag_orden", {1.5, 9.9, 0.0, 2.0});
  const std::vector<double> expected{1.5, 9.9, 0.0, 2.0};
  EXPECT_EQ(read_ranges(uri, kRawTopic), expected);
}

TEST(BagToolsTest, FiltroReproducidoSinPicos) {
  // Lecturas como las del range_sim del Ejercicio 01: un reflejo y un eco
  // perdido entre lecturas buenas de ~1.5 m.
  const auto uri = write_bag("ej02_bag_filtro", {1.4, 1.5, 9.9, 1.6, 1.5, 0.0, 1.4, 1.5});
  const auto raw = read_ranges(uri, kRawTopic);
  ASSERT_EQ(raw.size(), 8u);
  // Misma ventana deslizante de 5 lecturas que usa el nodo range_filter.
  for (std::size_t end = 1; end <= raw.size(); ++end) {
    const std::size_t begin = end > 5 ? end - 5 : 0;
    const double value = filter_range({raw.begin() + begin, raw.begin() + end}, 0.05, 4.0);
    EXPECT_GT(value, 1.0) << "tras " << end << " lecturas";
    EXPECT_LT(value, 2.0) << "tras " << end << " lecturas";
  }
}

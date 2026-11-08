#include "ejercicio02_gtest_rosbag2_cpp/bag_tools.hpp"

#include "rosbag2_cpp/reader.hpp"
#include "rosbag2_storage/storage_filter.hpp"
#include "std_msgs/msg/float64.hpp"

namespace ejercicio02_gtest_rosbag2_cpp {

std::vector<double> read_ranges(const std::string& bag_uri, const std::string& topic) {
  // ============================================
  // PASO 2: Leer una bag con rosbag2_cpp
  // ============================================
  // Reader abre la bag (MCAP o SQLite: lo detecta solo). El filtro hace que
  // solo entregue mensajes de `topic`, y read_next<Float64>() deserializa
  // cada uno al tipo de mensaje de ROS.
  // Descomenta las siguientes líneas para el Paso 2:
  //
  // rosbag2_cpp::Reader reader;
  // reader.open(bag_uri);
  // rosbag2_storage::StorageFilter filter;
  // filter.topics = {topic};
  // reader.set_filter(filter);
  // std::vector<double> values;
  // while (reader.has_next()) {
  //   values.push_back(reader.read_next<std_msgs::msg::Float64>().data);
  // }
  // return values;
  (void)bag_uri;  // elimina esta línea al completar el Paso 2
  (void)topic;    // elimina esta línea al completar el Paso 2
  return {};      // elimina esta línea al completar el Paso 2
}

}  // namespace ejercicio02_gtest_rosbag2_cpp

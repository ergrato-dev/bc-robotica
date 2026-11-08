#pragma once

#include <string>
#include <vector>

namespace ejercicio02_gtest_rosbag2_cpp {

// Devuelve, en orden de tiempo, los valores std_msgs/msg/Float64 de `topic`
// grabados en la bag de la carpeta `bag_uri`.
std::vector<double> read_ranges(const std::string& bag_uri, const std::string& topic);

}  // namespace ejercicio02_gtest_rosbag2_cpp

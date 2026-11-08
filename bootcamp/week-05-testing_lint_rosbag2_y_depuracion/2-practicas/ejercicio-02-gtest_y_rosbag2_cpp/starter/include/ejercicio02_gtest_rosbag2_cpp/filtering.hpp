// Lógica pura del filtro de distancia, sin nada de ROS: se prueba con gtest
// en milisegundos, sin arrancar nodos.
#pragma once

#include <algorithm>
#include <stdexcept>
#include <vector>

namespace ejercicio02_gtest_rosbag2_cpp {

// Mediana de las últimas lecturas, recortada al rango que mide el sensor.
// Igual que statistics.median en Python: con un número par de lecturas, media
// de las dos centrales. La ventana se recibe por copia porque hay que ordenarla.
inline double filter_range(std::vector<double> window, double min_m, double max_m) {
  if (window.empty()) {
    throw std::invalid_argument("la ventana de lecturas está vacía");
  }
  std::sort(window.begin(), window.end());
  const auto middle = window.size() / 2;
  const double median =
      window.size() % 2 == 1 ? window[middle] : (window[middle - 1] + window[middle]) / 2.0;
  return std::clamp(median, min_m, max_m);
}

}  // namespace ejercicio02_gtest_rosbag2_cpp

// Paso 1 — tests unitarios de filter_range con gtest. Sin ROS: puro C++.

// ============================================
// PASO 1: Tests unitarios
// ============================================
// Cada TEST(Grupo, Nombre) es un test. EXPECT_* anota el fallo y sigue;
// ASSERT_* corta el test en ese punto. Sin main(): ament_add_gtest enlaza el
// de gtest, que ejecuta todos los TEST del archivo.
// Descomenta las siguientes líneas para el Paso 1:
//
// #include "ejercicio02_gtest_rosbag2_cpp/filtering.hpp"
// #include "gtest/gtest.h"
//
// #include <stdexcept>
//
// using ejercicio02_gtest_rosbag2_cpp::filter_range;
//
// TEST(FilterRangeTest, MedianaIgnoraUnReflejo) {
//   EXPECT_DOUBLE_EQ(filter_range({1.0, 1.1, 9.9, 1.2, 1.0}, 0.05, 4.0), 1.1);
// }
//
// TEST(FilterRangeTest, RecortaAlRangoDelSensor) {
//   EXPECT_DOUBLE_EQ(filter_range({5.0, 6.0, 7.0}, 0.05, 4.0), 4.0);
//   EXPECT_DOUBLE_EQ(filter_range({0.0, 0.01, 0.02}, 0.05, 4.0), 0.05);
// }
//
// TEST(FilterRangeTest, VentanaParPromediaLasDosCentrales) {
//   EXPECT_DOUBLE_EQ(filter_range({1.0, 2.0, 3.0, 4.0}, 0.05, 4.0), 2.5);
// }
//
// TEST(FilterRangeTest, VentanaVaciaEsUnError) {
//   EXPECT_THROW(filter_range({}, 0.05, 4.0), std::invalid_argument);
// }

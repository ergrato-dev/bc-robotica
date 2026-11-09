// La ruta simulada: los mismos casos que test_route.py.
#include "gtest/gtest.h"
#include "proyecto_dominio_cpp/route.hpp"

#include <cmath>

using proyecto_dominio_cpp::route_pose;

TEST(RoutePose, ALaIdaAvanzaMirandoHaciaDelante) {
  const auto pose = route_pose(3.0, 10.0);
  EXPECT_DOUBLE_EQ(pose.x_m, 3.0);
  EXPECT_DOUBLE_EQ(pose.yaw_rad, 0.0);
}

TEST(RoutePose, ALaVueltaRetrocedeMirandoHaciaAtras) {
  const auto pose = route_pose(13.0, 10.0);
  EXPECT_DOUBLE_EQ(pose.x_m, 7.0);
  EXPECT_DOUBLE_EQ(pose.yaw_rad, M_PI);
}

TEST(RoutePose, NuncaSaleDeLaRecta) {
  for (const double distance : {0.0, 4.2, 9.99, 10.0, 17.5, 123.4}) {
    const auto pose = route_pose(distance, 10.0);
    EXPECT_GE(pose.x_m, 0.0) << distance;
    EXPECT_LE(pose.x_m, 10.0) << distance;
  }
}

cmake_minimum_required(VERSION 3.28)
project(proyecto_dominio_cpp)

if(NOT CMAKE_CXX_STANDARD)
  set(CMAKE_CXX_STANDARD 17)
  set(CMAKE_CXX_STANDARD_REQUIRED ON)
endif()
if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic -Werror)
endif()

find_package(ament_cmake REQUIRED)
find_package(rclcpp REQUIRED)
find_package(std_msgs REQUIRED)

add_executable(sensor_stub src/sensor_stub.cpp)
target_compile_features(sensor_stub PUBLIC cxx_std_17)
ament_target_dependencies(sensor_stub rclcpp std_msgs)

install(TARGETS sensor_stub DESTINATION lib/${PROJECT_NAME})

ament_package()

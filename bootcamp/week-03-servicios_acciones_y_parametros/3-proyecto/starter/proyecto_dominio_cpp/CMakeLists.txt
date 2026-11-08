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
find_package(rcl_interfaces REQUIRED)
find_package(proyecto_dominio_interfaces REQUIRED)

add_executable(sensor_stub src/sensor_stub_main.cpp)
target_include_directories(sensor_stub PUBLIC
  $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/include>)
target_compile_features(sensor_stub PUBLIC cxx_std_17)
ament_target_dependencies(sensor_stub rclcpp rcl_interfaces proyecto_dominio_interfaces)
install(TARGETS sensor_stub DESTINATION lib/${PROJECT_NAME})

if(BUILD_TESTING)
  find_package(ament_cmake_gtest REQUIRED)
  ament_add_gtest(test_sensor_stub test/test_sensor_stub.cpp)
  target_include_directories(test_sensor_stub PUBLIC
    $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/include>)
  target_compile_features(test_sensor_stub PUBLIC cxx_std_17)
  ament_target_dependencies(test_sensor_stub rclcpp rcl_interfaces proyecto_dominio_interfaces)
endif()

ament_package()

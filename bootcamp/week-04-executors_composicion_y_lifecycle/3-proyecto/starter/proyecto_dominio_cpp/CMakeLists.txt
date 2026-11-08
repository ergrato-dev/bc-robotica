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
find_package(rclcpp_components REQUIRED)
find_package(rclcpp_lifecycle REQUIRED)
find_package(lifecycle_msgs REQUIRED)
find_package(proyecto_dominio_interfaces REQUIRED)

# Componente: biblioteca compartida que un container puede cargar. EXECUTABLE
# genera además el ejecutable de siempre (ros2 run proyecto_dominio_cpp
# sensor_stub), con SingleThreadedExecutor. TODO: justifica el executor en tu
# README; si cambias, añade EXECUTOR MultiThreadedExecutor.
add_library(sensor_stub_component SHARED src/sensor_stub_component.cpp)
target_include_directories(sensor_stub_component PUBLIC
  $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/include>)
target_compile_features(sensor_stub_component PUBLIC cxx_std_17)
ament_target_dependencies(sensor_stub_component
  rclcpp rclcpp_components rclcpp_lifecycle rcl_interfaces proyecto_dominio_interfaces)
rclcpp_components_register_node(sensor_stub_component
  PLUGIN "proyecto_dominio_cpp::SensorStub"
  EXECUTABLE sensor_stub)
install(TARGETS sensor_stub_component
  ARCHIVE DESTINATION lib
  LIBRARY DESTINATION lib
  RUNTIME DESTINATION bin)

if(BUILD_TESTING)
  find_package(ament_cmake_gtest REQUIRED)
  ament_add_gtest(test_sensor_stub test/test_sensor_stub.cpp)
  target_include_directories(test_sensor_stub PUBLIC
    $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/include>)
  target_compile_features(test_sensor_stub PUBLIC cxx_std_17)
  ament_target_dependencies(test_sensor_stub
    rclcpp rclcpp_lifecycle lifecycle_msgs rcl_interfaces proyecto_dominio_interfaces)
endif()

ament_package()

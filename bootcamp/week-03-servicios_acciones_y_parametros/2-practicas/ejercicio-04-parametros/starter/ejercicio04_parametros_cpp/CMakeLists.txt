cmake_minimum_required(VERSION 3.28)
project(ejercicio04_parametros_cpp)

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
find_package(std_msgs REQUIRED)

add_executable(heartbeat src/heartbeat_main.cpp)
target_include_directories(heartbeat PUBLIC
  $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/include>)
target_compile_features(heartbeat PUBLIC cxx_std_17)
ament_target_dependencies(heartbeat rclcpp rcl_interfaces std_msgs)
install(TARGETS heartbeat DESTINATION lib/${PROJECT_NAME})
# Instala el YAML en share/ para poder pasarlo con --params-file.
install(DIRECTORY config DESTINATION share/${PROJECT_NAME})

if(BUILD_TESTING)
  find_package(ament_cmake_gtest REQUIRED)
  ament_add_gtest(test_heartbeat test/test_heartbeat.cpp)
  target_include_directories(test_heartbeat PUBLIC
    $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/include>)
  target_compile_features(test_heartbeat PUBLIC cxx_std_17)
  ament_target_dependencies(test_heartbeat rclcpp rcl_interfaces std_msgs)
endif()

ament_package()

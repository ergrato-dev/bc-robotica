cmake_minimum_required(VERSION 3.28)
project(ejercicio03_accion_cpp)

if(NOT CMAKE_CXX_STANDARD)
  set(CMAKE_CXX_STANDARD 17)
  set(CMAKE_CXX_STANDARD_REQUIRED ON)
endif()
if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic -Werror)
endif()

find_package(ament_cmake REQUIRED)
find_package(rclcpp REQUIRED)
# rclcpp_action es una librería aparte de rclcpp: sin ella no hay ActionClient.
find_package(rclcpp_action REQUIRED)
find_package(ejercicio03_interfaces REQUIRED)

add_executable(move_client src/move_client_main.cpp)
target_include_directories(move_client PUBLIC
  $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/include>)
target_compile_features(move_client PUBLIC cxx_std_17)
ament_target_dependencies(move_client rclcpp rclcpp_action ejercicio03_interfaces)
install(TARGETS move_client DESTINATION lib/${PROJECT_NAME})

if(BUILD_TESTING)
  find_package(ament_cmake_gtest REQUIRED)
  ament_add_gtest(test_move_client test/test_move_client.cpp)
  target_include_directories(test_move_client PUBLIC
    $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/include>)
  target_compile_features(test_move_client PUBLIC cxx_std_17)
  ament_target_dependencies(test_move_client rclcpp rclcpp_action ejercicio03_interfaces)
endif()

ament_package()

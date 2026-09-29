cmake_minimum_required(VERSION 3.28)
project(ejercicio02_pubsub_cpp)

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

add_executable(sensor_publisher src/sensor_publisher_main.cpp)
target_include_directories(sensor_publisher PUBLIC
  $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/include>)
target_compile_features(sensor_publisher PUBLIC cxx_std_17)
ament_target_dependencies(sensor_publisher rclcpp std_msgs)

add_executable(sensor_listener src/sensor_listener_main.cpp)
target_include_directories(sensor_listener PUBLIC
  $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/include>)
target_compile_features(sensor_listener PUBLIC cxx_std_17)
ament_target_dependencies(sensor_listener rclcpp std_msgs)

install(TARGETS sensor_publisher sensor_listener
  DESTINATION lib/${PROJECT_NAME})

if(BUILD_TESTING)
  find_package(ament_cmake_gtest REQUIRED)
  ament_add_gtest(test_pubsub test/test_pubsub.cpp)
  target_include_directories(test_pubsub PUBLIC
    $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/include>)
  target_compile_features(test_pubsub PUBLIC cxx_std_17)
  ament_target_dependencies(test_pubsub rclcpp std_msgs)
endif()

ament_package()

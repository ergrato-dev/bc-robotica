cmake_minimum_required(VERSION 3.28)
project(ejercicio03_reading_cpp)

if(NOT CMAKE_CXX_STANDARD)
  set(CMAKE_CXX_STANDARD 17)
  set(CMAKE_CXX_STANDARD_REQUIRED ON)
endif()
if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic -Werror)
endif()

find_package(ament_cmake REQUIRED)
find_package(rclcpp REQUIRED)
# Encuentra los headers generados en install/ejercicio03_interfaces.
find_package(ejercicio03_interfaces REQUIRED)

add_executable(reading_listener src/reading_listener_main.cpp)
target_include_directories(reading_listener PUBLIC
  $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/include>)
target_compile_features(reading_listener PUBLIC cxx_std_17)
ament_target_dependencies(reading_listener rclcpp ejercicio03_interfaces)
install(TARGETS reading_listener DESTINATION lib/${PROJECT_NAME})

if(BUILD_TESTING)
  find_package(ament_cmake_gtest REQUIRED)
  ament_add_gtest(test_reading test/test_reading.cpp)
  target_include_directories(test_reading PUBLIC
    $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/include>)
  target_compile_features(test_reading PUBLIC cxx_std_17)
  ament_target_dependencies(test_reading rclcpp ejercicio03_interfaces)
endif()

ament_package()

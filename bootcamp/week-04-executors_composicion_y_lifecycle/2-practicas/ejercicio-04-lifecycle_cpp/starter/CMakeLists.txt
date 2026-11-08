cmake_minimum_required(VERSION 3.28)
project(ejercicio04_lifecycle_cpp)

if(NOT CMAKE_CXX_STANDARD)
  set(CMAKE_CXX_STANDARD 17)
  set(CMAKE_CXX_STANDARD_REQUIRED ON)
endif()
if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic -Werror)
endif()

find_package(ament_cmake REQUIRED)
find_package(rclcpp REQUIRED)
find_package(rclcpp_components REQUIRED)
find_package(rclcpp_lifecycle REQUIRED)
find_package(lifecycle_msgs REQUIRED)
find_package(std_msgs REQUIRED)

# Componente, como en el Ejercicio 02: un nodo lifecycle también se puede
# cargar en un container (así funcionan los nodos de Nav2).
add_library(range_driver_component SHARED src/range_driver_component.cpp)
target_include_directories(range_driver_component PUBLIC
  $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/include>)
target_compile_features(range_driver_component PUBLIC cxx_std_17)
ament_target_dependencies(range_driver_component
  rclcpp rclcpp_components rclcpp_lifecycle lifecycle_msgs std_msgs)
rclcpp_components_register_node(range_driver_component
  PLUGIN "ejercicio04_lifecycle_cpp::RangeDriver"
  EXECUTABLE range_driver)
install(TARGETS range_driver_component
  ARCHIVE DESTINATION lib
  LIBRARY DESTINATION lib
  RUNTIME DESTINATION bin)

if(BUILD_TESTING)
  find_package(ament_cmake_gtest REQUIRED)
  ament_add_gtest(test_range_driver test/test_range_driver.cpp)
  target_include_directories(test_range_driver PUBLIC
    $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/include>)
  target_compile_features(test_range_driver PUBLIC cxx_std_17)
  ament_target_dependencies(test_range_driver rclcpp rclcpp_lifecycle lifecycle_msgs std_msgs)
endif()

ament_package()

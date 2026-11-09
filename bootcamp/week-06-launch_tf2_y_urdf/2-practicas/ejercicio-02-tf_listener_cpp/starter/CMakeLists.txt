cmake_minimum_required(VERSION 3.28)
project(ejercicio02_tf_listener_cpp)

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
find_package(geometry_msgs REQUIRED)
find_package(tf2 REQUIRED)
find_package(tf2_ros REQUIRED)

# Biblioteca con la geometría: el nodo y los tests enlazan la misma.
add_library(dock_geometry src/dock_geometry.cpp)
target_include_directories(dock_geometry PUBLIC
  $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/include>)
target_compile_features(dock_geometry PUBLIC cxx_std_17)
ament_target_dependencies(dock_geometry geometry_msgs)

add_executable(dock_monitor src/dock_monitor.cpp)
target_link_libraries(dock_monitor dock_geometry)
ament_target_dependencies(dock_monitor rclcpp std_msgs geometry_msgs tf2 tf2_ros)
install(TARGETS dock_monitor DESTINATION lib/${PROJECT_NAME})

# Los launch files van a share/, como en un paquete Python.
install(DIRECTORY launch DESTINATION share/${PROJECT_NAME})

if(BUILD_TESTING)
  find_package(ament_cmake_gtest REQUIRED)
  ament_add_gtest(test_dock_geometry test/test_dock_geometry.cpp)
  target_link_libraries(test_dock_geometry dock_geometry)
  # tf2::BufferCore: el mismo buffer que usa el listener, sin nodo ni red.
  ament_add_gtest(test_tf_buffer test/test_tf_buffer.cpp)
  target_link_libraries(test_tf_buffer dock_geometry)
  ament_target_dependencies(test_tf_buffer tf2 geometry_msgs)
endif()

ament_package()

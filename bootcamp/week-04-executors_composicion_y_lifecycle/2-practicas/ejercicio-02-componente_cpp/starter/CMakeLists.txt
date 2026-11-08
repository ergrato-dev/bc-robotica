cmake_minimum_required(VERSION 3.28)
project(ejercicio02_componente_cpp)

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
find_package(std_srvs REQUIRED)

# ============================================
# PASO 2: Compilar y registrar el componente
# ============================================
# Un componente es una biblioteca compartida (.so), no un ejecutable: el
# container la carga en marcha. rclcpp_components_register_node la anuncia
# en el índice de ament con su nombre de clase y, con EXECUTABLE, genera
# además un ejecutable para seguir usando ros2 run. EXECUTOR elige el
# executor de ese ejecutable (sin él, SingleThreadedExecutor).
# Descomenta las siguientes líneas para el Paso 2:
#
# add_library(monitor_component SHARED src/monitor_component.cpp)
# target_include_directories(monitor_component PUBLIC
#   $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/include>)
# target_compile_features(monitor_component PUBLIC cxx_std_17)
# ament_target_dependencies(monitor_component rclcpp rclcpp_components std_srvs)
# rclcpp_components_register_node(monitor_component
#   PLUGIN "ejercicio02_componente_cpp::Monitor"
#   EXECUTABLE monitor
#   EXECUTOR MultiThreadedExecutor)
# install(TARGETS monitor_component
#   ARCHIVE DESTINATION lib
#   LIBRARY DESTINATION lib
#   RUNTIME DESTINATION bin)

if(BUILD_TESTING)
  find_package(ament_cmake_gtest REQUIRED)
  find_package(ament_index_cpp REQUIRED)
  ament_add_gtest(test_monitor test/test_monitor.cpp)
  target_include_directories(test_monitor PUBLIC
    $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/include>)
  target_compile_features(test_monitor PUBLIC cxx_std_17)
  ament_target_dependencies(test_monitor rclcpp std_srvs ament_index_cpp)
endif()

ament_package()

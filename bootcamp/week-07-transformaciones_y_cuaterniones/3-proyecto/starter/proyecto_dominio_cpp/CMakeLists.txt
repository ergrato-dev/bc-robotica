cmake_minimum_required(VERSION 3.28)
project(proyecto_dominio_cpp)

if(NOT CMAKE_CXX_STANDARD)
  set(CMAKE_CXX_STANDARD 17)
  set(CMAKE_CXX_STANDARD_REQUIRED ON)
endif()
if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic -Werror)
endif()

# compile_commands.json para clang-tidy (Semana 05, Ejercicio 03).
set(CMAKE_EXPORT_COMPILE_COMMANDS ON)

find_package(ament_cmake REQUIRED)
find_package(rclcpp REQUIRED)
find_package(rcl_interfaces REQUIRED)
find_package(rclcpp_components REQUIRED)
find_package(rclcpp_lifecycle REQUIRED)
find_package(lifecycle_msgs REQUIRED)
find_package(proyecto_dominio_interfaces REQUIRED)
# Para publicar odom -> base_link.
find_package(geometry_msgs REQUIRED)
find_package(tf2_ros REQUIRED)

# Componente: biblioteca compartida que un container puede cargar. EXECUTABLE
# genera además el ejecutable de siempre (ros2 run proyecto_dominio_cpp
# sensor_stub), con SingleThreadedExecutor. TODO: justifica el executor en tu
# README; si cambias, añade EXECUTOR MultiThreadedExecutor.
add_library(sensor_stub_component SHARED src/sensor_stub_component.cpp)
target_include_directories(sensor_stub_component PUBLIC
  $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/include>)
target_compile_features(sensor_stub_component PUBLIC cxx_std_17)
ament_target_dependencies(sensor_stub_component
  rclcpp rclcpp_components rclcpp_lifecycle rcl_interfaces proyecto_dominio_interfaces
  geometry_msgs tf2_ros)
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
    rclcpp rclcpp_lifecycle lifecycle_msgs rcl_interfaces proyecto_dominio_interfaces
    geometry_msgs tf2_ros)
  ament_add_gtest(test_route test/test_route.cpp)
  target_include_directories(test_route PUBLIC
    $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/include>)

  # Lint como tests de colcon, igual que en el Ejercicio 03 de la Semana 05.
  find_package(ament_cmake_test REQUIRED)
  find_program(CLANG_FORMAT clang-format REQUIRED)
  find_program(CLANG_TIDY clang-tidy REQUIRED)
  file(GLOB_RECURSE LINT_SOURCES CONFIGURE_DEPENDS
    ${CMAKE_CURRENT_SOURCE_DIR}/include/*.hpp
    ${CMAKE_CURRENT_SOURCE_DIR}/src/*.cpp
    ${CMAKE_CURRENT_SOURCE_DIR}/test/*.cpp)
  file(GLOB TIDY_SOURCES CONFIGURE_DEPENDS ${CMAKE_CURRENT_SOURCE_DIR}/src/*.cpp)
  ament_add_test(clang_format GENERATE_RESULT_FOR_RETURN_CODE_ZERO
    COMMAND ${CLANG_FORMAT} --dry-run --Werror ${LINT_SOURCES})
  ament_add_test(clang_tidy GENERATE_RESULT_FOR_RETURN_CODE_ZERO
    COMMAND ${CLANG_TIDY} -p ${CMAKE_BINARY_DIR} --quiet ${TIDY_SOURCES})
endif()

ament_package()

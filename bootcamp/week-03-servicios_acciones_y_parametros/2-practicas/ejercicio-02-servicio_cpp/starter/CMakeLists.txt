cmake_minimum_required(VERSION 3.28)
project(ejercicio02_servicio_cpp)

if(NOT CMAKE_CXX_STANDARD)
  set(CMAKE_CXX_STANDARD 17)
  set(CMAKE_CXX_STANDARD_REQUIRED ON)
endif()
if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic -Werror)
endif()

find_package(ament_cmake REQUIRED)
find_package(rclcpp REQUIRED)
find_package(std_srvs REQUIRED)

# Un ejecutable por nodo; los dos comparten los headers de include/.
foreach(node enable_server enable_client)
  add_executable(${node} src/${node}_main.cpp)
  target_include_directories(${node} PUBLIC
    $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/include>)
  target_compile_features(${node} PUBLIC cxx_std_17)
  ament_target_dependencies(${node} rclcpp std_srvs)
  install(TARGETS ${node} DESTINATION lib/${PROJECT_NAME})
endforeach()

if(BUILD_TESTING)
  find_package(ament_cmake_gtest REQUIRED)
  ament_add_gtest(test_servicio test/test_servicio.cpp)
  target_include_directories(test_servicio PUBLIC
    $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/include>)
  target_compile_features(test_servicio PUBLIC cxx_std_17)
  ament_target_dependencies(test_servicio rclcpp std_srvs)
endif()

ament_package()

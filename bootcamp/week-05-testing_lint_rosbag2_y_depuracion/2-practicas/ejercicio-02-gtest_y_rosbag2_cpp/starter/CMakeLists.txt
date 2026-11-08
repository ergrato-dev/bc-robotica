cmake_minimum_required(VERSION 3.28)
project(ejercicio02_gtest_rosbag2_cpp)

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
find_package(rosbag2_cpp REQUIRED)
find_package(rosbag2_storage REQUIRED)

# Biblioteca con lo que se prueba: el ejecutable y los tests enlazan la misma.
add_library(range_tools src/bag_tools.cpp)
target_include_directories(range_tools PUBLIC
  $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/include>)
target_compile_features(range_tools PUBLIC cxx_std_17)
ament_target_dependencies(range_tools rclcpp std_msgs rosbag2_cpp rosbag2_storage)

add_executable(range_filter src/range_filter_main.cpp)
target_link_libraries(range_filter range_tools)
install(TARGETS range_filter DESTINATION lib/${PROJECT_NAME})

if(BUILD_TESTING)
  find_package(ament_cmake_gtest REQUIRED)

  # ============================================
  # PASO 1: Registrar el test unitario
  # ============================================
  # ament_add_gtest compila test/test_filtering.cpp como un ejecutable de
  # gtest y lo apunta para que colcon test lo ejecute.
  # Descomenta las siguientes líneas para el Paso 1:
  #
  # ament_add_gtest(test_filtering test/test_filtering.cpp)
  # target_link_libraries(test_filtering range_tools)

  ament_add_gtest(test_bag_tools test/test_bag_tools.cpp)
  target_link_libraries(test_bag_tools range_tools)
endif()

ament_package()

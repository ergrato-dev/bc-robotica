cmake_minimum_required(VERSION 3.28)
project(ejercicio03_lint_cpp)

if(NOT CMAKE_CXX_STANDARD)
  set(CMAKE_CXX_STANDARD 17)
  set(CMAKE_CXX_STANDARD_REQUIRED ON)
endif()
if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic -Werror)
endif()
# Qué: escribe build/<paquete>/compile_commands.json con el comando exacto de
# cada .cpp. Para qué: clang-tidy necesita esas flags e includes para analizar
# el código igual que lo compila el compilador.
set(CMAKE_EXPORT_COMPILE_COMMANDS ON)

find_package(ament_cmake REQUIRED)
find_package(rclcpp REQUIRED)
find_package(std_msgs REQUIRED)

add_executable(battery_monitor src/battery_monitor.cpp)
ament_target_dependencies(battery_monitor rclcpp std_msgs)
install(TARGETS battery_monitor DESTINATION lib/${PROJECT_NAME})

if(BUILD_TESTING)
  find_package(ament_cmake_test REQUIRED)
  find_program(CLANG_FORMAT clang-format REQUIRED)
  find_program(CLANG_TIDY clang-tidy REQUIRED)
  set(SOURCES ${CMAKE_CURRENT_SOURCE_DIR}/src/battery_monitor.cpp)
  # ament_add_test registra el comando como test de colcon: código de salida 0
  # es aprobado. GENERATE_RESULT_FOR_RETURN_CODE_ZERO hace que aparezca con su
  # nombre en colcon test-result.
  ament_add_test(clang_format GENERATE_RESULT_FOR_RETURN_CODE_ZERO
    COMMAND ${CLANG_FORMAT} --dry-run --Werror ${SOURCES})
  ament_add_test(clang_tidy GENERATE_RESULT_FOR_RETURN_CODE_ZERO
    COMMAND ${CLANG_TIDY} -p ${CMAKE_BINARY_DIR} --quiet ${SOURCES})
endif()

ament_package()

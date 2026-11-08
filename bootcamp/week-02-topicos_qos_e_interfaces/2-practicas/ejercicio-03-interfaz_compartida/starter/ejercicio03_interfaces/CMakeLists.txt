cmake_minimum_required(VERSION 3.28)
project(ejercicio03_interfaces)

find_package(ament_cmake REQUIRED)

# ============================================
# PASO 1 (parte B): generar el código de la interfaz
# ============================================
# Qué: rosidl lee msg/SensorReading.msg y genera Python, C++ y typesupport.
# Impacto: sin esto el paquete compila pero no contiene ningún tipo.
# Descomenta las siguientes líneas para el Paso 1:
#
# find_package(rosidl_default_generators REQUIRED)
# find_package(std_msgs REQUIRED)
#
# rosidl_generate_interfaces(${PROJECT_NAME}
#   "msg/SensorReading.msg"
#   DEPENDENCIES std_msgs
# )
#
# ament_export_dependencies(rosidl_default_runtime)

ament_package()

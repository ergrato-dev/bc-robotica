cmake_minimum_required(VERSION 3.28)
project(proyecto_dominio_interfaces)

find_package(ament_cmake REQUIRED)
find_package(rosidl_default_generators REQUIRED)
find_package(std_msgs REQUIRED)

# TODO: si renombras DomainState.msg, cambia también esta ruta.
rosidl_generate_interfaces(${PROJECT_NAME}
  "msg/DomainState.msg"
  DEPENDENCIES std_msgs
)

ament_export_dependencies(rosidl_default_runtime)
ament_package()

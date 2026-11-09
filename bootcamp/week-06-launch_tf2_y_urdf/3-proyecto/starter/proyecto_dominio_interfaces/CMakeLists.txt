cmake_minimum_required(VERSION 3.28)
project(proyecto_dominio_interfaces)

find_package(ament_cmake REQUIRED)
find_package(rosidl_default_generators REQUIRED)
find_package(std_msgs REQUIRED)

# TODO: si renombras DomainState.msg o SetMode.srv, cambia también estas rutas.
rosidl_generate_interfaces(${PROJECT_NAME}
  "msg/DomainState.msg"
  "srv/SetMode.srv"
  DEPENDENCIES std_msgs
)

ament_export_dependencies(rosidl_default_runtime)
ament_package()

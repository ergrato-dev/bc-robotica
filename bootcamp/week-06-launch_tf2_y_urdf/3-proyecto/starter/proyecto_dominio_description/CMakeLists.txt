cmake_minimum_required(VERSION 3.28)
project(proyecto_dominio_description)

find_package(ament_cmake REQUIRED)

# Paquete *_description: solo el modelo del robot y el launch que lo publica.
# Sin código: lo usan el bringup de esta semana, Gazebo (Semana 08) y Nav2.
install(DIRECTORY urdf launch DESTINATION share/${PROJECT_NAME})

ament_package()

# Estado simulado del robot en tu dominio.
# TODO: renombra el tipo a algo de tu misión (AisleState, BenchState...) y
# adapta los campos con la tabla del README del proyecto. Unidades SI.

std_msgs/Header header

string location            # dónde está el robot: pasillo, mesa, surco...
uint32 pending_tasks       # tareas que quedan en la misión
float32 battery_percent    # carga de 0.0 a 100.0

uint8 MODE_IDLE=0
uint8 MODE_WORKING=1
uint8 MODE_CHARGING=2
uint8 mode                 # uno de los MODE_* de arriba

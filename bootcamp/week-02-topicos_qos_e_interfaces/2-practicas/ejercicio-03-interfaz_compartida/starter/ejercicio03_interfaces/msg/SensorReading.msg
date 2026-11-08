# Lectura de un sensor genérico, con unidad y estado.
# Compartida por ejercicio03_reading_py (publisher) y ejercicio03_reading_cpp
# (listener): un solo contrato para los dos lenguajes.

# ============================================
# PASO 2: Campos del mensaje
# ============================================
# Hasta este paso el mensaje no tiene campos. Quita solo el "# " inicial de
# cada línea de abajo.
# Descomenta las siguientes líneas para el Paso 2:
#
# std_msgs/Header header
#
# string sensor_id          # qué sensor midió ("front", "left"...)
# float64 value             # valor medido, en la unidad de "unit"
# string unit "m"           # unidad SI; por defecto metros
# bool is_valid true        # false si el sensor está fuera de su rango útil
#
# uint8 STATUS_OK=0
# uint8 STATUS_WARN=1
# uint8 STATUS_ERROR=2
# uint8 status              # uno de los STATUS_* de arriba

# Ejercicio 03 — Comparar `rclpy` vs `rclcpp` con `ros2 topic hz`

Sin código nuevo: usa los dos nodos que ya construiste (Ejercicios 01 y 02) para medir
si hay una diferencia observable de frecuencia/latencia entre un publisher Python y uno
C++ publicando el mismo mensaje al mismo ritmo nominal (0.5 s).

Esta es la primera vez del bootcamp que **mides** en vez de asumir — hábito que se
repite en las semanas 09, 11 y 17.

## Paso 1: Publisher Python, medir con la CLI

```bash
# Terminal 1
ros2 run ejercicio01_pubsub_py sensor_publisher

# Terminal 2
ros2 topic hz /sensor/state --window 20
```

Anota la frecuencia media reportada (debería rondar 2.0 Hz — el timer es de 0.5 s) y el
`min`/`max` de la ventana.

## Paso 2: Publisher C++, mismo topic, misma medición

Detén el publisher Python (`Ctrl+C`), y repite con el nodo C++:

```bash
# Terminal 1
ros2 run ejercicio02_pubsub_cpp sensor_publisher

# Terminal 2
ros2 topic hz /sensor/state --window 20
```

## Paso 3: Medir con `ros2 topic delay` (si tu mensaje tuviera `Header`)

`std_msgs/String` no tiene campo `Header` con timestamp, así que `ros2 topic delay` no
aplica aquí — lo verás de verdad en la Semana 02 cuando cambiemos a un mensaje con
`Header`. Por ahora, anota en tu README de proyecto (`3-proyecto/`) qué observaste en
los pasos 1 y 2.

## Preguntas para tu informe (respóndelas en el README de tu `3-proyecto/`)

1. ¿La frecuencia media fue distinta entre el publisher Python y el C++? ¿Por cuánto?
2. Un timer de 0.5 s en ROS2 no es tiempo real duro — ¿qué esperarías que pasara si el
   callback del timer tardara más de 0.5 s en ejecutarse, en cualquiera de los dos
   lenguajes?
3. Con solo este ejercicio, ¿es suficiente evidencia para decidir "siempre uso C++
   porque es más rápido"? ¿Qué te falta medir para una decisión real? (Esto se retoma
   con benchmarking formal en la Semana 17/Track A y B — semana de integración y
   rendimiento).

## Checklist

- [ ] Medí la frecuencia del publisher Python con `ros2 topic hz`
- [ ] Medí la frecuencia del publisher C++ con `ros2 topic hz`
- [ ] Escribí mis observaciones y respuestas en `3-proyecto/README.md`

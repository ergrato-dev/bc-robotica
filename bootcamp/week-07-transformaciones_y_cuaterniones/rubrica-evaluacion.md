# Rúbrica de Evaluación — Semana 07

Evaluación en tres componentes. Mínimo **70%** en cada uno para aprobar la semana.

## 🧠 Conocimiento (30%)

Cuestionario de autoevaluación. Responde primero sin ver las respuestas.

1. Escribe la matriz de rotación de un giro de 90° en yaw sin mirar ninguna
   fórmula. ¿Qué truco usaste?
2. ¿Por qué la inversa de una matriz de rotación es su traspuesta?
3. Un punto y una velocidad se multiplican por la misma matriz 4x4. ¿Por qué a
   uno le afecta la traslación y al otro no?
4. Tienes `T_odom_base` y `T_base_laser`. ¿Cómo obtienes `T_odom_laser`? ¿Y
   `T_laser_odom`?
5. Al invertir `T_a_b` alguien escribe la nueva traslación como `-t`. ¿Cuándo
   funciona y cuándo no?
6. ¿En qué orden y sobre qué ejes aplica ROS roll, pitch y yaw? ¿Dónde lo usas
   sin darte cuenta?
7. ¿Qué es el bloqueo de cardán y por qué un cuaternión no lo sufre?
8. El robot mira con yaw 3.0 y quiere mirar con yaw -3.0. ¿Cuánto tiene que
   girar y hacia qué lado?
9. Escribe el cuaternión de un giro de 180° alrededor de y. ¿Qué otro
   cuaternión representa el mismo giro?
10. Pasas el resultado de `transforms3d.euler.euler2quat(0, 0, π/2)` directamente
    a un mensaje de ROS. ¿Qué giro obtienes?

<details>
<summary>Ver respuestas</summary>

1. `[[0, -1, 0], [1, 0, 0], [0, 0, 1]]`. Las columnas son los ejes del marco
   girado vistos desde el padre: el nuevo x apunta a `+y` (`(0, 1, 0)`), el nuevo
   y a `-x` (`(-1, 0, 0)`) y z no cambia.
2. Porque sus columnas son vectores unitarios y perpendiculares entre sí:
   `Rᵀ R` multiplica cada eje por los demás, y da 1 en la diagonal y 0 fuera, la
   identidad.
3. Por la cuarta coordenada: el punto lleva un 1, que multiplica la columna de
   traslación; la velocidad lleva un 0, que la anula. Una dirección gira con el
   marco pero no se desplaza con él.
4. `T_odom_laser = T_odom_base @ T_base_laser` (los subíndices de dentro se
   tocan). `T_laser_odom` es su inversa: rotación traspuesta y traslación
   `-Rᵀ t`.
5. Solo cuando no hay rotación (`R` es la identidad). Con rotación hay que girar
   la traslación: `-Rᵀ t`.
6. Primero roll en x, luego pitch en y, luego yaw en z, sobre los ejes fijos del
   padre: `R = Rz(yaw) · Ry(pitch) · Rx(roll)`. En el `rpy` de URDF y en
   `--roll --pitch --yaw` de `static_transform_publisher`.
7. Con pitch de ±90°, roll y yaw giran alrededor del mismo eje y se pierde un
   grado de libertad: solo se recupera su diferencia. El cuaternión describe el
   giro como eje y ángulo, sin descomponerlo en tres giros, así que no tiene
   ninguna orientación especial.
8. 0.283 rad (2π - 6) hacia la izquierda: `atan2(sin(-6), cos(-6))`. Restando a
   secas saldría -6.0, casi una vuelta entera hacia la derecha.
9. `(0, 1, 0, 0)`: eje y, `sin(90°) = 1`, `cos(90°) = 0`. También `(0, -1, 0, 0)`:
   `q` y `-q` son el mismo giro.
10. `transforms3d` pone `w` delante: devuelve `(0.707, 0, 0, 0.707)`. Leído como
    `(x, y, z, w)` es un giro de 90° en **roll**, no en yaw.

</details>

## 💪 Desempeño (40%)

Verificado automáticamente por `colcon test` en cada `starter/`:

| Ejercicio | Verificación |
|---|---|
| 01 (calculadora) | `test_homogeneous` (13), `test_contra_tf2` (2) |
| 02 (cuaterniones) | `test_quaternions` (16) |
| 03 (tf2) | `test_to_frame` (3), `test_relay_launch` |

Además, haber roto el código a propósito y visto fallar el test correspondiente
(checklist de cada ejercicio).

```bash
colcon test --packages-select ejercicio01_transform_calculator_py \
  ejercicio02_quaternions_py ejercicio03_point_transform_py
colcon test-result --verbose
```

## 📦 Producto (30%)

La capa del proyecto del dominio (`3-proyecto/`):

- [ ] `bearing_and_range` pasa `test_targeting.py` sin importar nada de ROS
- [ ] `target_locator` publica el objetivo en el marco del sensor y
      `test_target_locator_launch.py` pasa
- [ ] El objetivo, el sensor, su campo de visión y su alcance son los de tu misión
- [ ] `colcon test` pasa en `proyecto_dominio_py` y `proyecto_dominio_cpp`
- [ ] Respuestas de los tres ejercicios en el README del proyecto

Criterios observables más allá de los tests:

| Criterio | Bien | Mal |
|---|---|---|
| Uso de tf2 | `buffer.transform` y nada más | Matrices calculadas a mano con datos que ya están en `/tf` |
| Parámetros | Objetivo, campo de visión y alcance como parámetros, justificados en el README | Valores del starter sin cambiar |
| Ángulos | Radianes por dentro, grados solo en el log | Grados mezclados en los cálculos |

### Penalizaciones (ver también `.github/copilot-instructions.md`)

| Situación | Penalización |
|---|---|
| No compila/lintea limpio | 0 en Producto |
| Cuaterniones escritos componente a componente sin calcular `w` | -10 |
| Diferencias de ángulos sin normalizar | -10 |
| `except Exception` en vez de las excepciones de tf2 | -10 |
| Código copiado de otra misión/dominio | 0 en Producto |

---

## 🔗 Navegación

| Anterior | Actual | Siguiente |
| -------- | ------ | --------- |
| [Glosario](5-glosario/README.md) | **Rúbrica** | Semana 08 (pendiente de publicar) |

← [Volver a la Semana 07](README.md)

<p align="center">
  <img src="assets/bootcamp-header.svg" alt="Robotics Zero to Hero Bootcamp" width="800">
</p>

<p align="center">
  <a href="LICENSE"><img src="https://img.shields.io/badge/license-CC%20BY--NC--SA%204.0-lightgrey.svg" alt="License CC BY-NC-SA 4.0"></a>
  <a href="#"><img src="https://img.shields.io/badge/weeks-19-yellow.svg" alt="19 Weeks"></a>
  <a href="#"><img src="https://img.shields.io/badge/hours-190-orange.svg" alt="190 Hours"></a>
  <a href="#"><img src="https://img.shields.io/badge/ROS2-Jazzy-22314E?logo=ros&logoColor=white" alt="ROS2 Jazzy"></a>
  <a href="#"><img src="https://img.shields.io/badge/Python%20%2B%20C%2B%2B-first%20class-4b8bbe.svg" alt="Python + C++"></a>
</p>

<p align="center">
  <a href="README.md"><img src="https://img.shields.io/badge/🇪🇸_Español-0969DA?style=for-the-badge&logoColor=white" alt="Spanish Version"></a>
</p>

---

## 📋 Description

Intensive **19-week (~4.5 months)** bootcamp focused on **robotics with ROS2**, from
absolute zero in robotics to an autonomous mobile robot with SLAM+Nav2 or a
manipulator arm with vision and pick&place. Everything verifiable in simulation, with
**Python and C++ as first-class languages** — neither relegated to a side note.

### 🎯 Goals

By the end of the bootcamp, students will be able to:

- ✅ Master the ROS2 computational graph (nodes, topics, services, actions, QoS)
- ✅ Write equivalent nodes in `rclpy` and `rclcpp`, and know when to use each
- ✅ Model a robot in URDF/Xacro and reason about its TF2 tree
- ✅ Simulate a full robot in Gazebo Harmonic and verify it headless
- ✅ Build perception with OpenCV (and optional deep-learning detection)
- ✅ Fuse sensors with an EKF and justify when a node needs C++
- ✅ **Track A**: map, localize and navigate autonomously with Nav2, including
  writing your own C++ plugins
- ✅ **Track B**: plan motion, detect objects and run a full pick&place pipeline with
  MoveIt2, including a C++ planning adapter
- ✅ Document and demonstrate a robotic system with reproducible evidence

### 🚀 Why this bootcamp?

> **Both languages first-class from day one** — Python to prototype and orchestrate,
> C++ where the framework requires it or there's a real latency budget.

Instructor and students both start with no prior robotics experience (though with
prior programming experience): the curriculum relies only on official documentation
and mature stacks (ROS2 LTS, Nav2, MoveIt2, Gazebo Harmonic), no experimental paths.

---

## 🗓️ Bootcamp Structure

|         Phase          | Weeks | Hours | Main Topics                                      |
| :---------------------: | :---: | :---: | ------------------------------------------------ |
| **1 · Bilingual ROS2 Fundamentals** |   1-5   |  50h  | Graph/DDS, topics, QoS, services, actions, executors, TF2, URDF — in `rclpy` **and** `rclcpp` |
| **2 · Simulation and Perception**   |  6-10   |  50h  | Gazebo Harmonic, sensors, OpenCV, EKF fusion, advanced detection |
| **3 · Common bridge: kinematics**   |  11-12  |  20h  | Differential and arm kinematics, track/domain checkpoint |
| **4 · Specialization (Track A or B)** |  13-17  |  50h  | Track A: SLAM+Nav2 (with C++ plugins) · Track B: MoveIt2+vision (with C++ plugins) |
| **5 · Capstone**         |  18-19  |  20h  | Final integration, demo, optional hardware |

**Total: 19 weeks** | **190 hours** of intensive training

### 🔀 Two Tracks, One Path

Weeks 01-12 are common to everyone. The track is chosen in week 12:

- **Track A · Autonomous Mobile** — SLAM (`slam_toolbox`) + AMCL + Nav2. Capstone: a
  robot that maps, localizes and navigates while avoiding obstacles.
- **Track B · Manipulator** — MoveIt2 + vision. Capstone: an arm that detects an
  object and executes pick&place.

See [docs/tracks.md](docs/tracks.md) for the full policy (includes the anti-plagiarism
mission/domain catalog).

---

## 📚 Weekly Content

Each week includes:

```
bootcamp/week-XX-main_topic/              # weeks 01-12
bootcamp/track-{a,b}/week-XX-topic/       # weeks 13-19, per track
├── README.md                 # Objectives and schedule
├── rubrica-evaluacion.md     # Evaluation criteria
├── 0-assets/                 # SVG diagrams
├── 1-teoria/                 # Theoretical material
├── 2-practicas/              # Guided exercises (rclpy and/or rclcpp)
├── 3-proyecto/                # Weekly project layer (track + domain)
├── 4-recursos/                # ebooks-free/, videografia/, webgrafia/
└── 5-glosario/                 # Key terms
```

### 🔑 Key Components

- 📖 **Theory**: concepts with the why before the how, in `rclpy` and/or `rclcpp`
- 💻 **Practice**: guided exercises (uncomment pattern), verified with `colcon test`
  and headless simulation
- 📝 **Evaluation**: Knowledge (30%) + Performance (40%) + Product (30%)
- 🎓 **Resources**: glossaries, official references, supplementary material

---

## 🛠️ Tech Stack

| Technology | Version | Use |
|------------|---------|-----|
| ROS2 | **Jazzy Jalisco** | Middleware, LTS |
| Ubuntu | **24.04 LTS** | Base system |
| Python | **3.12.3** (`rclpy`) | Prototyping, orchestration, perception |
| C++ | **17** (`rclcpp`) | Hot path, Nav2/MoveIt2 plugins |
| Gazebo | **Harmonic** (`gz-sim` 8.7.0) | Simulation |
| Nav2 | `jazzy` branch | Autonomous navigation (Track A) |
| MoveIt2 | `jazzy` branch | Manipulation (Track B) |
| OpenCV | **4.10.0.84** | Perception |
| Docker | **27.5.1** | Mandatory development environment |

**Development environment**: Docker + WSLg/X11 for RViz2/Gazebo GUI (❌ do NOT install
ROS2 directly on the host OS except via the documented native alternative).

See [docs/stack-versions.md](docs/stack-versions.md) for full pinned details.

---

## 🚀 Quick Start

### Prerequisites

- **Docker** and **Docker Compose** installed
- **Prior programming experience in Python and/or C++** (this bootcamp does not teach
  basic syntax)
- **Git** for version control
- **VS Code** (recommended) with included extensions

### 1. Clone the Repository

```bash
git clone https://github.com/ergrato-dev/bc-robotica.git
cd bc-robotica
```

### 2. Set Up the Environment

→ [Docker setup guide](docs/setup/con-docker.md) (recommended, includes GUI
passthrough for RViz2/Gazebo via WSLg/X11)

### 3. Go to the Current Week

```bash
cd bootcamp/week-01-fundamentos_ros2_y_workspace
```

### 4. Follow the Instructions

Each week contains a `README.md` with detailed instructions.

---

## 📊 Learning Methodology

### Teaching Strategies

- 🎯 **Project-Based Learning**: one system that grows over 19 weeks on your track and
  your domain, never a throwaway exercise
- 🔁 **Uncomment to Learn**: exercises ship with explained code and tests; you learn by
  reading, uncommenting, and watching tests pass
- 🐍🔧 **Bilingual from day one**: every communication concept (weeks 01-05) is
  implemented in Python and C++, side by side
- 🖥️ **Simulation before hardware**: everything is validated in headless Gazebo first;
  physical hardware is always an optional extension (see
  [docs/hardware-opcional.md](docs/hardware-opcional.md))
- 📏 **Measure, don't assume**: `rclpy` vs `rclcpp` benchmarking in each track's
  integration weeks

---

## 📜 License

This bootcamp is licensed under [CC BY-NC-SA 4.0](LICENSE) — educational use,
non-commercial, adaptations share the same license.

## 🤝 Code of Conduct

See [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md).

## 🔒 Security

See [SECURITY.md](SECURITY.md).

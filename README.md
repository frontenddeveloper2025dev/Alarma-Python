# ⏰ Alarm Tool Project – Gestor de Alarmas Semanales

**Alarm Tool Project** es una aplicación web en español construida con **Streamlit** que permite crear, administrar y monitorear alarmas recurrentes por día y hora. Diseñada para ejecutarse de manera local, incluye un sistema de reproducción de audio que se activa automáticamente al cumplirse cada alarma.

---

## 🖼️ Vista Previa

![Alarm Tool UI](https://github.com/frontenddeveloper2025dev/Alarma-Python/blob/main/python%20alarm.jpeg)

---

## 📌 Características Principales

- Interfaz en español simple e intuitiva
- Configura alarmas por día y hora de la semana
- Reproducción automática de audio generado cuando la alarma se activa
- Historial de alarmas activadas
- Persistencia de datos con base de datos local (SQLite)
- Reproducción sin bloquear la interfaz (uso de hilos concurrentes)
- Reinicio automático de alarmas cada medianoche

---

## 🧠 Arquitectura del Sistema

### 🔹 Frontend – Interfaz de Usuario

- **Framework:** [Streamlit](https://streamlit.io)
- **Diseño:** Aplicación de una sola página con navegación lateral (sidebar)
- **Estado:** Manejo de `session_state` para mantener el estado activo
- **Idioma:** Español para todos los textos y controles

### 🔹 Backend – Lógica y Monitorización

- **Componentes principales:**
  - `AlarmMonitor`: Servicio en segundo plano que revisa si hay alarmas activas
  - `AlarmDatabase`: Gestor de persistencia basado en SQLite
  - `AudioPlayer`: Módulo de reproducción de audio con `pygame`
  - `AlarmSoundGenerator`: Generador de sonidos con `numpy` y guardado en WAV

- **Modelo de hilos:**
  - La app principal corre en el hilo principal (Streamlit)
  - La verificación de alarmas corre en un **hilo demonio**
  - La reproducción de audio corre en hilos independientes para no bloquear la app

- **Lógica de activación:**
  - Revisa alarmas activas cada 30 segundos
  - Impide que una alarma se dispare dos veces el mismo día
  - Reinicia automáticamente las alarmas al llegar medianoche

---

## 🗄️ Almacenamiento de Datos

- **Base de Datos:** SQLite (`alarms.db`)
- **Tablas:**
  - `alarms`: Configuración de cada alarma (nombre, hora, días, estado)
  - `alarm_history`: Registro histórico de activaciones
- **Formato de datos:** JSON para días de la semana, horas como `HH:MM`

---

## 🔊 Sistema de Audio

- **Generación de sonido:**
  - Sonidos beep generados con `numpy`
  - Frecuencias de 800Hz y 1000Hz combinadas
  - Archivos WAV temporales

- **Reproducción de audio:**
  - Uso de `pygame.mixer` para compatibilidad multiplataforma
  - Duración configurable (por defecto: 30 segundos)
  - Prevención de múltiples reproducciones simultáneas

---

## 🛡️ Manejo de Errores

- Degradación suave si no se puede inicializar el audio
- Try/except para errores durante la verificación y reproducción
- Limpieza automática de archivos temporales

---

## 📦 Dependencias

### 🐍 Librerías de Python

```text
streamlit     # Interfaz web
pandas        # Manejo de datos para mostrar alarmas
pygame        # Reproducción de audio
numpy         # Generación de sonido
sqlite3       # Base de datos local (incluido en Python)


## ▶️ Cómo Ejecutar

Instala las dependencias necesarias:

pip install streamlit pandas pygame numpy


Corre la app:

streamlit run app.py


## Abre la app en tu navegador en:

http://localhost:8501

##👩‍💻 Autora

Desarrollado por frontenddeveloper2025dev
 como proyecto de automatización y monitoreo local de alarmas con interfaz simple y efectiva.

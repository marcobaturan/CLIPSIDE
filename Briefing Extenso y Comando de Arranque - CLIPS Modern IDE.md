# **Briefing Detallado: Proyecto CLIPS Modern IDE**

## **1\. Visión del Proyecto**

El **CLIPS Modern IDE** es un entorno de desarrollo integrado diseñado específicamente para sistemas Linux (Debian 12\) que busca revitalizar la experiencia de programación en CLIPS (C Language Integrated Production System). El objetivo es ofrecer la robustez del IDE clásico de Windows/Mac, pero integrando capacidades modernas de Inteligencia Artificial local y una interfaz de usuario contemporánea basada en Python.

## **2\. Pila Tecnológica (Tech Stack)**

| Componente | Tecnología Seleccionada |
| :---- | :---- |
| Lenguaje de Programación | Python 3.11+ |
| Framework de GUI | CustomTkinter (Tema oscuro nativo) |
| Motor de Inferencia | CLIPSPy (Binding oficial para CLIPS 6.4) |
| Asistente de IA | Ollama (Modelo: marcobaturan/clips-architect-final) |
| Resaltado de Sintaxis | Pygments (Léxico adaptado para CLIPS) |
| Gestión de Entorno | Venv / Pip |

## **3\. Arquitectura y Estructura del Framework**

El proyecto se integrará dentro de la estructura de trabajo existente del usuario, respetando las rutas y patrones de diseño establecidos:  
/home/marco/PycharmProjects/CLIPSIDE  
├── src/  
│   ├── main.py            \# Punto de entrada de la aplicación  
│   ├── ui/                \# Componentes de CustomTkinter  
│   ├── core/              \# Lógica de integración con CLIPSPy y Ollama  
│   └── assets/            \# Iconos (Serpiente CLIPS) y Splash Screen  
├── scripts/  
│   └── setup\_env.sh       \# Script de instalación y configuración  
├── docs/  
│   ├── README.md          \# Documentación técnica extensa  
│   └── USER\_MANUAL.md     \# Guía de usuario final  
└── tests/                 \# Batería de pruebas unitarias

## **4\. Funcionalidades Críticas**

* **Editor Multicapa:** Soporte para .clp con numeración de líneas y resaltado de palabras clave (defrule, deffacts, etc.).  
* **Ventanas de Inspección:**  
  * *Fact Window:* Visualización en tiempo real de la memoria de trabajo.  
  * *Agenda Window:* Lista de activaciones pendientes en el motor.  
* **Consola REPL:** Terminal interactiva para ejecutar comandos directos al motor CLIPS.  
* **Ollama Chatbox:** Panel lateral para generación de código mediante IA local, enviando un System Prompt especializado en sintaxis CLIPS.

## **5\. Identidad Visual**

* **Icono:** Una versión modificada del logo de CLIPS donde el maniquí es reemplazado por una cabeza de serpiente (Python) con un microchip integrado.  
* **Splash Screen:** Imagen minimalista de la serpiente verde con el texto "CLIPS IDE" cargando los módulos.

# ---

**Comando de Arranque y Configuración**

Para inicializar el proyecto en la ruta especificada, ejecute el siguiente bloque en la terminal:  
\# 1\. Navegar al directorio y preparar entorno  
cd /home/marco/PycharmProjects/CLIPSIDE  
python3 \-m venv .venv  
source .venv/bin/activate

\# 2\. Instalar dependencias  
pip install customtkinter clipspy pygments ollama pillow

\# 3\. Crear el script de arranque de la aplicación (start.sh)  
cat \< start.sh  
\#\!/bin/bash  
source .venv/bin/activate  
python3 src/main.py  
EOF  
chmod \+x start.sh

\# 4\. Generar estructura inicial de archivos  
mkdir \-p src/ui src/core src/assets docs tests  
touch src/main.py src/core/engine.py src/ui/editor.py

## **6\. Plan de Publicación**

Al finalizar el desarrollo, se ejecutará un script de integración con Make/GraphQL para publicar un artículo técnico en Hashnode y LinkedIn, detallando el proceso de afinación del modelo en Ollama y la arquitectura del IDE.
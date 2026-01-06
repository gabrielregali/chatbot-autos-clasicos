# 🛠️ Asistente Técnico de Mantenimiento (RAG) - Chatbot

Asistente basado en **Retrieval-Augmented Generation (RAG)** para realizar consultas técnicas sobre **manuales originales de vehículos**, utilizando búsqueda semántica y modelos de lenguaje de gran escala.

El sistema responde **exclusivamente con información contenida en los manuales técnicos**, e indica explícitamente cuando un dato no se encuentra documentado, evitando inferencias externas o alucinaciones.

---

## 🌟 Características Principales

- **RAG estricto**: las respuestas se generan únicamente a partir del contenido de los manuales.
- **Sin alucinaciones**: si un dato no figura explícitamente, el asistente lo informa.
- **Búsqueda semántica**: recuperación de información por significado, no solo por palabras clave.
- **Multilenguaje**: combina manuales en español e inglés.
- **Escalable**: la misma arquitectura puede aplicarse a manuales de maquinaria industrial.

---

## 📚 Manuales incluidos (actualmente)

- **Fiat 600** – Manual de Taller  
- **Fiat Uno** – Manual Haynes (inglés)  
- **Citroën 3CV** – Manual del fabricante (español)

---

## 🛠️ Stack Tecnológico

- **Lenguaje:** Python 3.x  
- **Modelo de Lenguaje (LLM):** Google Gemini 2.5 Flash  
- **Modelo de Embeddings:** all-mpnet-base-v2 (Sentence Transformers)  
- **Base de Datos Vectorial:** Supabase (PostgreSQL + pgvector)  
- **Interfaz de Usuario:** Streamlit  

---

## 🚀 Instalación Rápida

Clonar el repositorio:

```bash
git clone https://github.com/tu-usuario/tu-repo.git
cd tu-repo


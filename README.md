# 🛠️ Asistente Técnico de Mantenimiento (RAG)

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

## 📚 Manuales incluidos

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

## 🚀 Instalación

### 1️⃣ Clonar el repositorio

```bash
git clone https://github.com/tu-usuario/tu-repo.git
cd tu-repo

### 2️⃣ Instalar dependencias

pip install -r requirements.txt

### 3️⃣ Configurar secretos

GEMINI_API_KEY = "tu_api_key"
SUPABASE_URL = "tu_supabase_url"
SUPABASE_KEY = "tu_supabase_anon_key"

### 4️⃣ Ejecutar la aplicación

streamlit run app.py

## 🧠 Funcionamiento General

1. La consulta del usuario se convierte en un **embedding semántico**.
2. Se realiza una **búsqueda vectorial** en Supabase utilizando `pgvector`.
3. Se recuperan los fragmentos más relevantes del manual seleccionado.
4. El modelo **Gemini** genera la respuesta utilizando **exclusivamente** ese contexto.
5. Si el dato solicitado no está presente en el manual, el sistema lo indica explícitamente.

---

## 🏭 Aplicación en Mantenimiento Industrial

Este proyecto funciona como una **Prueba de Concepto (PoC)** para Ingeniería de Mantenimiento y Confiabilidad.

La misma arquitectura puede utilizarse para:

- Consultas rápidas sobre manuales técnicos industriales.
- Reducción del **MTTR** mediante acceso inmediato a procedimientos.
- Digitalización del conocimiento experto.
- Asistencia conversacional para mantenimiento preventivo y correctivo.
- Soporte a procedimientos de seguridad y documentación técnica.

---

## ⚠️ Limitaciones

- La aplicación pública tiene un **límite diario de consultas** debido a las restricciones actuales de la API de Gemini.
- El asistente no reemplaza la lectura completa del manual ni el criterio profesional del técnico.

---

## 🔗 Demo en vivo

👉 **[https://chatbot-autos-clasicos-nvynbkrzdqtlxqzr9ornpo.streamlit.app/]**

---

## 👤 Autor

**Gabriel Alfredo Regali**  
Confiabilidad Mantenimiento · IA aplicada





# 🛠️ **Asistente Técnico de Mantenimiento (RAG)**

Asistente basado en **Retrieval-Augmented Generation (RAG)** para consultas técnicas sobre manuales originales de vehículos clásicos, utilizando búsqueda semántica y modelos de lenguaje de gran escala.

El sistema responde exclusivamente con información contenida en los manuales, indicando explícitamente cuando un dato no se encuentra documentado.

---

## 🌟 **Características Principales**
* **RAG estricto:** Respuestas basadas únicamente en manuales técnicos originales.
* **Sin alucinaciones:** Si el dato no figura en el manual, el asistente lo informa.
* **Búsqueda semántica:** Recuperación por significado, no por palabras clave.
* **Multilenguaje:** Combina manuales en español e inglés.
* **Escalable:** La arquitectura permite incorporar nuevos equipos o maquinaria industrial.

---

## 📚 **Manuales Incluidos (actualmente)**
* **Fiat 600** – Manual de Taller
* **Fiat Uno** – Manual Haynes (EN)
* **Citroën 3CV** – Manual del Fabricante (ES)

---

## 🛠️ **Stack Tecnológico**
* **Lenguaje:** Python 3.x
* **LLM:** Google Gemini 2.5 Flash
* **Embeddings:** `all-mpnet-base-v2` (Sentence Transformers)
* **Base Vectorial:** Supabase (PostgreSQL + pgvector)
* **Frontend:** Streamlit

---

## 🚀 **Instalación Rápida**

1. **Clonar el repositorio:**
   ```bash
   git clone [https://github.com/tu-repo.git](https://github.com/tu-repo.git)

2. **Instalar dependencias:**
  pip install -r requirements.txt

3. **Configurar secretos en .streamlit/secrets.toml:**
   GEMINI_API_KEY = "tu_api_key"
  SUPABASE_URL = "tu_url"
  SUPABASE_KEY = "tu_key"

4. **Ejecutar:**
   streamlit run app.py
   
---


## 🧠 Funcionamiento General

1. La consulta del usuario se convierte en un **embedding semántico**.
2. Se realiza una **búsqueda vectorial** en Supabase utilizando `pgvector`.
3. Se recuperan los fragmentos más relevantes del manual seleccionado.
4. El modelo **Gemini** genera la respuesta utilizando **exclusivamente** ese contexto.
5. Si el dato solicitado no está presente en el manual, el sistema lo indica explícitamente.

---


## 🏭 **Aplicación en Mantenimiento Industrial**

Este proyecto funciona como una **Prueba de Concepto (PoC)** para Ingeniería de Mantenimiento y Confiabilidad.

La misma arquitectura puede utilizarse para:

- Consultas rápidas sobre manuales técnicos industriales.
- Reducción del **MTTR** mediante acceso inmediato a procedimientos.
- Digitalización del conocimiento experto.
- Asistencia conversacional para mantenimiento preventivo y correctivo.
- Soporte a procedimientos de seguridad y documentación técnica.


## ⚠️ Limitaciones

- La aplicación pública tiene un **límite diario de consultas** debido a las restricciones actuales de la API de Gemini.
- El asistente no reemplaza la lectura completa del manual ni el criterio profesional del técnico.

---



🔗 **App en vivo:** 
👉 [https://chatbot-autos-clasicos-nvynbkrzdqtlxqzr9ornpo.streamlit.app/]


## 👤 Autor

**Gabriel Alfredo Regali**  
Ingeniería de Confiabilidad · Mantenimiento · IA aplicada




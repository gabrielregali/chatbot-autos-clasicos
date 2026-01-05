# -*- coding: utf-8 -*-
import streamlit as st
import re
from google import genai
from sentence_transformers import SentenceTransformer
from supabase import create_client

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(
    page_title="Asistente Técnico de Mantenimiento",
    page_icon="🛠️",
    layout="centered"
)

# --- CONFIGURACIÓN DE CLAVES (SEGURO PARA STREAMLIT CLOUD) ---
try:
    SUPABASE_URL = st.secrets["SUPABASE_URL"]
    SUPABASE_KEY = st.secrets["SUPABASE_KEY"]
    GEMINI_API_KEY = st.secrets["GEMINI_API_KEY"]
except KeyError as e:
    st.error(f"Falta la clave {e} en los secretos de Streamlit.")
    st.stop()

# --- CACHE DE RECURSOS ---
@st.cache_resource
def load_resources():
    bert = SentenceTransformer("all-mpnet-base-v2")
    client_gemini = genai.Client(api_key=GEMINI_API_KEY)
    supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
    return bert, client_gemini, supabase

bert_model, gemini_client, supabase_client = load_resources()

# --- SIDEBAR ---
with st.sidebar:
    st.markdown("### 🧰 Activo técnico")
    st.caption("Seleccioná el vehículo sobre el cual querés consultar el manual.")

    vehiculo = st.selectbox(
        "",
        ("fiat_600", "fiat_uno", "citroen_3cv"),
        format_func=lambda x: {
            "fiat_600": "Fiat 600 (La Bolita)",
            "fiat_uno": "Fiat Uno",
            "citroen_3cv": "Citroën 3CV"
        }.get(x)
    )

    st.markdown("---")
    st.caption(
        "Las respuestas se basan **exclusivamente** en los manuales técnicos cargados. "
        "Si un dato no figura explícitamente en el manual, el sistema lo indica."
    )

# --- ENCABEZADO PRINCIPAL ---
st.markdown("## 🛠️ Asistente Técnico de Mantenimiento")
st.markdown(
    "Consulta técnica basada en manuales originales de **Fiat 600**, **Fiat Uno** "
    "y **Citroën 3CV**, utilizando recuperación de información (RAG)."
)

# --- HISTORIAL DE CHAT ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# Mensaje inicial del asistente
if not st.session_state.messages:
    with st.chat_message("assistant"):
        st.markdown(
            "Podés hacer consultas técnicas sobre procedimientos, valores y mantenimiento "
            "según el manual del vehículo seleccionado. "
            "Si un dato no figura en el manual, te lo voy a indicar claramente."
        )

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- LÓGICA DE CONSULTA ---
if prompt := st.chat_input("Escribí tu consulta técnica aquí:"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.spinner("Buscando información en manuales técnicos..."):
        # 1. Mejora de búsqueda: Manejo de números (10000 -> 10.000)
        search_query = prompt
        numeros = re.findall(r'\d+', prompt)
        for num in numeros:
            if len(num) >= 4 and "." not in num:
                formateado = f"{int(num):,}".replace(",", ".")
                search_query += f" {formateado}"

        # 2. Embedding de la consulta
        query_vector = bert_model.encode(search_query).tolist()

        # 3. Buscar en Supabase
        try:
            res = supabase_client.rpc("buscar_manual_especifico", {
                "query_embedding": str(query_vector),
                "match_count": 20,
                "filtro_modelo": vehiculo
            }).execute()

            contexto = "\n---\n".join([item["content"] for item in res.data])
        except Exception as e:
            st.error(f"Error en base de datos: {e}")
            contexto = ""

        # 4. Respuesta con Gemini
        if contexto:
            instruccion = (
                f"Sos un mecánico argentino con amplia experiencia técnica en {vehiculo}. "
                f"Respondé de manera clara, precisa y profesional, utilizando terminología de taller "
                f"argentina de forma moderada y sobria. "
                f"Basá tus respuestas ÚNICAMENTE en la información contenida en los fragmentos del "
                f"manual proporcionados. "
                f"Priorizá datos técnicos verificables como valores numéricos, tablas, tolerancias, "
                f"procedimientos y advertencias del fabricante. "
                f"Si el manual NO especifica explícitamente un dato solicitado, indicá claramente que "
                f"esa información no figura en el manual. "
                f"No inventes valores ni completes información faltante."
            )

            try:
                response = gemini_client.models.generate_content(
                    model="gemini-2.5-flash",
                    config={"system_instruction": instruccion},
                    contents=f"Contexto del manual:\n{contexto}\n\nPregunta: {prompt}"
                )
                answer = response.text
            except Exception as e:
                answer = f"Error en Gemini: {e}"
        else:
            answer = (
                "No encontré información técnica sobre esa consulta en el manual seleccionado. "
                "Probá reformular la pregunta o consultar otro sistema del vehículo."
            )

    with st.chat_message("assistant"):
        st.markdown(answer)

    st.session_state.messages.append({"role": "assistant", "content": answer})



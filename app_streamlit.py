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

# --- CONFIGURACIÓN DE CLAVES ---
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

# --- INTERFAZ DE USUARIO ---
st.title("🛠️ Asistente Técnico de Mantenimiento")

st.write(
    "Consulta técnica basada en **manuales originales** de "
    "**Fiat 600, Fiat Uno y Citroën 3CV**."
)

# 👉 FRASE RAG (AQUÍ VA)
st.caption(
    "📘 Las respuestas se generan exclusivamente a partir de manuales técnicos "
    "originales mediante recuperación semántica (RAG). "
    "Si un dato no figura explícitamente en el manual, el sistema lo indica."
)

st.divider()

vehiculo = st.sidebar.selectbox(
    "Seleccioná el modelo del vehículo:",
    ("fiat_600", "fiat_uno", "citroen_3cv"),
    format_func=lambda x: {
        "fiat_600": "Fiat 600 (La Bolita)",
        "fiat_uno": "Fiat Uno",
        "citroen_3cv": "Citroën 3CV"
    }.get(x)
)

# --- HISTORIAL DE CHAT ---
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- INPUT DEL USUARIO ---
if prompt := st.chat_input("Escribí tu consulta técnica aquí:"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.spinner("Analizando manuales técnicos..."):
        # Normalización de números
        search_query = prompt
        numeros = re.findall(r'\d+', prompt)
        for num in numeros:
            if len(num) >= 4 and "." not in num:
                formateado = f"{int(num):,}".replace(",", ".")
                search_query += f" {formateado}"

        # Embedding
        query_vector = bert_model.encode(search_query).tolist()

        # Búsqueda en Supabase
        try:
            res = supabase_client.rpc(
                "buscar_manual_especifico",
                {
                    "query_embedding": str(query_vector),
                    "match_count": 20,
                    "filtro_modelo": vehiculo
                }
            ).execute()

            contexto = "\n---\n".join(item["content"] for item in res.data)
        except Exception as e:
            st.error(f"Error en la base de datos: {e}")
            contexto = ""

        # Respuesta del modelo
        if contexto:
            system_instruction = (
                f"Sos un técnico mecánico con amplia experiencia en {vehiculo}. "
                f"Respondé de forma clara, precisa y profesional. "
                f"Usá terminología de taller argentino de manera moderada y sobria. "
                f"Basá tus respuestas ÚNICAMENTE en la información contenida en los "
                f"fragmentos del manual proporcionados. "
                f"Priorizá datos técnicos verificables: valores numéricos, tolerancias, "
                f"tablas, procedimientos y advertencias del fabricante. "
                f"Si el manual no especifica explícitamente un dato solicitado, "
                f"indicá claramente que esa información no figura en el manual. "
                f"No inventes valores ni agregues conocimiento externo."
            )

            try:
                response = gemini_client.models.generate_content(
                    model="gemini-2.5-flash",
                    config={"system_instruction": system_instruction},
                    contents=f"Contexto del manual:\n{contexto}\n\nPregunta: {prompt}"
                )
                answer = response.text
            except Exception as e:
                answer = f"Error en Gemini: {e}"
        else:
            answer = (
                "No se encontró información específica sobre esta consulta "
                "en el manual seleccionado."
            )

    with st.chat_message("assistant"):
        st.markdown(answer)

    st.session_state.messages.append(
        {"role": "assistant", "content": answer}
    )




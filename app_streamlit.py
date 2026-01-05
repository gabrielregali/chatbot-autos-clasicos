# -*- coding: utf-8 -*-
import streamlit as st
import re
from google import genai
from sentence_transformers import SentenceTransformer
from supabase import create_client, Client

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(
    page_title="IA Mecánica Clásica", 
    page_icon="🚗",
    layout="centered"
)

# --- CONFIGURACIÓN DE CLAVES (SEGURO PARA STREAMLIT CLOUD) ---
# En Streamlit Cloud, estas claves se cargan desde el panel "Secrets"
try:
    SUPABASE_URL = st.secrets["SUPABASE_URL"]
    SUPABASE_KEY = st.secrets["SUPABASE_KEY"]
    GEMINI_API_KEY = st.secrets["GEMINI_API_KEY"]
except KeyError as e:
    st.error(f"Falta la clave {e} en los secretos de Streamlit.")
    st.stop()

# --- CACHE DE RECURSOS (Versión moderna st.cache_resource) ---
@st.cache_resource
def load_resources():
    # Modelo para Embeddings
    bert = SentenceTransformer("all-mpnet-base-v2")
    # Cliente Gemini (SDK Moderno compatible con 2.5)
    client_gemini = genai.Client(api_key=GEMINI_API_KEY)
    # Cliente Supabase
    supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
    return bert, client_gemini, supabase

bert_model, gemini_client, supabase_client = load_resources()

# --- INTERFAZ DE USUARIO ---
st.title("🚗 Experto en Mecánica")
st.write("Consulta técnica para **Fiat 600, Fiat Uno y Citroën 3CV**.")

vehiculo = st.sidebar.selectbox(
    "Selecciona el modelo del vehículo:",
    ("fiat_600", "fiat_uno", "citroen_3cv"),
    format_func=lambda x: {
        "fiat_600": "Fiat 600 (La Bolita)",
        "fiat_uno": "Fiat Uno",
        "citroen_3cv": "Citroën 3CV"
    }.get(x)
)

# Historial de Chat
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- LÓGICA DE CONSULTA ---
if prompt := st.chat_input("Escribe tu duda técnica aquí:"):
    # Mostrar mensaje del usuario
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.spinner("Buscando en manuales técnicos..."):
        # 1. Mejora de búsqueda: Manejo de números (10000 -> 10.000)
        search_query = prompt
        numeros = re.findall(r'\d+', prompt)
        for num in numeros:
            if len(num) >= 4 and "." not in num:
                formateado = f"{int(num):,}".replace(",", ".")
                search_query += f" {formateado}"

        # 2. Embedding de la consulta
        query_vector = bert_model.encode(search_query).tolist()

        # 3. Buscar en Supabase (Usando el workaround de String para el vector)
        try:
            res = supabase_client.rpc("buscar_manual_especifico", {
                "query_embedding": str(query_vector), # Convertido a string como en Sun Tzu
                "match_count": 20, # Aumentado para captar más tablas
                "filtro_modelo": vehiculo
            }).execute()
            
            contexto = "\n---\n".join([item['content'] for item in res.data])
        except Exception as e:
            st.error(f"Error en base de datos: {e}")
            contexto = ""

        # 4. Respuesta con Gemini 2.5
        if contexto:
            # System Instruction: Definimos la personalidad argentina
            instruccion = (
                    f"Sos un mecánico argentino con amplia experiencia técnica en {vehiculo}. "
                    f"Respondé de manera clara, precisa y profesional, utilizando terminología de taller "
                    f"argentina de forma moderada y sobria. "
                    f"Basá tus respuestas ÚNICAMENTE en la información contenida en los fragmentos del "
                    f"manual proporcionados. "
                    f"Priorizá datos técnicos verificables como valores numéricos, tablas, tolerancias, "
                    f"procedimientos y advertencias del fabricante. "
                    f"Si el manual NO especifica explícitamente un dato solicitado, indicá claramente que "
                    f"esa información no figura en el manual y evitá hacer recomendaciones basadas en "
                    f"experiencia personal o conocimiento externo. "
                    f"No inventes valores ni completes información faltante. "
                    f"Mantené un tono técnico, respetuoso y directo, como el de un mecánico experimentado "
                    f"que explica un procedimiento con seriedad."
            )

            try:
                # Llamada al modelo 2.5 como en tu código de Sun Tzu
                response = gemini_client.models.generate_content(
                    model='gemini-2.5-flash', 
                    config={'system_instruction': instruccion},
                    contents=f"Contexto del manual:\n{contexto}\n\nPregunta: {prompt}"
                )
                answer = response.text
            except Exception as e:
                answer = f"Error en Gemini 2.5: {e}"
        else:
            answer = "¡Epa fiera! No encontré información técnica sobre eso en el manual. ¿Probaste preguntando de otra forma?"

    # Mostrar y guardar respuesta
    with st.chat_message("assistant"):
        st.markdown(answer)

    st.session_state.messages.append({"role": "assistant", "content": answer})


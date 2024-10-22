import streamlit as st
import google.generativeai as genai
from config import GEMINI_API_KEY
import os
import sqlite3

# Cargar el contenido HTML
def load_html(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        return f.read()

# Configuración de Gemini
genai.configure(api_key=GEMINI_API_KEY)

# Configuración del modelo
generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 40,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config=generation_config,
)

# Conectar a la base de datos SQLite
def init_db():
    conn = sqlite3.connect('chatbot.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS student_advising (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_name TEXT,
            student_email TEXT,
            interests TEXT,
            user_input TEXT,
            bot_response TEXT
        )
    ''')
    conn.commit()
    return conn

# Guardar la conversación en la base de datos
def save_conversation(student_name, student_email, interests, user_input, bot_response):
    conn = init_db()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO student_advising (student_name, student_email, interests, user_input, bot_response)
        VALUES (?, ?, ?, ?, ?)
    ''', (student_name, student_email, interests, user_input, bot_response))
    conn.commit()
    conn.close()

# Cargar y mostrar el HTML
html_content = load_html('pagina.html')
st.markdown(html_content, unsafe_allow_html=True)

# Interacción del usuario
student_name = st.text_input("Ingresa tu nombre completo:")
student_email = st.text_input("Ingresa tu correo electrónico:")
interests = st.text_input("¿Cuáles son tus intereses académicos? (ej. Matemáticas, Ciencias, Artes)")

user_input = st.text_input("¿Qué deseas saber sobre carreras universitarias o formación vocacional?")

if user_input:
    # Usar el modelo para generar una respuesta a otras preguntas
    chat_session = model.start_chat(history=[])
    response = chat_session.send_message(user_input)
    
    # Mostrar la respuesta en la aplicación
    st.write(response.text)
    
    # Guardar la conversación en la base de datos
    save_conversation(student_name, student_email, interests, user_input, response.text)

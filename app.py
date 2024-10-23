import streamlit as st
import google.generativeai as genai
from config import GEMINI_API_KEY
import os
import sqlite3
import requests

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
            user_input TEXT,
            bot_response TEXT
        )
    ''')
    conn.commit()
    return conn

# Guardar la conversación en la base de datos
def save_conversation(student_name, user_input, bot_response):
    conn = init_db()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO student_advising (student_name, user_input, bot_response)
        VALUES (?, ?, ?)
    ''', (student_name, user_input, bot_response))
    conn.commit()
    conn.close()

# Estilo del chat emergente
st.markdown("""
    <style>
        .chat-container {
            position: fixed;
            bottom: 20px;
            right: 20px;
            width: 300px;
            height: 400px;
            border: 1px solid #ccc;
            border-radius: 10px;
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
            display: none;
            background-color: white;
            z-index: 1000;
        }
        .chat-header {
            background-color: #4CAF50;
            color: white;
            padding: 10px;
            text-align: center;
            border-top-left-radius: 10px;
            border-top-right-radius: 10px;
        }
        .chat-body {
            padding: 10px;
            overflow-y: auto;
            height: 300px;
        }
        .chat-toggle {
            position: fixed;
            bottom: 20px;
            right: 20px;
            background-color: transparent;
            border: none;
            cursor: pointer;
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
        }
    </style>
    <div class="chat-container" id="chat-container">
        <div class="chat-header">Asistente Vocacional</div>
        <div class="chat-body" id="chat-body">
            <!-- Aquí se mostrarán las respuestas -->
        </div>
    </div>
    <button class="chat-toggle" id="chat-toggle">
        <img src="zorro chat bot.jpg" alt="Logo" style="width: 50px; height: 50px;"/>
    </button>
    <script>
        const chatToggle = document.getElementById('chat-toggle');
        const chatContainer = document.getElementById('chat-container');
        chatToggle.onclick = function() {
            chatContainer.style.display = chatContainer.style.display === 'none' ? 'block' : 'none';
        };
    </script>
""", unsafe_allow_html=True)

# Agregar un título a la aplicación
st.title("Asimov")  # Título de la aplicación

# Interacción del usuario
student_name = st.text_input("¡Hola! Ingresa tu nombre completo para comenzar tu viaje hacia la carrera ideal:")

user_input = st.text_input("Cuéntame, ¿qué es lo que realmente te preocupa sobre tu futuro académico? ¿Tienes dudas sobre qué carrera elegir o cómo enfrentar la incertidumbre? Estoy aquí para escucharte y ayudarte a encontrar claridad en tu camino.")

if user_input:
    # Usar el modelo para analizar las respuestas y recomendar carreras
    chat_session = model.start_chat(history=[])
    response = chat_session.send_message(user_input)  # Enviar la entrada del usuario para análisis
    
    # Mostrar la respuesta en la ventana emergente
    st.markdown(f'<div class="chat-body" id="chat-body">🦊 Respuesta del asistente: {response.text}</div>', unsafe_allow_html=True)
    
    # Sugerir MentorIA como herramienta
    st.write("En nuestra aplicación MentorIA, podemos profundizar más sobre este tema. Tenemos grandes apartados de opciones para ti.")
    
    # Guardar la conversación en la base de datos
    save_conversation(student_name, user_input, response.text)

def respuesta_intereses(intereses):
    if intereses:  # Cambiado 'interests' a 'intereses'
        return f"¡Genial! Te recomiendo usar nuestro recomendador de carreras que utiliza tus intereses y habilidades para encontrar la carrera universitaria que más se ajusta a ti. Puedes explorar más en 'MentorIA'."
    else:
        return "No te preocupes, aquí te ayudamos a descubrir tus habilidades y tu promedio académico con nuestros sencillos tests. ¡Anímate a probarlos y descubre tu potencial!"

# Crear un botón que al hacer clic muestre un mensaje
if st.button('Mostrar alerta'):
    st.write("¡Hola soy Asimov!")

# Manejo de la comunicación con el chatbot
if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = []

# Definición de la función chatbot_response antes de su uso
def chatbot_response(user_input):
    # Lógica para generar la respuesta del chatbot
    return {"response": "Esta es una respuesta de ejemplo."}  # Cambia esto por la lógica real

# Manejo de la comunicación con el chatbot
if st.session_state.get('user_input'):
    user_input = st.session_state.user_input
    if user_input:  # Verificar que user_input no esté vacío
        response = chatbot_response(user_input)  # Aquí se usa user_input
        st.session_state['chat_history'].append({'user': user_input, 'bot': response['response']})

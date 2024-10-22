import google.generativeai as genai
from config import GEMINI_API_KEY

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

def generar_respuesta(prompt):
    chat_session = model.start_chat(history=[])
    response = chat_session.send_message(prompt)
    return response.text

# Ejemplo de uso
if __name__ == "__main__":
    prompt_usuario = "Soy un chatbot diseñado para ayudar a personas de todas las edades a encontrar su camino profesional. Puedes preguntarme sobre carreras universitarias, formación vocacional, universidades, habilidades requeridas y mucho más."
    respuesta = generar_respuesta(prompt_usuario)
    print(respuesta)

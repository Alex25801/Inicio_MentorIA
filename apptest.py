import streamlit as st
import os
import google.generativeai as genai
from config import GEMINI_API_KEY

# Configuración de Gemini
genai.configure(api_key=GEMINI_API_KEY)

def generar_recomendacion(intereses, habilidades, rendimiento):
    # Configuración del modelo
    generation_config = {
        "temperature": 0.7,
        "top_p": 0.95,
        "top_k": 40,
        "max_output_tokens": 1024,
    }
    
    modelo = genai.GenerativeModel(
        model_name="gemini-1.5-flash",
        generation_config=generation_config,
    )
    
    # Definir universidades y carreras según áreas de especialización y continentes
    universidades = {
        "Historia": {
            "Excelente": {
                "América Latina": {
                    "Universidad de Buenos Aires (Argentina)": ["Historia", "Ciencias Sociales"],
                    "Universidad de Chile": ["Historia", "Ciencias Políticas"],
                },
                "Europa": {
                    "Universidad de Oxford (Reino Unido)": ["Historia", "Arqueología"],
                    "Universidad de Cambridge (Reino Unido)": ["Historia", "Antropología"],
                },
                "Asia": {
                    "Universidad de Tokio (Japón)": ["Historia", "Ciencias Sociales"],
                },
            },
            "Bueno": {
                "América Latina": {
                    "Universidad Nacional de La Plata": ["Historia", "Filosofía"],
                },
                "Europa": {
                    "Universidad de Ámsterdam (Países Bajos)": ["Historia", "Ciencias Sociales"],
                },
                "Asia": {
                    "Universidad de Pekín (China)": ["Historia", "Ciencias Políticas"],
                },
            },
            "Promedio": {
                "América Latina": {
                    "Universidad de San Marcos (Perú)": ["Historia", "Ciencias Sociales"],
                },
                "Europa": {
                    "Universidad de Lisboa (Portugal)": ["Historia", "Ciencias Sociales"],
                },
                "Asia": {
                    "Universidad de Seúl (Corea del Sur)": ["Historia", "Ciencias Sociales"],
                },
            },
            "Necesita mejorar": {
                "América Latina": {
                    "Universidad de la Habana (Cuba)": ["Historia", "Ciencias Sociales"],
                },
                "Europa": {
                    "Universidad de Varsovia (Polonia)": ["Historia", "Ciencias Sociales"],
                },
                "Asia": {
                    "Universidad de Manila (Filipinas)": ["Historia", "Ciencias Sociales"],
                },
            },
        },
        "Ciencias Sociales": {
            "Excelente": {
                "América Latina": {
                    "Universidad Nacional Autónoma de México (UNAM)": ["Sociología", "Psicología"],
                },
                "Europa": {
                    "London School of Economics (Reino Unido)": ["Ciencias Sociales", "Economía"],
                },
                "Asia": {
                    "Universidad de Singapur": ["Ciencias Sociales", "Psicología"],
                },
            },
            "Bueno": {
                "América Latina": {
                    "Universidad de los Andes (Colombia)": ["Ciencias Políticas", "Psicología"],
                },
                "Europa": {
                    "Universidad de Ámsterdam (Países Bajos)": ["Ciencias Sociales", "Antropología"],
                },
                "Asia": {
                    "Universidad de Seúl (Corea del Sur)": ["Ciencias Sociales", "Sociología"],
                },
            },
            "Promedio": {
                "América Latina": {
                    "Universidad de Costa Rica": ["Ciencias Sociales", "Psicología"],
                },
                "Europa": {
                    "Universidad de Lisboa (Portugal)": ["Ciencias Sociales", "Antropología"],
                },
                "Asia": {
                    "Universidad de Tailandia": ["Ciencias Sociales", "Psicología"],
                },
            },
            "Necesita mejorar": {
                "América Latina": {
                    "Universidad de la Habana (Cuba)": ["Ciencias Sociales", "Psicología"],
                },
                "Europa": {
                    "Universidad de Varsovia (Polonia)": ["Ciencias Sociales", "Antropología"],
                },
                "Asia": {
                    "Universidad de Manila (Filipinas)": ["Ciencias Sociales", "Psicología"],
                },
            },
        },
        # Agregar más áreas de especialización de manera similar...
    }
    
    # Generar el prompt
    prompt = f"""
    Basándote en la siguiente información de un estudiante:
    
    Intereses: {intereses}
    Habilidades: {habilidades}
    Rendimiento académico: {rendimiento}
    
    Sugiere posibles trayectorias educativas y profesionales. Proporciona al menos 3 opciones 
    con una breve explicación de por qué podrían ser adecuadas.
    """
    
    respuesta = modelo.generate_content(prompt)
    
    # Agregar recomendaciones de universidades y carreras
    recomendaciones = respuesta.text
    area_especializacion = ""
    
    # Determinar el área de especialización basada en los intereses
    for area in universidades.keys():
        if area in intereses:
            area_especializacion = area
            break
    
    if area_especializacion and area_especializacion in universidades:
        universidades_recomendadas = universidades[area_especializacion][rendimiento]
        recomendaciones += f"\n\n**Universidades y carreras recomendadas para estudiar {area_especializacion} con rendimiento {rendimiento}:**\n"
        
        for continente, lista in universidades_recomendadas.items():
            recomendaciones += f"- **{continente}:**\n"
            for universidad, carreras in lista.items():
                recomendaciones += f"  - {universidad}: " + ", ".join(carreras) + "\n"
    
    return recomendaciones

def test_cultura_general():
    st.subheader("Prueba de Cultura General")
    
    preguntas = [
        {
            "pregunta": "¿Cuál es la capital de Francia?",
            "opciones": ["Berlín", "Madrid", "París", "Roma"],
            "respuesta_correcta": "París"
        },
        {
            "pregunta": "¿Cuánto es 15 dividido por 3?",
            "opciones": ["3", "4", "5", "6"],
            "respuesta_correcta": "5"
        },
        {
            "pregunta": "¿Qué órgano del cuerpo humano bombea sangre?",
            "opciones": ["Pulmones", "Hígado", "Corazón", "Riñones"],
            "respuesta_correcta": "Corazón"
        },
        {
            "pregunta": "¿Qué es el PIB?",
            "opciones": ["Producto Interno Bruto", "Producto Internacional Bruto", "Producto Interno Bursátil", "Producto Internacional Bursátil"],
            "respuesta_correcta": "Producto Interno Bruto"
        },
        {
            "pregunta": "¿Cuál es la unidad básica de la vida?",
            "opciones": ["Tejido", "Órgano", "Célula", "Sistema"],
            "respuesta_correcta": "Célula"
        },
        {
            "pregunta": "¿En qué año comenzó la Segunda Guerra Mundial?",
            "opciones": ["1939", "1941", "1945", "1936"],
            "respuesta_correcta": "1939"
        },
        {
            "pregunta": "¿Cuál es el resultado de 7 + 8?",
            "opciones": ["14", "15", "16", "17"],
            "respuesta_correcta": "15"
        },
        {
            "pregunta": "¿Qué tipo de hueso es el fémur?",
            "opciones": ["Hueso largo", "Hueso corto", "Hueso plano", "Hueso irregular"],
            "respuesta_correcta": "Hueso largo"
        },
        {
            "pregunta": "¿Qué es la inflación?",
            "opciones": ["Aumento generalizado de precios", "Disminución de precios", "Estabilidad de precios", "Aumento de la producción"],
            "respuesta_correcta": "Aumento generalizado de precios"
        },
        {
            "pregunta": "¿Cuál es el océano más grande del mundo?",
            "opciones": ["Atlántico", "Índico", "Ártico", "Pacífico"],
            "respuesta_correcta": "Pacífico"
        },
        {
            "pregunta": "¿Quién escribió 'Cien años de soledad'?",
            "opciones": ["Gabriel García Márquez", "Mario Vargas Llosa", "Jorge Luis Borges", "Pablo Neruda"],
            "respuesta_correcta": "Gabriel García Márquez"
        },
        {
            "pregunta": "¿Qué es un número primo?",
            "opciones": ["Un número que solo es divisible por 1 y por sí mismo", "Un número que tiene más de dos divisores", "Un número que termina en 0", "Un número que es par"],
            "respuesta_correcta": "Un número que solo es divisible por 1 y por sí mismo"
        },
        {
            "pregunta": "¿Cuál es la capital de Japón?",
            "opciones": ["Seúl", "Tokio", "Pekín", "Bangkok"],
            "respuesta_correcta": "Tokio"
        },
        {
            "pregunta": "¿Qué es un antiséptico?",
            "opciones": ["Un medicamento para aliviar el dolor", "Una sustancia que previene la infección", "Un tipo de anestesia", "Un tratamiento para enfermedades crónicas"],
            "respuesta_correcta": "Una sustancia que previene la infección"
        },
        {
            "pregunta": "¿Cuál es la raíz cuadrada de 144?",
            "opciones": ["10", "11", "12", "13"],
            "respuesta_correcta": "12"
        },
        {
            "pregunta": "¿Quién fue el primer presidente de los Estados Unidos?",
            "opciones": ["Abraham Lincoln", "George Washington", "Thomas Jefferson", "John Adams"],
            "respuesta_correcta": "George Washington"
        },
        {
            "pregunta": "¿Qué es un mercado?",
            "opciones": ["Un lugar físico para comprar y vender", "Un sistema de intercambio de bienes y servicios", "Un tipo de inversión", "Una forma de ahorro"],
            "respuesta_correcta": "Un sistema de intercambio de bienes y servicios"
        },
        {
            "pregunta": "¿Cuál es el continente más grande del mundo?",
            "opciones": ["África", "Asia", "América", "Europa"],
            "respuesta_correcta": "Asia"
        },
        {
            "pregunta": "¿Qué es la fotosíntesis?",
            "opciones": ["Proceso de respiración", "Proceso de producción de energía en plantas", "Proceso de digestión", "Proceso de reproducción"],
            "respuesta_correcta": "Proceso de producción de energía en plantas"
        },
        {
            "pregunta": "¿Quién fue el líder de la Revolución Francesa?",
            "opciones": ["Napoleón Bonaparte", "Maximilien Robespierre", "Luis XVI", "Georges Danton"],
            "respuesta_correcta": "Maximilien Robespierre"
        },
        {
            "pregunta": "¿Cuál es el país más poblado del mundo?",
            "opciones": ["India", "Estados Unidos", "China", "Indonesia"],
            "respuesta_correcta": "China"
        }
    ]
    
    st.write("Responde las siguientes preguntas:")
    
    respuestas_usuario = {}
    for i, pregunta in enumerate(preguntas):
        respuesta = st.radio(pregunta["pregunta"], pregunta["opciones"], key=f"pregunta_{i}")
        respuestas_usuario[i] = respuesta
    
    if st.button("Verificar respuestas", key="verificar_cultura_general"):
        puntuacion = 0
        for i, pregunta in enumerate(preguntas):
            # Mostrar la pregunta y las opciones
            st.write(f"**{pregunta['pregunta']}**")
            respuesta_usuario = respuestas_usuario[i]
            st.write(f"Tu respuesta: {respuesta_usuario}")
            
            if respuesta_usuario == pregunta["respuesta_correcta"]:
                # Resaltar la respuesta correcta
                st.markdown(f"<div style='background-color: #d4edda; padding: 5px;'>¡Correcto! ✅</div>", unsafe_allow_html=True)
                puntuacion += 1
            else:
                # Mostrar la respuesta correcta si se equivocó
                st.markdown(f"<div style='background-color: #f8d7da; padding: 5px;'>Respuesta correcta: {pregunta['respuesta_correcta']} ❌</div>", unsafe_allow_html=True)
        
        st.success(f"Has obtenido {puntuacion} de {len(preguntas)} puntos.")
        
        # Proporcionar habilidades basadas en la puntuación
        if puntuacion == len(preguntas):
            st.balloons()
            st.write("¡Excelente! Tienes un amplio conocimiento de cultura general.")
            st.write("Habilidades que podrías desarrollar: Historia o Ciencias Sociales.")
        elif puntuacion >= len(preguntas) * 0.75:  # 15 o más
            st.write("Buen trabajo. Tienes un buen nivel de cultura general, pero aún puedes mejorar.")
            st.write("Habilidades que podrías desarrollar:")
            st.write("- Revisa conceptos de historia y geografía.")
            st.write("- Practica más preguntas de matemáticas.")
            st.write("- Lee más sobre biología y anatomía.")
            st.write("Podrías enfocarte en Biología o Economía.")
        elif puntuacion >= len(preguntas) * 0.5:  # 10 a 14
            st.write("Hay espacio para mejorar. Te recomendamos estudiar más sobre estos temas.")
            st.write("Habilidades que podrías desarrollar:")
            st.write("- Dedica tiempo a estudiar historia y geografía.")
            st.write("- Practica ejercicios de matemáticas regularmente.")
            st.write("- Lee libros o artículos sobre biologa y anatomía.")
            st.write("- Considera unirte a grupos de estudio o foros en línea para discutir estos temas.")
            st.write("Podrías enfocarte en Matemáticas o Ciencias de la Salud.")
        else:  # Menos de 10
            st.write("Es un buen momento para reflexionar sobre tus intereses y áreas de mejora.")
            st.write("Habilidades que podrías desarrollar:")
            st.write("- Dedica tiempo a estudiar historia y geografía.")
            st.write("- Practica ejercicios de matemáticas regularmente.")
            st.write("- Lee libros o artículos sobre biología y anatomía.")
            st.write("- Considera unirte a grupos de estudio o foros en línea para discutir estos temas.")
            st.write("Podrías enfocarte en Educación o Ciencias Sociales.")
        
        # Mensaje motivacional
        st.write("Recuerda que el conocimiento es poder. Cada esfuerzo que hagas para aprender más te acercará a tus metas. ¡Sigue adelante y nunca dejes de aprender!")

def cuestionario_habilidades():
    st.subheader("Cuestionario de Habilidades Fuertes y Blandas")
    
    respuestas = {}
    
    preguntas = [
        "¿Cómo prefieres trabajar en un proyecto?",
        "Cuando enfrentas un problema, ¿cómo sueles abordarlo?",
        "¿Qué tipo de tareas disfrutas más?",
        "¿Cmo te sientes al hablar en público?",
        "Cuando trabajas en grupo, ¿qué rol sueles asumir?",
        "¿Cómo manejas el estrés o la presión?",
        "¿Qué tan importante es para ti ayudar a los demás?",
        "¿Cómo te sientes al aprender cosas nuevas?",
        "¿Qué tipo de feedback prefieres recibir?",
        "¿Qué habilidades crees que son más importantes para tu futuro?"
    ]
    
    opciones = [
        ["Solo", "En un equipo", "No tengo preferencia"],
        ["Analizo datos", "Consulto con otros", "Confío en mi intuición"],
        ["Tareas técnicas", "Tareas creativas", "Tareas interpersonales"],
        ["Muy cómodo", "Algo nervioso", "Muy incómodo"],
        ["Líder", "Mediador", "Ejecutor"],
        ["Me mantengo enfocado", "Hablo con alguien", "Me relajo"],
        ["Muy importante", "Algo importante", "No es prioridad"],
        ["Emocionado", "Nervioso", "Indiferente"],
        ["Crítico y directo", "Positivo y motivador", "Constructivo"],
        ["Habilidades técnicas", "Habilidades interpersonales", "Habilidades de gestión"]
    ]
    
    for i, pregunta in enumerate(preguntas):
        respuesta = st.radio(pregunta, opciones[i], key=f"pregunta_habilidad_{i}")
        respuestas[i] = respuesta
    
    if st.button("Enviar respuestas", key="enviar_habilidades"):
        st.write("Tus respuestas:")
        for i, respuesta in respuestas.items():
            st.write(f"{preguntas[i]}: {respuesta}")
        
        # Análisis de habilidades
        habilidades = analizar_habilidades(respuestas)
        st.subheader("Análisis de Habilidades")
        st.write(habilidades)

def analizar_habilidades(respuestas):
    habilidades_descubiertas = []
    explicaciones = []
    fortalezas = []
    areas_mejora = []

    # Evaluar respuestas y generar explicaciones
    if respuestas[0] == "Leer libros":
        habilidades_descubiertas.append("Lectura crítica")
        explicaciones.append(
            "Leer libros no solo mejora tu capacidad de análisis y comprensión, "
            "sino que también te expone a nuevas ideas y perspectivas. "
            "Esto es fundamental en cualquier carrera que requiera investigación o comunicación, "
            "ya que te permite abordar problemas desde diferentes ángulos."
        )
        fortalezas.append("Tienes una inclinación hacia el aprendizaje y la reflexión, "
                         "lo que te permite adquirir nuevos conocimientos de manera efectiva.")

    if respuestas[1] == "Comunicación":
        habilidades_descubiertas.append("Habilidades de comunicación")
        explicaciones.append(
            "La comunicación efectiva es esencial en casi todas las profesiones. "
            "Facilita la colaboración y la comprensión entre colegas, lo que puede llevar a un ambiente de trabajo más armonioso. "
            "Desarrollar esta habilidad te ayudará a construir relaciones sólidas y a ser un líder más efectivo."
        )
        fortalezas.append("Tienes la capacidad de conectar con los demás, "
                         "lo que te permite construir relaciones sólidas en el trabajo.")

    # Continúa con el resto de las respuestas y explicaciones de manera similar...
    # Generar un mensaje de retroalimentación
    mensaje = "### Análisis de tus Habilidades\n\n"
    mensaje += "#### Fortalezas:\n"
    if fortalezas:
        mensaje += "- " + "\n- ".join(fortalezas) + "\n\n"
    else:
        mensaje += "No se identificaron fortalezas específicas.\n\n"

    mensaje += "#### Áreas de Mejora:\n"
    if areas_mejora:
        mensaje += "- " + "\n- ".join(areas_mejora) + "\n\n"
    else:
        mensaje += "No se identificaron áreas de mejora específicas.\n\n"

    mensaje += "#### Habilidades Descubiertas:\n"
    if habilidades_descubiertas:
        mensaje += "- " + "\n- ".join(habilidades_descubiertas) + "\n\n"
        mensaje += "#### Explicaciones:\n"
        for exp in explicaciones:
            mensaje += f"- {exp}\n"
    else:
        mensaje += "Parece que no has seleccionado opciones que indiquen habilidades específicas. ¡Reflexiona sobre tus respuestas y considera qué áreas te gustaría explorar más!"

    mensaje += "\n### Reflexiones Finales\n"
    mensaje += (
        "Recuerda que el autoconocimiento es un viaje continuo. Es normal enfrentar desafíos y tener dudas en el camino. "
        "Tus fortalezas son un gran recurso que puedes utilizar para avanzar, mientras que las áreas de mejora son oportunidades "
        "para crecer y aprender. No dudes en buscar apoyo cuando lo necesites, ya sea de amigos, familiares o profesionales. "
        "Cada paso que tomes hacia el autoconocimiento y el desarrollo personal es valioso. ¡Sigue adelante y confía en ti mismo!"
    )

    return mensaje

def preguntas_api():
    st.subheader("Descubre tus Habilidades")

    st.write("¡Hola! Estoy aquí para ayudarte a descubrir tus habilidades y cómo pueden influir en tu trayectoria educativa y profesional. Responde las siguientes preguntas para que podamos conocerte mejor.")

    preguntas = [
        {
            "pregunta": "¿Qué actividad disfrutas más en tu tiempo libre?",
            "opciones": ["Leer libros", "Hacer ejercicio", "Jugar videojuegos", "Cocinar"],
            "explicacion": "Esta pregunta nos ayuda a entender tus intereses y pasiones, que son fundamentales para tu desarrollo personal."
        },
        {
            "pregunta": "¿Cuál de las siguientes habilidades consideras ms importante para tu carrera?",
            "opciones": ["Comunicación", "Análisis de datos", "Creatividad", "Liderazgo"],
            "explicacion": "Identificar tus habilidades clave puede guiarte hacia una carrera que se alinee con tus fortalezas."
        },
        {
            "pregunta": "Cuando enfrentas un problema, ¿cómo sueles resolverlo?",
            "opciones": ["Analizo la situación", "Pido ayuda a otros", "Confío en mi intuición", "Busco información"],
            "explicacion": "Tu enfoque para resolver problemas puede revelar mucho sobre tu estilo de trabajo y tu capacidad de adaptación."
        },
        {
            "pregunta": "¿Qué tipo de trabajo prefieres?",
            "opciones": ["Trabajo en equipo", "Trabajo individual", "Trabajo en un entorno dinámico", "Trabajo estructurado"],
            "explicacion": "Conocer tu preferencia de trabajo puede ayudarte a encontrar un entorno laboral que te motive."
        },
        {
            "pregunta": "¿Qué te motiva más en tu vida cotidiana?",
            "opciones": ["Aprender cosas nuevas", "Ayudar a los demás", "Lograr mis metas personales", "Disfrutar de mis pasatiempos"],
            "explicacion": "Entender tus motivaciones puede guiarte hacia una carrera que te brinde satisfacción y propósito."
        },
        {
            "pregunta": "¿Cómo te sientes al trabajar bajo presión?",
            "opciones": ["Me gusta el desafío", "Me estresa un poco", "Prefiero un ambiente tranquilo", "No me importa"],
            "explicacion": "Tu respuesta a esta pregunta puede indicar cómo manejas situaciones desafiantes en el trabajo."
        },
        {
            "pregunta": "¿Qué tipo de feedback prefieres recibir?",
            "opciones": ["Crítico y directo", "Positivo y motivador", "Constructivo y equilibrado", "No me gusta recibir feedback"],
            "explicacion": "Saber cómo prefieres recibir feedback puede ayudarte a crecer y mejorar en tu carrera."
        },
        {
            "pregunta": "¿Cuál es tu estilo de aprendizaje preferido?",
            "opciones": ["Visual", "Auditivo", "Kinestésico", "Lectura/escritura"],
            "explicacion": "Conocer tu estilo de aprendizaje puede ayudarte a elegir métodos de estudio que te beneficien."
        },
        {
            "pregunta": "¿Qué habilidades crees que son más importantes para tu futuro?",
            "opciones": ["Habilidades técnicas", "Habilidades interpersonales", "Habilidades de gestión", "Habilidades creativas"],
            "explicacion": "Identificar las habilidades que valoras puede guiarte en tu desarrollo profesional."
        },
        {
            "pregunta": "¿Cómo te sientes al aprender cosas nuevas?",
            "opciones": ["Emocionado", "Nervioso", "Indiferente", "Frustrado"],
            "explicacion": "Tu actitud hacia el aprendizaje puede influir en tu crecimiento personal y profesional."
        },
        {
            "pregunta": "¿Cuál ha sido tu mayor fracaso y qué aprendiste de él?",
            "opciones": ["No he tenido fracasos significativos", "Un proyecto que no salió como esperaba", "Una relación que no funcionó", "Un examen que no aprobé"],
            "explicacion": "Reflexionar sobre los fracasos puede ayudarte a identificar áreas de mejora y crecimiento."
        },
        {
            "pregunta": "¿Qué te impide alcanzar tus metas?",
            "opciones": ["Falta de tiempo", "Miedo al fracaso", "Falta de apoyo", "No estoy seguro de mis metas"],
            "explicacion": "Identificar obstáculos puede ser el primer paso para superarlos y avanzar hacia tus objetivos."
        },
        {
            "pregunta": "¿Cómo manejas la crítica o el rechazo?",
            "opciones": ["Lo tomo de manera constructiva", "Me siento herido", "Lo ignoro", "Me motiva a mejorar"],
            "explicacion": "Entender cómo manejas la crítica puede ayudarte a desarrollar una mentalidad más resiliente."
        },
    ]
    
    respuestas_usuario = {}
    for i, pregunta in enumerate(preguntas):
        st.write(f"**{pregunta['pregunta']}**")
        st.write(f"*{pregunta['explicacion']}*")  # Explicación de la pregunta
        respuesta = st.radio("Selecciona una opción:", pregunta["opciones"], key=f"pregunta_api_{i}")
        respuestas_usuario[i] = respuesta
    
    if st.button("Enviar respuestas", key="enviar_api"):
        # Análisis de habilidades
        habilidades = analizar_habilidades(respuestas_usuario)
        st.subheader("Análisis de Habilidades")
        st.write(habilidades)

# Interfaz de Streamlit
col1, col2 = st.columns([4, 1])

with col1:
    st.title("Recomendador de Trayectorias Educativas y Profesionales")
with col2:
    st.image("descarga.jpeg", width=100)

# Crear pestañas
tab1, tab2, tab3, tab4 = st.tabs(["Prueba de Cultura General", "Recomendación", "Habilidades", "Preguntas API"])

with tab1:
    test_cultura_general()

with tab2:
    intereses = st.text_area("Ingresa tus intereses (separados por comas):")
    habilidades = st.text_area("Ingresa tus habilidades (separadas por comas):")
    rendimiento = st.selectbox("Selecciona tu rendimiento académico:", 
                               ["Excelente", "Bueno", "Promedio", "Necesita mejorar"])

    if st.button("Generar recomendación", key="generar_recomendacion"):
        if intereses and habilidades:
            with st.spinner("Generando recomendaciones..."):
                recomendacion = generar_recomendacion(intereses, habilidades, rendimiento)
            st.subheader("Recomendaciones:")
            st.write(recomendacion)
        else:
            st.warning("Por favor, ingresa tus intereses y habilidades.")

with tab3:
    cuestionario_habilidades()

with tab4:
    preguntas_api()

# Sidebar con instrucciones
st.sidebar.markdown(""" 
<div style="background-color: #E0E0E0; padding: 10px; border-radius: 5px;">
<h2 style="color: black;">Cómo usar esta herramienta:</h2>

1. **Prueba de Cultura General:** Responde a una serie de preguntas sobre diversos temas. 
   - Al finalizar, recibirás una puntuación y sugerencias sobre habilidades que puedes desarrollar.
   - Las preguntas abarcan áreas como matemáticas, biología, historia y geografía.

2. **Generador de Recomendaciones:** Ingresa tus intereses y habilidades.
   - Selecciona tu rendimiento académico.
   - Haz clic en "Generar recomendación" para recibir sugerencias sobre posibles trayectorias educativas y profesionales.
   - Las recomendaciones incluirán universidades relevantes de América Latina, Europa, Asia y otros continentes, junto con las carreras que ofrecen.
po
3. **Cuestionario de Habilidades:** Responde a preguntas sobre tus preferencias y habilidades.
   - Este cuestionario te ayudará a identificar tus habilidades fuertes y blandas.
   - Al finalizar, recibirás un análisis que destaca en qué áreas podrías sobresalir, basado en tus respuestas.

4. **Preguntas API:** Responde a preguntas relacionadas con aptitudes, razonamiento lógico y velocidad cognitiva.
   - Al finalizar, recibirás una puntuación que refleja tu rendimiento en estas áreas.

La IA analizará tu información y sugerirá posibles trayectorias educativas y profesionales.
</div>
""", unsafe_allow_html=True)

# Estilo CSS para cambiar el fondo a gris y todas las letras a negro
st.markdown(
    """
    <style>
    .stApp {
        background-color: #D3D3D3; /* Fondo gris */
        color: #000000; /* Texto negro */
    }
    .stButton > button {
        background-color: #FF6347; /* Tomate */
        color: white; /* Color del texto del botón */
    }
    .stTextInput > div > div > input {
        background-color: #A9A9A9; /* Fondo de input gris oscuro */
        color: black; /* Texto negro en input */
    }
    .stTextArea > div > div > textarea {
        background-color: #A9A9A9; /* Fondo de textarea gris oscuro */
        color: black; /* Texto negro en textarea */
    }
    .stSelectbox > div > div > select {
        background-color: #A9A9A9; /* Fondo de selectbox gris oscuro */
        color: black; /* Texto negro en selectbox */
    }
    /* Asegurarse de que todas las letras sean negras */
    h1, h2, h3, h4, h5, h6, p, li, span {
        color: #000000; /* Texto negro para encabezados y párrafos */
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Estilo CSS para cambiar el texto a negro en la sección de instrucciones
st.markdown(
    """
    <style>
    .instrucciones {
        color: #000000; /* Texto negro */
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Estilo CSS para cambiar el texto a negro en la pestaña "Cómo utilizar la herramienta"
st.markdown(
    """
    <style>
    .como-utilizar {
        color: #000000; /* Texto negro */
    }
    </style>
    """,
    unsafe_allow_html=True
)

# En la sección de "Cómo utilizar la herramienta"
st.subheader("Cómo utilizar la herramienta")
st.markdown('<div class="como-utilizar">Aquí puedes incluir instrucciones sobre cómo usar la herramienta. Asegúrate de seguir los pasos indicados para obtener los mejores resultados.</div>', unsafe_allow_html=True)

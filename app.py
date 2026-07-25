import streamlit as st
import random

# Configuración de la página
st.set_page_config(page_title="Juego de Preguntas & Penitencias", page_icon="🎮", layout="centered")

# --- LISTA DE PENITENCIAS ---
PENITENCIAS = [
    "🎤 Cantar el coro de tu canción favorita usando solo la letra 'la la la'.",
    "🎭 Hacer una imitación de un animal o personaje famoso durante 15 segundos.",
    "💃 Hacer un baile gracioso de 10 segundos sin música.",
    "📜 Decir un trabalenguas rápido tres veces seguidas sin equivocarte.",
    "🤭 Contar un chiste con la voz más grave o fina que puedas.",
    "🤳 Decir 3 virtudes o cosas buenas sobre el otro jugador.",
    "🤖 Hablar como un robot o con acento divertido durante el siguiente turno.",
    "🙈 Hacer 5 flexiones de pecho o 10 saltos de tijera.",
    "🎨 Dibujar un retrato rápido del otro jugador en un papel en 20 segundos.",
    "🗿 Quedarte como una estatua sin pestañear ni moverte durante 15 segundos.",
    "🎩 Inventar un poema rimbombante de 2 versos sobre un objeto de la habitación.",
    "🤐 Intentar tararear una canción manteniendo la boca abierta.",
    "🧼 Decir 5 cosas que hay en un baño en menos de 5 segundos.",
    "👑 Tratar al otro jugador como 'Su Majestad' durante el próximo turno.",
    "🐸 Hacer 5 saltos de rana cruzando la habitación.",
    "🧐 Decir el alfabeto al revés empezando desde la Z hasta la P.",
    "🤝 Hacerle un cumplido sincero al otro jugador mirándolo fijamente.",
    "🦕 Hacer la caminata y el rugido de un dinosaurio por 10 segundos."
]

# Inicialización de estados de sesión (Session State)
if "etapa" not in st.session_state:
    st.session_state.etapa = "registro"
if "jugadores" not in st.session_state:
    st.session_state.jugadores = []
if "preguntas" not in st.session_state:
    st.session_state.preguntas = []
if "puntos" not in st.session_state:
    st.session_state.puntos = {}
if "turno_index" not in st.session_state:
    st.session_state.turno_index = 0
if "pregunta_actual" not in st.session_state:
    st.session_state.pregunta_actual = ""

st.title("🎮 Preguntas & Penitencias")

# --- ETAPA 1: REGISTRO DE JUGADORES ---
if st.session_state.etapa == "registro":
    st.subheader("👤 Registro de Jugadores")
    j1 = st.text_input("Nombre del Jugador 1:")
    j2 = st.text_input("Nombre del Jugador 2:")

    if st.button("Continuar ➡️", use_container_width=True):
        if j1.strip() and j2.strip():
            st.session_state.jugadores = [j1.strip(), j2.strip()]
            st.session_state.puntos = {j1.strip(): 0, j2.strip(): 0}
            st.session_state.etapa = "preguntas"
            st.rerun()
        else:
            st.warning("⚠️ Por favor ingresa ambos nombres.")

# --- ETAPA 2: INGRESO DE PREGUNTAS ---
elif st.session_state.etapa == "preguntas":
    st.subheader("📝 Banco de Preguntas")
    st.write("Agreguen todas las preguntas que deseen para la partida.")

    nueva_p = st.text_input("Escribe una pregunta y presiona 'Agregar':")
    if st.button("➕ Agregar Pregunta"):
        if nueva_p.strip():
            st.session_state.preguntas.append(nueva_p.strip())
            st.success("¡Pregunta agregada!")
        else:
            st.warning("La pregunta no puede estar vacía.")

    if st.session_state.preguntas:
        st.write(f"**Preguntas guardadas ({len(st.session_state.preguntas)}):**")
        for p in st.session_state.preguntas:
            st.text(f"• {p}")

    if st.button("🚀 ¡Empezar el Juego!", type="primary", use_container_width=True):
        if len(st.session_state.preguntas) > 0:
            st.session_state.turno_index = random.randint(0, 1)
            st.session_state.etapa = "juego"
            st.rerun()
        else:
            st.error("Debes ingresar al menos una pregunta para empezar.")

# --- ETAPA 3: DINÁMICA DEL JUEGO ---
elif st.session_state.etapa == "juego":
    # Mostrar Puntos
    col1, col2 = st.columns(2)
    j1, j2 = st.session_state.jugadores
    col1.metric(j1, f"{st.session_state.puntos[j1]} pts")
    col2.metric(j2, f"{st.session_state.puntos[j2]} pts")
    st.divider()

    if not st.session_state.preguntas:
        st.session_state.etapa = "final"
        st.rerun()

    jugador_actual = st.session_state.jugadores[st.session_state.turno_index]

    if not st.session_state.pregunta_actual:
        st.session_state.pregunta_actual = random.choice(st.session_state.preguntas)

    st.subheader(f"🎯 Turno de: {jugador_actual.upper()}")
    st.info(f"❓ **Pregunta:** {st.session_state.pregunta_actual}")

    st.write("¿Respondió correctamente?")
    btn_col1, btn_col2 = st.columns(2)

    if btn_col1.button("✅ SÍ (Punto)", use_container_width=True):
        st.session_state.puntos[jugador_actual] += 1
        st.toast(f"🎉 ¡Punto para {jugador_actual}!")
        st.session_state.preguntas.remove(st.session_state.pregunta_actual)
        st.session_state.pregunta_actual = ""
        st.session_state.turno_index = 1 - st.session_state.turno_index
        st.rerun()

    if btn_col2.button("❌ NO (Penitencia)", use_container_width=True):
        penitencia = random.choice(PENITENCIAS)
        st.error(f"🔥 **PENITENCIA PARA {jugador_actual.upper()}:**\n\n👉 {penitencia}")
        st.session_state.preguntas.remove(st.session_state.pregunta_actual)
        st.session_state.pregunta_actual = ""
        st.session_state.turno_index = 1 - st.session_state.turno_index

        if st.button("Siguiente Turno ➡️"):
            st.rerun()

# --- ETAPA 4: RESULTADOS FINALES ---
elif st.session_state.etapa == "final":
    st.balloons()
    st.title("🏁 ¡Fin del Juego!")

    j1, j2 = st.session_state.jugadores
    pts1 = st.session_state.puntos[j1]
    pts2 = st.session_state.puntos[j2]

    st.write("### 🏆 Puntuación Final:")
    st.write(f"• **{j1}:** {pts1} puntos")
    st.write(f"• **{j2}:** {pts2} puntos")

    if pts1 > pts2:
        st.success(f"🎉 ¡El ganador es {j1}!")
    elif pts2 > pts1:
        st.success(f"🎉 ¡El ganador es {j2}!")
    else:
        st.info("🤝 ¡Es un empate!")

    if st.button("Reiniciar Juego 🔄"):
        st.session_state.etapa = "registro"
        st.session_state.preguntas = []
        st.session_state.pregunta_actual = ""
        st.rerun()
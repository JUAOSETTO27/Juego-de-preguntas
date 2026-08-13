import streamlit as st
import random
import json

# Configuración de la página
st.set_page_config(page_title="Trivia & Penitencias", page_icon="🎮", layout="centered")

# --- LISTA DE PENITENCIAS ---
PENITENCIAS = [
    "🎤 Cantar el coro de tu canción favorita usando solo la letra 'la la la'.",
    "🎭 Hacer una imitación de un animal o personaje famoso durante 15 segundos.",
    "💃 Hacer un baile gracioso de 10 segundos sin música.",
    "📜 Decir un trabalenguas rápido tres veces seguidas sin equivocarte.",
    "🤭 Contar un chiste con la voz más grave o fina que puedas.",
    "🤳 Decir 3 virtudes o cosas buenas sobre otro jugador (o de ti mismo si juegas solo).",
    "🤖 Hablar como un robot o con acento divertido durante el siguiente turno.",
    "🙈 Hacer 5 flexiones de pecho o 10 saltos de tijera.",
    "🎨 Dibujar un retrato rápido en un papel en 20 segundos.",
    "🗿 Quedarte como una estatua sin pestañear ni moverte durante 15 segundos.",
    "🎩 Inventar un poema rimbombante de 2 versos sobre un objeto cercano.",
    "🤐 Intentar tararear una canción manteniendo la boca abierta.",
    "🧼 Decir 5 cosas que hay en un baño en menos de 5 segundos.",
    "👑 Hablar como la realeza ('Su Majestad') durante el próximo turno.",
    "🐸 Hacer 5 saltos de rana cruzando el lugar.",
    "🧐 Decir el alfabeto al revés empezando desde la Z hasta la P.",
    "🤝 Hacer un cumplido sincero mirando fijamente a alguien o a la cámara.",
    "🦕 Hacer la caminata y el rugido de un dinosaurio por 10 segundos."
]

# Inicialización de estado
if "etapa" not in st.session_state:
    st.session_state.etapa = "registro"
if "jugadores" not in st.session_state:
    st.session_state.jugadores = []
if "preguntas" not in st.session_state:
    st.session_state.preguntas = []  # Lista de dicts: {"pregunta", "correcta", "incorrectas"}
if "puntos" not in st.session_state:
    st.session_state.puntos = {}
if "intentos" not in st.session_state:
    st.session_state.intentos = {}
if "turno_index" not in st.session_state:
    st.session_state.turno_index = 0
if "pregunta_actual" not in st.session_state:
    st.session_state.pregunta_actual = None
if "opciones_actuales" not in st.session_state:
    st.session_state.opciones_actuales = []

st.title("🎮 Trivia & Penitencias")

# --- MENÚ SUPERIOR: GUARDAR Y CARGAR PROGRESO ---
with st.sidebar:
    st.header("💾 Gestión de Sesión")
    
    # 1. Introducir Progreso (Cargar)
    st.subheader("📥 Introducir progreso")
    codigo_progreso = st.text_area("Pega aquí tu código de guardado:")
    if st.button("Cargar partida"):
        if codigo_progreso.strip():
            try:
                data = json.loads(codigo_progreso.strip())
                st.session_state.jugadores = data.get("jugadores", [])
                st.session_state.preguntas = data.get("preguntas", [])
                st.session_state.puntos = data.get("puntos", {})
                st.session_state.intentos = data.get("intentos", {})
                st.session_state.turno_index = data.get("turno_index", 0)
                st.session_state.etapa = data.get("etapa", "juego")
                st.session_state.pregunta_actual = None
                st.success("¡Progreso cargado con éxito!")
                st.rerun()
            except Exception:
                st.error("El código introducido no es válido.")
        else:
            st.warning("Pega un código de progreso antes de cargar.")

    st.divider()

    # 2. Generar Código de Guardado
    if st.session_state.jugadores:
        st.subheader("📤 Exportar progreso")
        estado_dict = {
            "jugadores": st.session_state.jugadores,
            "preguntas": st.session_state.preguntas,
            "puntos": st.session_state.puntos,
            "intentos": st.session_state.intentos,
            "turno_index": st.session_state.turno_index,
            "etapa": st.session_state.etapa
        }
        json_str = json.dumps(estado_dict)
        st.code(json_str, language="json")
        st.caption("Copia este código para introducirlo en tu próxima sesión.")


# --- ETAPA 1: REGISTRO DE JUGADORES ---
if st.session_state.etapa == "registro":
    st.subheader("👥 Registro de Jugadores")
    st.write("Añade de 1 a N jugadores para comenzar.")

    if "temp_jugadores" not in st.session_state:
        st.session_state.temp_jugadores = []

    nuevo_jugador = st.text_input("Nombre del jugador:")
    if st.button("➕ Añadir Jugador"):
        if nuevo_jugador.strip():
            if nuevo_jugador.strip() not in st.session_state.temp_jugadores:
                st.session_state.temp_jugadores.append(nuevo_jugador.strip())
                st.success(f"¡{nuevo_jugador.strip()} añadido!")
            else:
                st.warning("Este jugador ya está registrado.")
        else:
            st.warning("Escribe un nombre válido.")

    if st.session_state.temp_jugadores:
        st.write("**Jugadores registrados:**")
        for j in st.session_state.temp_jugadores:
            st.text(f"• {j}")

        if st.button("Continuar a Preguntas ➡️", type="primary", use_container_width=True):
            st.session_state.jugadores = list(st.session_state.temp_jugadores)
            st.session_state.puntos = {j: 0 for j in st.session_state.jugadores}
            st.session_state.intentos = {j: 0 for j in st.session_state.jugadores}
            st.session_state.etapa = "preguntas"
            st.rerun()


# --- ETAPA 2: INGRESO DE PREGUNTAS CON OPCIÓN MÚLTIPLE ---
elif st.session_state.etapa == "preguntas":
    st.subheader("📝 Crear Preguntas (Opción Múltiple)")
    st.write("Crea preguntas con su respuesta correcta y opciones incorrectas.")

    with st.form("form_pregunta", clear_on_submit=True):
        preg_txt = st.text_input("Enunciado de la pregunta:")
        resp_corr = st.text_input("✅ Respuesta Correcta:")
        resp_inc1 = st.text_input("❌ Opción Incorrecta 1:")
        resp_inc2 = st.text_input("❌ Opción Incorrecta 2 (Opcional):")
        resp_inc3 = st.text_input("❌ Opción Incorrecta 3 (Opcional):")

        submitted = st.form_submit_button("➕ Guardar Pregunta")
        if submitted:
            if preg_txt.strip() and resp_corr.strip() and resp_inc1.strip():
                incorrectas = [i.strip() for i in [resp_inc1, resp_inc2, resp_inc3] if i.strip()]
                st.session_state.preguntas.append({
                    "pregunta": preg_txt.strip(),
                    "correcta": resp_corr.strip(),
                    "incorrectas": incorrectas
                })
                st.success("¡Pregunta agregada exitosamente!")
            else:
                st.error("Debes ingresar la pregunta, la respuesta correcta y al menos 1 opción incorrecta.")

    if st.session_state.preguntas:
        st.write(f"**Preguntas cargadas ({len(st.session_state.preguntas)}):**")
        for idx, p in enumerate(st.session_state.preguntas, 1):
            st.text(f"{idx}. {p['pregunta']} (Correcta: {p['correcta']})")

    if st.button("🚀 ¡Empezar el Juego!", type="primary", use_container_width=True):
        if len(st.session_state.preguntas) > 0:
            st.session_state.turno_index = random.randint(0, len(st.session_state.jugadores) - 1)
            st.session_state.etapa = "juego"
            st.rerun()
        else:
            st.error("Agrega al menos una pregunta para poder jugar.")


# --- ETAPA 3: DINÁMICA DEL JUEGO ---
elif st.session_state.etapa == "juego":
    # Mostrar Marcador de Puntos
    cols = st.columns(len(st.session_state.jugadores))
    for idx, jug in enumerate(st.session_state.jugadores):
        pts = st.session_state.puntos[jug]
        tot = st.session_state.intentos[jug]
        porcentaje = int((pts / tot) * 100) if tot > 0 else 0
        cols[idx % len(cols)].metric(jug, f"{pts} pts", f"{porcentaje}% efec.")

    st.divider()

    if not st.session_state.preguntas:
        st.session_state.etapa = "final"
        st.rerun()

    jugador_actual = st.session_state.jugadores[st.session_state.turno_index]

    # Cargar nueva pregunta si no hay una activa
    if st.session_state.pregunta_actual is None:
        p_obj = random.choice(st.session_state.preguntas)
        st.session_state.pregunta_actual = p_obj
        
        # Combinar y mezclar opciones
        opciones = [p_obj["correcta"]] + p_obj["incorrectas"]
        random.shuffle(opciones)
        st.session_state.opciones_actuales = opciones

    p_curr = st.session_state.pregunta_actual

    st.subheader(f"🎯 Turno de: {jugador_actual.upper()}")
    st.info(f"❓ **Pregunta:** {p_curr['pregunta']}")

    st.write("Selecciona tu respuesta:")
    
    # Crear un botón por cada opción de respuesta
    for opcion in st.session_state.opciones_actuales:
        if st.button(opcion, key=f"btn_{opcion}", use_container_width=True):
            st.session_state.intentos[jugador_actual] += 1
            
            if opcion == p_curr["correcta"]:
                st.session_state.puntos[jugador_actual] += 1
                st.toast(f"🎉 ¡CORRECTO! Punto para {jugador_actual}")
            else:
                penitencia = random.choice(PENITENCIAS)
                st.error(f"❌ **INCORRECTO.** La respuesta correcta era: **{p_curr['correcta']}**")
                st.warning(f"🔥 **PENITENCIA PARA {jugador_actual.upper()}:**\n\n👉 {penitencia}")

            # Remover la pregunta usada y pasar turno
            st.session_state.preguntas.remove(p_curr)
            st.session_state.pregunta_actual = None
            st.session_state.opciones_actuales = []
            st.session_state.turno_index = (st.session_state.turno_index + 1) % len(st.session_state.jugadores)

            if st.button("Siguiente Turno ➡️"):
                st.rerun()


# --- ETAPA 4: RESULTADOS FINALES Y EFECTIVIDAD ---
elif st.session_state.etapa == "final":
    st.balloons()
    st.title("🏁 ¡Fin del Juego!")
    st.write("Se han respondido todas las preguntas.")

    st.subheader("📊 Tabla de Desempeño")

    # Tabla con cálculos de precisión/efectividad
    resultados = []
    for jug in st.session_state.jugadores:
        pts = st.session_state.puntos[jug]
        tot = st.session_state.intentos[jug]
        pct = (pts / tot * 100) if tot > 0 else 0
        
        # Asignar Rango/Insignia según efectividad
        if pct == 100:
            rango = "🥇 Maestro de la Trivia"
        elif pct >= 70:
            rango = "🥈 Sabio Aceptable"
        elif pct >= 40:
            rango = "🥉 En riesgo de Penitencia"
        else:
            rango = "🔥 Rey de las Penitencias"

        resultados.append({"Jugador": jug, "Puntos": pts, "Respondidas": tot, "Efectividad": f"{pct:.1f}%", "Rango": rango})

    st.table(resultados)

    if st.button("Reiniciar Nueva Partida 🔄", type="primary"):
        st.session_state.etapa = "registro"
        st.session_state.jugadores = []
        st.session_state.temp_jugadores = []
        st.session_state.preguntas = []
        st.session_state.pregunta_actual = None
        st.rerun()

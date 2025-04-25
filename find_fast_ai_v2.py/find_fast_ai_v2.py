import streamlit as st
import googlemaps
import openai
import request 
# API Keys
GOOGLE_MAPS_API_KEY = 'AIzaSyC9Le3YOKyUUnapYlk0OKSQLzmxV2hc1Uw'
OPENAI_API_KEY = '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'

# Inicializar APIs
gmaps = googlemaps.Client(key=GOOGLE_MAPS_API_KEY)
openai.api_key = OPENAI_API_KEY

# Configuración inicial
st.set_page_config(page_title="📍 Find Fast AI", layout="centered")

# Estilos
st.markdown("""
    <style>
    .stApp {
        background-color: #f0f2f6;
        max-width: 1000px;
        margin: auto;
        padding: 20px;
    }
    .tarjeta {
        background-color: white;
        padding: 20px;
        border-radius: 12px;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        margin-bottom: 20px;
    }
    .tarjeta img {
        border-radius: 8px;
        margin-bottom: 10px;
    }
    .titulo {
        text-align: center;
        font-size: 36px;
        color: #1a73e8;
        font-weight: bold;
        margin-bottom: 30px;
    }
    </style>
""", unsafe_allow_html=True)

# Título principal
st.markdown('<div class="titulo">📍 Find Fast AI</div>', unsafe_allow_html=True)

# Estados
if 'resultados' not in st.session_state:
    st.session_state.resultados = []
if 'comparar' not in st.session_state:
    st.session_state.comparar = []

# Entrada de búsqueda
consulta = st.text_input("🔍 ¿Qué estás buscando?", max_chars=50)

# Consulta con IA
if consulta:
    with st.spinner("Buscando lugares..."):
        try:
            lugares = gmaps.places(query=consulta)['results']
            st.session_state.resultados = lugares
        except Exception as e:
            st.error(f"Error con Google Maps: {e}")
            st.session_state.resultados = []

# Mostrar resultados
if st.session_state.resultados:
    st.subheader("🔎 Resultados:")
    cols = st.columns(2)
    for i, lugar in enumerate(st.session_state.resultados[:6]):
        detalles = gmaps.place(place_id=lugar['place_id'])['result']

        nombre = detalles.get('name', 'No disponible')
        direccion = detalles.get('formatted_address', 'No disponible')
        calificacion = detalles.get('rating', 'Sin calificación')
        telefono = detalles.get('formatted_phone_number', 'No disponible')
        sitio_web = detalles.get('website', 'No disponible')
        tipos = ', '.join(detalles.get('types', []))
        precio = detalles.get('price_level', 'No especificado')
        horarios = detalles.get('opening_hours', {}).get('weekday_text', [])

        # Imagen
        if 'photos' in detalles:
            photo_ref = detalles['photos'][0]['photo_reference']
            foto_url = f"https://maps.googleapis.com/maps/api/place/photo?maxwidth=400&photoreference={photo_ref}&key={GOOGLE_MAPS_API_KEY}"
        else:
            foto_url = "https://via.placeholder.com/400x300?text=Sin+Foto"

        # Mapa estático
        mapa_url = f"https://maps.googleapis.com/maps/api/staticmap?center={direccion}&zoom=15&size=400x200&markers=color:red%7C{direccion}&key={GOOGLE_MAPS_API_KEY}"

        with cols[i % 2]:
            st.markdown(f"""
                <div class="tarjeta">
                    <h4>{nombre}</h4>
                    <img src="{foto_url}" width="100%">
                    <p><strong>Dirección:</strong> {direccion}</p>
                    <p><strong>Calificación:</strong> {calificacion} ⭐</p>
                    <p><strong>Precio:</strong> {precio}</p>
                    <p><strong>Teléfono:</strong> {telefono}</p>
                    <p><strong>Tipos:</strong> {tipos}</p>
                    <p><strong>Web:</strong> <a href="{sitio_web}" target="_blank">{sitio_web}</a></p>
                    <p><strong>Horario:</strong><br>{'<br>'.join(horarios) if horarios else 'No disponible'}</p>
                    <img src="{mapa_url}" width="100%">
                </div>
            """, unsafe_allow_html=True)

            if st.button(f"Comparar {nombre}", key=f"cmp_{i}"):
                st.session_state.comparar.append({
                    "nombre": nombre,
                    "direccion": direccion,
                    "calificacion": calificacion,
                    "telefono": telefono
                })

# Comparación
if st.session_state.comparar:
    st.subheader("📊 Comparación de Lugares:")
    for lugar in st.session_state.comparar:
        st.markdown(f"""
        - **{lugar['nombre']}**
        - 📍 {lugar['direccion']}
        - ⭐ {lugar['calificacion']}
        - 📞 {lugar['telefono']}
        """)

    

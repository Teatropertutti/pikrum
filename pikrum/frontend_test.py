import streamlit as st
import requests

st.set_page_config(page_title="PIKRUM AI Test Bench", layout="wide")

st.title("🚀 PIKRUM AI - Interfaccia di Test")

# Configurazione URL (Assicurati che il server Django sia attivo sulla 8000)
BASE_URL = "http://127.0.0.1:8000/api/v1"

tabs = st.tabs(["📤 Caricamento", "🔍 Ricerca Semantica"])

with tabs[0]:
    st.header("Gestione Immagini")
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Nuova Reference")
        st.caption("Usa questo per i prodotti campione (100% crop)")
        ref_file = st.file_uploader("Scegli immagine Reference", type=['jpg', 'jpeg', 'png'], key="ref")
        if st.button("Invia come Reference"):
            if ref_file:
                files = {"image_file": ref_file.getvalue()}
                r = requests.post(f"{BASE_URL}/upload/reference/", files={"image_file": (ref_file.name, ref_file.getvalue())})
                st.json(r.json())
            else:
                st.error("Seleziona un file")

    with col2:
        st.subheader("Nuovo Catalogo")
        st.caption("Usa questo per foto d'ambiente (Scomposizione AI)")
        cat_file = st.file_uploader("Scegli immagine Catalogo", type=['jpg', 'jpeg', 'png'], key="cat")
        if st.button("Invia al Catalogo"):
            if cat_file:
                r = requests.post(f"{BASE_URL}/upload/catalog/", files={"image_file": (cat_file.name, cat_file.getvalue())})
                st.json(r.json())
            else:
                st.error("Seleziona un file")

with tabs[1]:
    st.header("Ricerca nel Database")
    search_type = st.radio("Metodo di ricerca", ["Testo", "Immagine"])
    
    results = None
    if search_type == "Testo":
        query_text = st.text_input("Cosa cerchi? (es: 'tazza di caffè')")
        if st.button("Cerca per Testo"):
            r = requests.post(f"{BASE_URL}/search/", data={"query_text": query_text})
            results = r.json()
    else:
        query_img = st.file_uploader("Carica immagine per cercare simili", type=['jpg', 'png'])
        if st.button("Cerca per Immagine"):
            r = requests.post(f"{BASE_URL}/search/", files={"query_image": (query_img.name, query_img.getvalue())})
            results = r.json()

    if results:
        st.subheader("Risultati Trovati")
        for res in results:
            with st.expander(f"Match: {res['label']} (Distanza: {res['distance']:.4f})"):
                col_a, col_b = st.columns([1, 2])
                # Nota: le URL funzionano se Django serve i media correttamente
                col_a.image(f"http://127.0.0.1:8000{res['image_url']}")
                st.write(f"**Box:** {res['box']}")
                st.write(f"**Tags:** {', '.join(res['tags'])}")
import streamlit as st
from fpdf import FPDF

# --- SETUP INIZIALE ---
if 'menu' not in st.session_state:
    st.session_state.menu = {"Lumache in umido": 12.0, "Lumache fritte": 10.0}

# --- FUNZIONE PDF ---
def genera_pdf(nome, ordine):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(200, 10, txt="Ricevuta Prenotazione - Sagra della Lumaca", ln=True, align='C')
    pdf.set_font("Arial", size=12)
    pdf.ln(10)
    pdf.cell(200, 10, txt=f"Cliente: {nome}", ln=True)
    pdf.cell(200, 10, txt="Dettaglio Ordine:", ln=True)
    for piatto, quantita in ordine.items():
        if quantita > 0:
            pdf.cell(200, 10, txt=f"- {piatto}: {quantita}", ln=True)
    return pdf.output(dest='S').encode('latin-1')

# --- INTERFACCIA ---
st.title("🐌 Sagra della Lumaca")

# Area Admin
with st.sidebar:
    st.header("🔑 Area Admin")
    pwd = st.text_input("Password", type="password")
    if pwd == "valledeire":
        nuovo_p = st.text_input("Nuovo Piatto")
        prezzo_p = st.number_input("Prezzo")
        if st.button("Aggiorna Menù"):
            st.session_state.menu[nuovo_p] = prezzo_p
            st.rerun()

# Prenotazione
st.header("Ordina i tuoi piatti")
ordine = {}
for piatto, prezzo in st.session_state.menu.items():
    ordine[piatto] = st.number_input(f"{piatto} (€{prezzo})", 0, 10)

nome = st.text_input("Nome Cliente")
if st.button("Conferma e Scarica Ricevuta"):
    if nome:
        pdf_bytes = genera_pdf(nome, ordine)
        st.download_button("Scarica PDF Prenotazione", pdf_bytes, "ricevuta.pdf")
    else:
        st.error("Inserisci il nome!")

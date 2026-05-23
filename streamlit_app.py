import streamlit as st
from fpdf import FPDF

# Inizializzazione Sessione
if 'step' not in st.session_state: st.session_state.step = 1
if 'menu' not in st.session_state: st.session_state.menu = {"Lumache in umido": 12.0, "Lumache fritte": 10.0}
if 'ordine' not in st.session_state: st.session_state.ordine = {}

st.title("🐌 Sagra della Lumaca")

# --- AREA ADMIN (Sidebar) ---
with st.sidebar:
    st.header("🔑 Area Admin")
    pwd = st.text_input("Password", type="password")
    if pwd == "valledeire":
        new_dish = st.text_input("Nome nuovo piatto")
        new_price = st.number_input("Prezzo", min_value=0.0)
        if st.button("Aggiorna Menù"):
            st.session_state.menu[new_dish] = new_price
            st.rerun()

# --- STEP 1: SELEZIONE PIATTI ---
if st.session_state.step == 1:
    st.header("1. Scegli i piatti")
    totale = 0
    for piatto, prezzo in st.session_state.menu.items():
        qta = st.number_input(f"{piatto} (€{prezzo:.2f})", 0, 10, key=piatto)
        if qta > 0:
            st.session_state.ordine[piatto] = qta
            totale += (qta * prezzo)
            
    if totale > 0:
        st.write(f"### Totale: € {totale:.2f}")
        if st.button("Procedi al Pagamento"):
            st.session_state.step = 2
            st.rerun()

# --- STEP 2: PAGAMENTO ---
elif st.session_state.step == 2:
    st.header("2. Pagamento")
    st.write("IBAN: IT00XXXXX | PayPal: paypal.me/sagra")
    if st.file_uploader("Carica la ricevuta"):
        if st.button("Conferma"):
            st.session_state.step = 3
            st.rerun()
    if st.button("Indietro"): st.session_state.step = 1; st.rerun()

# --- STEP 3: DOWNLOAD ---
elif st.session_state.step == 3:
    st.header("3. Scarica Ricevuta")
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, "Ricevuta Sagra", ln=True, align='C')
    for p, q in st.session_state.ordine.items():
        pdf.cell(200, 10, f"{p} x {q}", ln=True)
    
    # Forza la conversione in bytes e specifica il tipo file
    pdf_bytes = bytes(pdf.output()) 
    
    st.download_button(
        label="📥 Scarica PDF",
        data=pdf_bytes,
        file_name="Prenotazione.pdf",
        mime="application/pdf"
    )
    
    if st.button("Nuova Prenotazione"):
        st.session_state.step = 1
        st.rerun()

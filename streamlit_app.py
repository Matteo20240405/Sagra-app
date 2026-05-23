import streamlit as st
from fpdf import FPDF

# Inizializzazione menù (usa session_state per renderlo persistente)
if 'menu' not in st.session_state:
    st.session_state.menu = {"Lumache in umido": 12.0, "Lumache fritte": 10.0}

st.title("🐌 Sagra della Lumaca")
st.subheader("S.M.S. Fratellanza Segnese")

# --- AREA ADMIN ---
with st.sidebar:
    st.header("🔑 Area Admin")
    pwd = st.text_input("Password", type="password")
    if pwd == "valledeire":
        new_dish = st.text_input("Nome nuovo piatto")
        new_price = st.number_input("Prezzo", min_value=0.0)
        if st.button("Aggiorna Menù"):
            st.session_state.menu[new_dish] = new_price
            st.rerun() # Ricarica per mostrare il nuovo piatto

# --- AREA ORDINE ---
st.header("🍽️ Crea il tuo ordine")
ordine = {}
totale = 0

# Visualizza e calcola
for piatto, prezzo in st.session_state.menu.items():
    col1, col2 = st.columns([3, 1])
    with col1:
        st.write(f"**{piatto}** - € {prezzo:.2f}")
    with col2:
        # Usiamo un key unico per ogni piatto
        qta = st.number_input(f"Qta", 0, 10, key=f"qta_{piatto}")
    
    if qta > 0:
        ordine[piatto] = qta
        totale += (qta * prezzo)

st.divider()
st.metric("Totale provvisorio", f"€ {totale:.2f}")

# --- CHECKOUT ---
nome = st.text_input("Nome e Cognome per la prenotazione")

if st.button("Conferma e Scarica Ricevuta"):
    if nome and totale > 0:
        # Generazione PDF corretta per fpdf2
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", 'B', 16)
        pdf.cell(200, 10, "Ricevuta Sagra della Lumaca", ln=True, align='C')
        pdf.set_font("Arial", size=12)
        pdf.ln(10)
        pdf.cell(200, 10, f"Cliente: {nome}", ln=True)
        for piatto, qta in ordine.items():
            pdf.cell(200, 10, f"- {piatto} x {qta}", ln=True)
        pdf.cell(200, 10, f"TOTALE PAGATO: € {totale:.2f}", ln=True)
        
        # Correzione fondamentale per fpdf2
        pdf_bytes = pdf.output() 
        
        st.download_button("📥 Scarica PDF Ricevuta", pdf_bytes, "Prenotazione.pdf")
    else:
        st.error("Inserisci il nome e seleziona almeno un piatto!")

import streamlit as st
from fpdf import FPDF

# Inizializzazione
if 'step' not in st.session_state: st.session_state.step = 1
if 'menu' not in st.session_state: st.session_state.menu = {"Lumache in umido": 12.0, "Lumache fritte": 10.0}
if 'ordine' not in st.session_state: st.session_state.ordine = {}

st.title("🐌 Sagra della Lumaca")

# --- STEP 1: SELEZIONE PIATTI ---
if st.session_state.step == 1:
    st.header("1. Scegli i tuoi piatti")
    st.session_state.ordine = {}
    totale = 0
    
    for piatto, prezzo in st.session_state.menu.items():
        qta = st.number_input(f"{piatto} (€{prezzo:.2f})", 0, 10, key=piatto)
        if qta > 0:
            st.session_state.ordine[piatto] = qta
            totale += (qta * prezzo)
            
    st.write(f"### Totale: € {totale:.2f}")
    
    if totale > 0:
        if st.button("Procedi al Pagamento"):
            st.session_state.step = 2
            st.rerun()

# --- STEP 2: PAGAMENTO ---
elif st.session_state.step == 2:
    st.header("2. Pagamento")
    st.write("Effettua il bonifico o paga con PayPal:")
    st.code("IBAN: IT00XXXXX | PayPal: paypal.me/sagra")
    
    ricevuta = st.file_uploader("Carica la ricevuta del pagamento")
    
    if ricevuta:
        if st.button("Conferma Pagamento e Genera Ricevuta"):
            st.session_state.step = 3
            st.rerun()
    
    if st.button("Indietro"):
        st.session_state.step = 1
        st.rerun()

# --- STEP 3: DOWNLOAD ---
elif st.session_state.step == 3:
    st.header("3. Ricevuta Prenotazione")
    
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, "Ricevuta Sagra della Lumaca", ln=True, align='C')
    for p, q in st.session_state.ordine.items():
        pdf.cell(200, 10, f"{p} x {q}", ln=True)
        
    pdf_bytes = pdf.output()
    st.download_button("📥 Scarica PDF", pdf_bytes, "Prenotazione.pdf")
    
    if st.button("Torna al menù"):
        st.session_state.step = 1
        st.rerun()

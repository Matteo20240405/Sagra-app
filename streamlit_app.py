import streamlit as st
from fpdf import FPDF

# Inizializzazione sessione
if 'step' not in st.session_state: st.session_state.step = 1 # 1: Ordine, 2: Pagamento, 3: Download

st.title("🐌 Sagra della Lumaca")

# --- STEP 1: ORDINE ---
if st.session_state.step == 1:
    st.header("1. Seleziona i piatti")
    # ... (inserisci qui il tuo codice di selezione piatti precedente) ...
    if st.button("Procedi al Pagamento"):
        st.session_state.step = 2
        st.rerun()

# --- STEP 2: PAGAMENTO ---
elif st.session_state.step == 2:
    st.header("2. Effettua il pagamento")
    st.info("Paga con PayPal o Bonifico Istantaneo")
    st.write("IBAN: IT00XXXXX | PayPal: paypal.me/sagra")
    
    ricevuta_file = st.file_uploader("Carica la ricevuta del pagamento (PDF/JPG)")
    
    if ricevuta_file:
        if st.button("Conferma Pagamento e Genera Ricevuta"):
            st.session_state.step = 3
            st.rerun()
    
    if st.button("Indietro"):
        st.session_state.step = 1
        st.rerun()

# --- STEP 3: DOWNLOAD ---
elif st.session_state.step == 3:
    st.header("3. Prenotazione Conclusa")
    st.success("Pagamento ricevuto! Puoi scaricare la tua ricevuta.")
    
    # Generazione PDF (logica precedente)
    pdf = FPDF()
    # ... (codice generazione PDF) ...
    pdf_bytes = pdf.output()
    
    st.download_button("📥 Scarica PDF Ricevuta", pdf_bytes, "Prenotazione.pdf")
    
    if st.button("Nuova Prenotazione"):
        st.session_state.step = 1
        st.rerun()

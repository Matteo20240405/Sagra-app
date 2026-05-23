import streamlit as st
from fpdf import FPDF

# Inizializzazione Sessione
if 'step' not in st.session_state: st.session_state.step = 1
if 'menu' not in st.session_state: st.session_state.menu = {"Lumache in umido": 12.0, "Lumache fritte": 10.0}
if 'ordine' not in st.session_state: st.session_state.ordine = {}

st.title("🐌 Sagra della Lumaca")
st.subheader("S.M.S. Fratellanza Segnese")

# --- 1. AREA ADMIN (Sidebar) ---
with st.sidebar:
    st.header("🔑 Area Admin")
    pwd = st.text_input("Password", type="password")
    if pwd == "valledeire":
        new_dish = st.text_input("Nome nuovo piatto")
        new_price = st.number_input("Prezzo", min_value=0.0)
        if st.button("Aggiorna Menù"):
            st.session_state.menu[new_dish] = new_price
            st.rerun()

# --- 2. STEP 1: SELEZIONE PIATTI ---
if st.session_state.step == 1:
    st.header("1. Scegli i piatti")
    st.session_state.ordine = {}
    totale_tot = 0
    
    for piatto, prezzo in st.session_state.menu.items():
        qta = st.number_input(f"{piatto} (€{prezzo:.2f})", 0, 10, key=piatto)
        if qta > 0:
            st.session_state.ordine[piatto] = {"qta": qta, "prezzo": prezzo, "parziale": qta * prezzo}
            totale_tot += (qta * prezzo)
            
    if totale_tot > 0:
        st.write(f"### Totale: € {totale_tot:.2f}")
        nome = st.text_input("Nome e Cognome")
        if nome and st.button("Conferma Ordine"):
            st.session_state.nome_cliente = nome
            st.session_state.step = 3 # Passiamo direttamente al download
            st.rerun()

# --- 3. STEP 3: DOWNLOAD RICEVUTA ---
elif st.session_state.step == 3:
    st.header("3. Ricevuta Prenotazione")
    st.success("Ordine registrato correttamente!")
    
    # Creazione PDF
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(200, 10, "Ricevuta Sagra della Lumaca", ln=True, align='C')
    pdf.set_font("Arial", size=12)
    pdf.ln(10)
    pdf.cell(200, 10, f"Cliente: {st.session_state.nome_cliente}", ln=True)
    pdf.ln(5)
    
    totale_finale = 0
    for p, dettagli in st.session_state.ordine.items():
        pdf.cell(200, 10, f"- {p} (x{dettagli['qta']}) -> {dettagli['parziale']:.2f} EUR", ln=True)
        totale_finale += dettagli['parziale']
    
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(200, 10, f"TOTALE GENERALE: {totale_finale:.2f} EUR", ln=True)
    
    # Richiesta allegato pagamento
    pdf.ln(10)
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(200, 10, "IMPORTANTE:", ln=True)
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 10, "Per completare la prenotazione, si prega di effettuare il pagamento (Bonifico/PayPal) e di ALLEGARE la copia della ricevuta di pagamento quando si presenta la presente ricevuta alla cassa della Sagra.")
    
    pdf_bytes = bytes(pdf.output())
    
    st.download_button("📥 Scarica PDF Ricevuta", pdf_bytes, "Prenotazione.pdf", mime="application/pdf")
    
    if st.button("Nuova Prenotazione"):
        st.session_state.step = 1
        st.rerun()

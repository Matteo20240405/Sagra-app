import streamlit as st
from fpdf import FPDF

# Inizializzazione Sessione
if 'step' not in st.session_state: st.session_state.step = 1
if 'menu' not in st.session_state: st.session_state.menu = {"Lumache in umido": 12.0, "Lumache fritte": 10.0}
if 'ordine' not in st.session_state: st.session_state.ordine = {}

st.title("🐌 Sagra della Lumaca")
st.subheader("S.M.S. Fratellanza Segnese")

# --- 1. AREA ADMIN ---
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
        st.write(f"### Totale da pagare: € {totale_tot:.2f}")
        nome = st.text_input("Nome e Cognome")
        if nome and st.button("Vai al Pagamento"):
            st.session_state.nome_cliente = nome
            st.session_state.step = 2
            st.rerun()

# --- 3. STEP 2: PAGAMENTO ---
elif st.session_state.step == 2:
    st.header("2. Dati per il pagamento")
    st.write("Per confermare la prenotazione, effettua il versamento dell'importo totale utilizzando uno dei seguenti metodi:")
    
    st.subheader("💳 Bonifico Bancario")
    st.code("IBAN: IT00 0000 0000 0000 0000 0000 00\nIntestatario: Sagra della Lumaca")
    
    st.subheader("📱 PayPal")
    st.code("paypal.me/sagra-lumaca")
    
    st.info("Dopo aver effettuato il pagamento, clicca sotto per scaricare la tua ricevuta. Ricorda di portare con te la ricevuta del pagamento effettuato quando ritirerai i piatti!")
    
    if st.button("Procedi al Download della Ricevuta"):
        st.session_state.step = 3
        st.rerun()
    if st.button("Indietro"):
        st.session_state.step = 1
        st.rerun()

# --- 4. STEP 3: DOWNLOAD RICEVUTA ---
elif st.session_state.step == 3:
    st.header("3. Ricevuta Prenotazione")
    
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
    pdf.cell(200, 10, f"TOTALE PAGATO: {totale_finale:.2f} EUR", ln=True)
    
    pdf.ln(10)
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(200, 10, "ISTRUZIONI:", ln=True)
    pdf.set_font("Arial", size=11)
    pdf.multi_cell(0, 7, "Si prega di conservare questa ricevuta e di allegare la copia del bonifico/transazione PayPal effettuata. Presentare entrambi ai camerieri al momento del ritiro.")
    
    pdf_bytes = bytes(pdf.output())
    
    st.download_button("📥 Scarica PDF Ricevuta", pdf_bytes, "Prenotazione.pdf", mime="application/pdf")
    
    if st.button("Nuova Prenotazione"):
        st.session_state.step = 1
        st.rerun()

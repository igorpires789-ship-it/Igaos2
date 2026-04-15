import streamlit as st
import streamlit.components.v1 as components
import re
from collections import Counter

# --- 1. CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="KING MAN DA ROLETA", layout="wide", initial_sidebar_state="expanded")

# --- 2. ESTILIZAÇÃO CSS COMPLETA (NEON, RACE, BOTÕES) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Bungee&display=swap');

    /* Título Neon */
    .neon-title {
        font-family: 'Bungee', cursive;
        font-size: 3.5rem;
        color: #fff;
        text-align: center;
        text-transform: uppercase;
        margin-top: -20px;
        margin-bottom: 30px;
        text-shadow: 0 0 10px #fff, 0 0 20px #FFD700, 0 0 40px #FFD700;
        animation: pulse 1.5s infinite alternate;
    }
    @keyframes pulse {
        from { text-shadow: 0 0 10px #fff, 0 0 20px #FFD700, 0 0 30px #FFD700; transform: scale(1); }
        to { text-shadow: 0 0 15px #fff, 0 0 30px #FFD700, 0 0 50px #FFD700; transform: scale(1.02); }
    }

    /* Teclado e Botões */
    div.stButton > button { width: 100%; height: 45px; font-weight: bold; color: white; border-radius: 5px; border: 1px solid #444; }
    .btn-red button { background-color: #ff4b4b !important; }
    .btn-black button { background-color: #1a1a1a !important; }
    .btn-green button { background-color: #28a745 !important; }
    .btn-action button { background-color: #3e4444 !important; }

    /* Race Racetrack Oval */
    .race-container {
        display: flex; flex-wrap: wrap; justify-content: center; align-items: center;
        padding: 25px; background-color: #101216; border-radius: 150px;
        border: 4px solid #333; margin: 20px 0; box-shadow: inset 0 0 15px rgba(0,0,0,0.5);
    }
    .race-slot {
        width: 38px; height: 55px; display: flex; align-items: center; justify-content: center;
        margin: 3px; border-radius: 8px; font-weight: bold; font-size: 1rem; color: white; border: 1px solid #222;
    }
    
    /* Gatilho Dourado Único */
    .gatilho-unico {
        background-color: #FFD700 !important; color: #000 !important;
        border: 2px solid #FFF; box-shadow: 0 0 15px #FFD700; transform: scale(1.2); z-index: 10;
    }
    .ultimo-sorteado { border: 3px solid #00ff00 !important; box-shadow: 0 0 10px #00ff00; }

    /* Histórico */
    .pills { display: inline-block; padding: 5px 12px; margin: 3px; border-radius: 20px; color: white; font-weight: bold; border: 1px solid #555; }
    </style>
    
    <h1 class="neon-title">KING MAN DA ROLETA</h1>
    """, unsafe_allow_html=True)

# --- 3. LÓGICA DE DADOS E VARIÁVEIS DE ESTADO ---
if 'historico_completo' not in st.session_state:
    st.session_state.historico_completo = []
if 'gatilho_atual' not in st.session_state:
    st.session_state.gatilho_atual = None

vermelhos = [1, 3, 5, 7, 9, 12, 14, 16, 18, 19, 21, 23, 25, 27, 30, 32, 34, 36]
sequencia_roda = [0, 32, 15, 19, 4, 21, 2, 25, 17, 34, 6, 27, 13, 36, 11, 30, 8, 23, 10, 5, 24, 16, 33, 1, 20, 14, 31, 9, 22, 18, 29, 7, 28, 12, 35, 3, 26]

def obter_cor_hex(num):
    if num == 0: return "#28a745"
    return "#ff4b4b" if num in vermelhos else "#1a1a1a"

def obter_cor_letra(num):
    if num == 0: return "Z"
    return "V" if num in vermelhos else "P"

# --- 4. MOTORES DE ANÁLISE DE PADRÕES ---
def analisar_padroes():
    hist = st.session_state.historico_completo
    if len(hist) < 5: return None
    
    cores_str = "".join([obter_cor_letra(n) for n in hist])
    
    # Exemplo de lógica para Escada 3-2-1
    # Se detectar o final de uma escada, sugere o número 17 (Exemplo de gatilho)
    if re.search(r"([PV])3[PV]1\1 2[PV]1", cores_str.replace('V', 'V ').replace('P', 'P ')):
        return 17 
    
    # Exemplo de lógica para Repetição de Histórico
    if len(cores_str) >= 4:
        seq_atual = cores_str[-4:]
        passado = cores_str[:-1]
        pos = passado.rfind(seq_atual)
        if pos != -1:
            return hist[pos + 4] # Sugere o que veio depois no passado
            
    return None

# --- 5. FUNÇÃO DE CELEBRAÇÃO (JS) ---
def disparar_efeito_ganho():
    confetti_js = """
    <script src="https://cdn.jsdelivr.net/npm/canvas-confetti@1.6.0/dist/confetti.browser.min.js"></script>
    <script>
        var count = 200;
        var defaults = { origin: { y: 0.7 } };
        function fire(particleRatio, opts) {
            confetti(Object.assign({}, defaults, opts, { particleCount: Math.floor(count * particleRatio) }));
        }
        fire(0.25, { spread: 26, startVelocity: 55 });
        fire(0.2, { spread: 60 });
        fire(0.35, { spread: 100, decay: 0.91, scalar: 0.8 });
        fire(0.1, { spread: 120, startVelocity: 25, decay: 0.92, scalar: 1.2 });
        fire(0.1, { spread: 120, startVelocity: 45 });
    </script>
    """
    components.html(confetti_js, height=0)

# --- 6. SIDEBAR (TECLADO DA ROLETA) ---
with st.sidebar:
    st.header("🎮 Entrada de Dados")
    
    # Botão Zero
    st.markdown('<div class="btn-green">', unsafe_allow_html=True)
    if st.button("0", key="k0"): st.session_state.historico_completo.append(0); st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

    # Teclado 1-36
    for row in range(12):
        cols = st.columns(3)
        for i, col_idx in enumerate([1, 2, 3]):
            num = (row * 3) + col_idx
            cor_c = "btn-red" if num in vermelhos else "btn-black"
            with cols[i]:
                st.markdown(f'<div class="{cor_c}">', unsafe_allow_html=True)
                if st.button(str(num), key=f"k{num}"):
                    st.session_state.historico_completo.append(num)
                    st.rerun()
                st.markdown('</div>', unsafe_allow_html=True)

    st.divider()
    c1, c2 = st.columns(2)
    with c1:
        st.markdown('<div class="btn-action">', unsafe_allow_html=True)
        if st.button("⬅️ APAGAR", key="del"):
            if st.session_state.historico_completo: st.session_state.historico_completo.pop(); st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    with c2:
        if st.button("🗑️ LIMPAR", key="clr"): st.session_state.historico_completo = []; st.rerun()

# --- 7. PROCESSAMENTO E EXIBIÇÃO ---
if st.session_state.historico_completo:
    # Verifica Ganho
    ultimo = st.session_state.historico_completo[-1]
    if st.session_state.gatilho_atual is not None and ultimo == st.session_state.gatilho_atual:
        st.success("🏆 WIN! O KING MAN ACERTOU!")
        disparar_efeito_ganho()
        st.session_state.gatilho_atual = None # Reseta gatilho após o win

    # Atualiza Gatilho
    st.session_state.gatilho_atual = analisar_padroes()

    # Exibição da Race
    st.subheader("🏎️ Racetrack (Sequência da Roda)")
    html_race = '<div class="race-container">'
    for n in sequencia_roda:
        base = "race-zero" if n == 0 else "race-red" if n in vermelhos else "race-black"
        extra = " gatilho-unico" if n == st.session_state.gatilho_atual else ""
        extra += " ultimo-sorteado" if n == ultimo and n != st.session_state.gatilho_atual else ""
        html_race += f'<div class="race-slot {base}{extra}">{n}</div>'
    html_race += '</div>'
    st.markdown(html_race, unsafe_allow_html=True)

    # Histórico Visual
    st.subheader("📜 Histórico Recente")
    h_vis = st.session_state.historico_completo[::-1]
    html_h = "".join([f'<div class="pills" style="background-color: {obter_cor_hex(n)};">{n}</div>' for n in h_vis[:20]])
    st.markdown(html_h, unsafe_allow_html=True)
else:
    st.info("Aguardando os primeiros números para iniciar a análise do King Man.")

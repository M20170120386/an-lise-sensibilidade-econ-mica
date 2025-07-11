import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(page_title="Análise de VPL com Sensibilidade")

st.title("Calculadora de VPL com Análise de Sensibilidade")

# Entradas do usuário
st.header("Dados do Projeto")

investimento_inicial = st.number_input("Investimento inicial (valor negativo)", value=-100000.0, format="%.2f")
fluxo_anual = st.number_input("Fluxo de caixa anual", value=30000.0, format="%.2f")
anos = st.number_input("Número de anos", min_value=1, value=5)
tma_base = st.slider("TMA base (%)", min_value=0.0, max_value=30.0, value=10.0, step=0.5)

# Cálculo do VPL base
tma_real = tma_base / 100
vpl_base = sum([fluxo_anual / (1 + tma_real) ** t for t in range(1, anos + 1)]) + investimento_inicial

st.success(f"VPL base: R$ {vpl_base:,.2f}")

st.divider()

# Análise de Sensibilidade
st.header("Análise de Sensibilidade: VPL x TMA")

tma_min = st.slider("TMA mínima (%)", 0.0, 30.0, 6.0, step=0.5)
tma_max = st.slider("TMA máxima (%)", 0.0, 30.0, 14.0, step=0.5)
passo = st.select_slider("Passo (%)", options=[0.5, 1.0, 2.0, 2.5, 5.0], value=1.0)

tma_range = np.arange(tma_min, tma_max + passo, passo)
vpls = [sum([fluxo_anual / (1 + t/100) ** t_ for t_ in range(1, anos + 1)]) + investimento_inicial for t in tma_range]

# Gráfico
fig, ax = plt.subplots()
ax.plot(tma_range, vpls, marker='o', color='blue')
ax.axhline(0, color='gray', linestyle='--')
ax.set_xlabel("TMA (%)")
ax.set_ylabel("VPL (R$)")
ax.set_title("Sensibilidade do VPL em relação à TMA")
ax.grid(True)
st.pyplot(fig)

# Interpretação
st.header("Interpretação")

if vpl_base > 0:
    st.markdown("O investimento é **viável** com a TMA base escolhida.")
else:
    st.markdown("O investimento é **inviável** com a TMA base escolhida.")

tma_critica = None
for i in range(len(tma_range) - 1):
    if vpls[i] >= 0 and vpls[i + 1] < 0:
        tma_critica = tma_range[i + 1]
        break

if tma_critica:
    st.markdown(f"A **TMA crítica** está em torno de **{tma_critica:.2f}%** — acima disso, o VPL se torna negativo.")


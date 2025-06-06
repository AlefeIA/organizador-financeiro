import streamlit as st
import matplotlib.pyplot as plt

st.set_page_config(page_title="Organizador Financeiro", layout="centered")

# 🌗 Escolha de tema
tema = st.selectbox("🌗 Escolha o tema visual:", ["Claro", "Escuro"])
if tema == "Escuro":
    st.markdown("""
        <style>
            body { background-color: #0e1117; color: white; }
            .stApp { background-color: #0e1117; color: white; }
        </style>
    """, unsafe_allow_html=True)

# Título
st.title("💰 Organizador Financeiro Inteligente")
st.markdown("Organize sua vida financeira por categoria e entenda para onde vai seu dinheiro.")

# RECEITA
st.header("💵 Receita")
salario = st.number_input("Salário principal (R$):", min_value=0.0, format="%.2f")
renda_extra = st.number_input("Outra fonte de renda (R$):", min_value=0.0, format="%.2f")
renda_total = salario + renda_extra

# GASTOS
st.header("📂 Gastos por categoria:")

# Moradia
st.subheader("🏠 Moradia")
aluguel = st.number_input("— Aluguel:", min_value=0.0, format="%.2f")
luz = st.number_input("— Luz:", min_value=0.0, format="%.2f")
agua = st.number_input("— Água:", min_value=0.0, format="%.2f")
moradia = aluguel + luz + agua
st.markdown(f"**Total Moradia:** R$ {moradia:.2f}")

# Transporte
st.subheader("🚗 Transporte")
financiamento = st.number_input("— Financiamento de veículo:", min_value=0.0, format="%.2f")
locomocao = st.number_input("— Custo de locomoção:", min_value=0.0, format="%.2f")
manutencao = st.number_input("— Manutenção do veículo:", min_value=0.0, format="%.2f")
transporte_terc = st.number_input("— Transporte terceirizado:", min_value=0.0, format="%.2f")
transporte = financiamento + locomocao + manutencao + transporte_terc
st.markdown(f"**Total Transporte:** R$ {transporte:.2f}")

# Alimentação
st.subheader("🍽️ Alimentação")
mercado = st.number_input("— Mercado:", min_value=0.0, format="%.2f")
delivery = st.number_input("— Delivery:", min_value=0.0, format="%.2f")
restaurantes = st.number_input("— Restaurantes e lanchonetes:", min_value=0.0, format="%.2f")
alimentacao = mercado + delivery + restaurantes
st.markdown(f"**Total Alimentação:** R$ {alimentacao:.2f}")

# Saúde
st.subheader("🩺 Saúde")
saude = st.number_input("Total com saúde (R$):", min_value=0.0, format="%.2f")

# Lazer
st.subheader("🎉 Lazer")
opcoes_lazer = st.multiselect(
    "Quais são seus 3 principais tipos de lazer?",
    ["Cinema", "Viagens", "Streaming", "Jogos", "Bares/Restaurantes", "Academia", "Shows", "Outros"],
    max_selections=3
)

valores_lazer = {}
total_lazer = 0
for opcao in opcoes_lazer:
    valor = st.number_input(f"— {opcao}:", min_value=0.0, format="%.2f")
    valores_lazer[opcao] = valor
    total_lazer += valor
lazer = total_lazer
st.markdown(f"**Total Lazer:** R$ {lazer:.2f}")

# Outros
st.subheader("📦 Outros")
outros = st.number_input("Outros gastos (R$):", min_value=0.0, format="%.2f")

# Resultado Final
total_gastos = moradia + transporte + alimentacao + saude + lazer + outros
economia = renda_total - total_gastos

st.subheader("📊 Resultado Mensal")
st.write(f"**Total de gastos:** R$ {total_gastos:.2f}")
st.write(f"**Sobra do mês:** R$ {economia:.2f}")

if economia < 0:
    st.error("⚠️ Você está gastando mais do que ganha!")
elif economia == 0:
    st.warning("⚠️ Você está no limite do orçamento.")
else:
    st.success("✅ Você está economizando! Continue assim.")

# Gráfico
labels = ['Moradia', 'Transporte', 'Alimentação', 'Saúde', 'Lazer', 'Outros']
valores = [moradia, transporte, alimentacao, saude, lazer, outros]
labels_filtradas = [label for label, valor in zip(labels, valores) if valor > 0]
valores_filtrados = [valor for valor in valores if valor > 0]

if valores_filtrados:
    st.subheader("📉 Distribuição dos gastos:")
    fig, ax = plt.subplots()
    ax.pie(valores_filtrados, labels=labels_filtradas, autopct='%1.1f%%', startangle=90)
    ax.axis('equal')
    st.pyplot(fig)



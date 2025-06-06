import streamlit as st

# Configuração da página
st.set_page_config(page_title="Organizador Financeiro", layout="centered")

# Inicializa o controle de páginas
if "pagina" not in st.session_state:
    st.session_state.pagina = 1

# Função para mudar de página
def avancar():
    st.session_state.pagina += 1

# PÁGINA 1 – Boas-vindas
if st.session_state.pagina == 1:
    st.title("👋 Seja bem-vindo ao Organizador Financeiro guiado por IA")
    st.markdown("### Preparado para ver seu dinheiro render?")
    st.image("https://cdn-icons-png.flaticon.com/512/609/609803.png", width=100)
    if st.button("Sim, vamos começar!"):
        avancar()

# PÁGINA 2 – Perfil
elif st.session_state.pagina == 2:
    st.title("📋 Etapa 1: Seu Perfil")

    sexo = st.radio("Sexo:", ["Masculino", "Feminino", "Outro"])
    estado_civil = st.selectbox("Estado Civil:", ["Solteiro(a)", "Casado(a)", "Divorciado(a)", "Viúvo(a)"])
    tem_filhos = st.radio("Você tem filhos?", ["Não", "Sim"])

    num_filhos = 0
    if tem_filhos == "Sim":
        num_filhos = st.number_input("Quantos filhos?", min_value=1, step=1)

    if st.button("Avançar para o organizador"):
        # Armazenar no session_state se quiser usar depois
        st.session_state.perfil = {
            "sexo": sexo,
            "estado_civil": estado_civil,
            "tem_filhos": tem_filhos,
            "num_filhos": num_filhos
        }
        avancar()

# PÁGINA 3 – Organizador financeiro (versão básica)
elif st.session_state.pagina == 3:
    st.title("💰 Etapa 2: Organize suas Finanças")

    salario = st.number_input("Salário principal (R$):", min_value=0.0, format="%.2f")
    renda_extra = st.number_input("Outra fonte de renda (R$):", min_value=0.0, format="%.2f")
    renda_total = salario + renda_extra

    st.subheader("📂 Gastos Mensais")
    moradia = st.number_input("Moradia (aluguel, luz, água):", min_value=0.0, format="%.2f")
    transporte = st.number_input("Transporte (combustível, ônibus, etc):", min_value=0.0, format="%.2f")
    alimentacao = st.number_input("Alimentação:", min_value=0.0, format="%.2f")
    saude = st.number_input("Saúde:", min_value=0.0, format="%.2f")
    lazer = st.number_input("Lazer:", min_value=0.0, format="%.2f")
    outros = st.number_input("Outros:", min_value=0.0, format="%.2f")

    total_gastos = moradia + transporte + alimentacao + saude + lazer + outros
    sobra = renda_total - total_gastos

    st.subheader("📊 Resultado")
    st.write(f"**Total de Renda:** R$ {renda_total:.2f}")
    st.write(f"**Total de Gastos:** R$ {total_gastos:.2f}")
    st.write(f"**Sobra do mês:** R$ {sobra:.2f}")

    if sobra < 0:
        st.error("⚠️ Você está gastando mais do que ganha.")
    elif sobra == 0:
        st.warning("⚠️ Sua renda está totalmente comprometida.")
    else:
        st.success("✅ Parabéns! Você está economizando.")

    st.markdown("🔁 Você pode voltar e revisar seus dados a qualquer momento recarregando a página.")

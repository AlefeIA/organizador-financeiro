
import streamlit as st
import json
import os

# === Função para salvar múltiplos campos ===
def salvar_dados(pares):
    if isinstance(pares, list):
        for i in range(0, len(pares), 2):
            dados[pares[i]] = pares[i + 1]
    usuarios[st.session_state.email]["dados"] = dados
    salvar_usuarios(usuarios)

st.set_page_config(page_title="Organizador IA", layout="wide")

if "tema_escuro" not in st.session_state:
    st.session_state.tema_escuro = False

def toggle_tema():
    st.session_state.tema_escuro = not st.session_state.tema_escuro

tema_classe = "background-color:#1c1c1c;color:white;border-radius:10px;padding:20px;" if st.session_state.tema_escuro else "background-color:#f9f9f9;color:#222;border-radius:10px;padding:20px;"

def carregar_usuarios():
    if os.path.exists("usuarios.json"):
        with open("usuarios.json", "r") as file:
            return json.load(file)
    return {}

def salvar_usuarios(usuarios):
    with open("usuarios.json", "w") as file:
        json.dump(usuarios, file, indent=4)

usuarios = carregar_usuarios()

for key in ["logado", "email", "pagina"]:
    if key not in st.session_state:
        st.session_state[key] = False if key == "logado" else "" if key == "email" else 1

if not st.session_state.logado:
    st.title("🔐 Login ou Cadastro")
    aba = st.radio("Escolha:", ["Login", "Cadastrar"])
    email = st.text_input("E-mail")
    senha = st.text_input("Senha", type="password")
    if aba == "Cadastrar":
        if st.button("Criar conta"):
            if email in usuarios:
                st.error("E-mail já cadastrado.")
            else:
                usuarios[email] = {"senha": senha, "dados": {}}
                salvar_usuarios(usuarios)
                st.success("Conta criada. Faça login.")
    else:
        if st.button("Entrar"):
            if email in usuarios and usuarios[email]["senha"] == senha:
                st.session_state.logado = True
                st.session_state.email = email
                st.session_state.pagina = 1
                st.rerun()
            else:
                st.error("E-mail ou senha incorretos.")

if st.session_state.logado:
    email = st.session_state.email
    dados = usuarios[email].get("dados", {})
    pagina = st.session_state.pagina

    if "boas_vindas_vista" not in st.session_state:
        st.session_state.boas_vindas_vista = False

    st.sidebar.title("⚙️ Menu")
    st.sidebar.write(f"Usuário: {email}")
    st.sidebar.button("🔄 Alternar tema", on_click=toggle_tema)
    st.sidebar.markdown("---")
    menu = st.sidebar.radio("Navegação", ["Perfil", "Gastos", "Recomendações"])

    if not st.session_state.boas_vindas_vista:
        st.markdown(f"<div style='{tema_classe}'><h2>👋 Seja bem-vindo ao Organizador Financeiro IA</h2><p>Preparado para ver seu dinheiro render?</p></div>", unsafe_allow_html=True)
        if st.button("Começar"):
            st.session_state.boas_vindas_vista = True
            st.rerun()

    if menu == "Perfil":
        st.markdown(f"<div style='{tema_classe}'><h3>📋 Perfil do Usuário</h3>", unsafe_allow_html=True)
        sexo = st.radio("Sexo:", ["Masculino", "Feminino", "Outro"], index=0)
        estado_civil = st.selectbox("Estado Civil:", ["Solteiro(a)", "Casado(a)", "Divorciado(a)", "Viúvo(a)"])
        tem_filhos = st.radio("Você tem filhos?", ["Não", "Sim"])
        num_filhos = 0
        if tem_filhos == "Sim":
            num_filhos = st.number_input("Quantos filhos?", min_value=1, step=1)
        if st.button("💾 Salvar Perfil"):
            dados.update({
                "sexo": sexo,
                "estado_civil": estado_civil,
                "tem_filhos": tem_filhos,
                "num_filhos": num_filhos
            })
            usuarios[email]["dados"] = dados
            salvar_usuarios(usuarios)
            st.success("Perfil salvo!")
        st.markdown("</div>", unsafe_allow_html=True)

    if menu == "Gastos":
        st.markdown(f"<div style='{tema_classe}'><h3>💸 Gastos e Subcategorias</h3>", unsafe_allow_html=True)
        salario = st.number_input("Salário mensal (R$):", value=dados.get("salario", 0.0), format="%.2f")

        with st.expander("🏠 Moradia"):
            aluguel = st.number_input("Aluguel:", value=dados.get("aluguel", 0.0), format="%.2f")
            luz = st.number_input("Luz:", value=dados.get("luz", 0.0), format="%.2f")
            agua = st.number_input("Água:", value=dados.get("agua", 0.0), format="%.2f")
            st.button("💾 Salvar Moradia", key="moradia_btn", on_click=lambda: salvar_dados(["aluguel", aluguel, "luz", luz, "agua", agua]))

        with st.expander("🚗 Transporte"):
            financiamento = st.number_input("Financiamento de veículo:", value=dados.get("financiamento", 0.0), format="%.2f")
            locomocao = st.number_input("Locomoção:", value=dados.get("locomocao", 0.0), format="%.2f")
            manutencao = st.number_input("Manutenção:", value=dados.get("manutencao", 0.0), format="%.2f")
            transporte_publico = st.number_input("Transporte público/particular:", value=dados.get("transporte_publico", 0.0), format="%.2f")
            st.button("💾 Salvar Transporte", key="transporte_btn", on_click=lambda: salvar_dados(["financiamento", financiamento, "locomocao", locomocao, "manutencao", manutencao, "transporte_publico", transporte_publico]))

        with st.expander("🍽️ Alimentação"):
            mercado = st.number_input("Mercado:", value=dados.get("mercado", 0.0), format="%.2f")
            delivery = st.number_input("Delivery:", value=dados.get("delivery", 0.0), format="%.2f")
            restaurantes = st.number_input("Restaurantes/lanchonetes:", value=dados.get("restaurantes", 0.0), format="%.2f")
            st.button("💾 Salvar Alimentação", key="alimentacao_btn", on_click=lambda: salvar_dados(["mercado", mercado, "delivery", delivery, "restaurantes", restaurantes]))

        with st.expander("🎉 Lazer"):
            opcoes = st.multiselect("Escolha até 3 programas de lazer:", ["Cinema", "Bares", "Jogos", "Viagens", "Streaming"])
            pares_lazer = []
            for i, opcao in enumerate(opcoes[:3]):
                valor = st.number_input(f"{opcao}:", value=dados.get(opcao, 0.0), format="%.2f")
                dados[opcao] = valor
                pares_lazer.extend([opcao, valor])
            st.button("💾 Salvar Lazer", key="lazer_btn", on_click=lambda: salvar_dados(pares_lazer))

        saude = st.number_input("🩺 Saúde:", value=dados.get("saude", 0.0), format="%.2f")
        outros = st.number_input("📦 Outros gastos:", value=dados.get("outros", 0.0), format="%.2f")
        if st.button("💾 Salvar Tudo"):
            dados.update({
                "salario": salario, "saude": saude, "outros": outros
            })
            usuarios[email]["dados"] = dados
            salvar_usuarios(usuarios)
            st.success("Todos os dados salvos!")

        st.markdown("</div>", unsafe_allow_html=True)

    if menu == "Recomendações":
        st.markdown(f"<div style='{tema_classe}'><h3>📊 Análise e Recomendações</h3>", unsafe_allow_html=True)
        salario = dados.get("salario", 0.0)
        moradia = dados.get("aluguel", 0.0) + dados.get("luz", 0.0) + dados.get("agua", 0.0)
        transporte = sum(dados.get(chave, 0.0) for chave in ["financiamento", "locomocao", "manutencao", "transporte_publico"])
        alimentacao = sum(dados.get(chave, 0.0) for chave in ["mercado", "delivery", "restaurantes"])
        lazer = sum(dados.get(chave, 0.0) for chave in ["Cinema", "Bares", "Jogos", "Viagens", "Streaming"])
        saude = dados.get("saude", 0.0)
        outros = dados.get("outros", 0.0)

        total = moradia + transporte + alimentacao + lazer + saude + outros
        sobra = salario - total

        st.metric("Total de Gastos", f"R$ {total:.2f}")
        st.metric("Sobra do mês", f"R$ {sobra:.2f}")

        st.subheader("💡 Recomendações")
        tetos = {
            "Moradia": salario * 0.30,
            "Transporte": salario * 0.15,
            "Alimentação": salario * 0.20,
            "Saúde": salario * 0.10,
            "Lazer": salario * 0.10
        }
        categorias = {
            "Moradia": moradia,
            "Transporte": transporte,
            "Alimentação": alimentacao,
            "Saúde": saude,
            "Lazer": lazer
        }
        for cat, valor in categorias.items():
            if valor > tetos[cat]:
                st.warning(f"⚠️ {cat}: R$ {valor:.2f} acima do ideal ({tetos[cat]:.2f})")
            else:
                st.success(f"✅ {cat} dentro do limite ideal.")
        st.markdown("</div>", unsafe_allow_html=True)

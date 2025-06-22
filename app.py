import streamlit as st
from datetime import datetime, timedelta
from services import *

st.set_page_config(page_title="ParkCondo", layout="wide")
st.title("🚗 ParkCondo – Gestão de Estacionamento e Acesso")

# ---- Gerenciamento de Sessão ----
if "apto" not in st.session_state:
    st.session_state["apto"] = None

# ---- Login ----
if not st.session_state["apto"]:
    st.subheader("🔑 Login")
    numero_apto = st.text_input("Digite seu número de apartamento")
    if st.button("Entrar"):
        user = login(numero_apto)
        if user:
            st.session_state["apto"] = numero_apto
            st.success(f"Bem-vindo, apartamento {numero_apto}")
            st.experimental_rerun()
        else:
            st.error("Número de apartamento não encontrado")
    st.stop()

# ---- Menu ----
aba = st.sidebar.selectbox(
    "Menu",
    ["📋 Solicitar Vaga", "🚗 Minhas Solicitações", "🏢 Painel Admin", "🏗️ Condomínios", "🚪 Sair"]
)

# ---- Logout ----
if aba == "🚪 Sair":
    st.session_state["apto"] = None
    st.experimental_rerun()

# ---- Solicitar Vaga ----
if aba == "📋 Solicitar Vaga":
    st.subheader("📋 Solicitar Vaga")
    entrada = st.time_input("Horário de entrada", value=datetime.now().time())
    saida = st.time_input("Horário de saída", value=(datetime.now() + timedelta(hours=2)).time())

    if st.button("Confirmar Pedido"):
        entrada_dt = datetime.combine(datetime.today(), entrada)
        saida_dt = datetime.combine(datetime.today(), saida)
        criar_pedido(
            condominio_id="123e4567-e89b-12d3-a456-426614174000",
            solicitante=st.session_state["apto"],
            visitante="",
            placa="",
            modelo="",
            entrada=entrada_dt,
            saida=saida_dt,
            price=0.0
        )
        st.success("Pedido realizado com sucesso!")

# ---- Minhas Solicitações ----
if aba == "🚗 Minhas Solicitações":
    st.subheader("🚗 Minhas Solicitações")
    pedidos = listar_pedidos()
    meus_pedidos = [p for p in pedidos if p["solicitante"] == st.session_state["apto"]]
    st.table(meus_pedidos)

# ---- Painel Admin ----
if aba == "🏢 Painel Admin":
    st.subheader("🏢 Pedidos de Acesso")
    pedidos = listar_pedidos()
    st.dataframe(pedidos)

    st.subheader("🚗 Vagas de Estacionamento")
    vagas = listar_vagas()
    st.dataframe(vagas)

# ---- Cadastro de Condomínio ----
if aba == "🏗️ Condomínios":
    st.subheader("🏗️ Cadastro de Condomínio")
    with st.form("form_cond"):
        nome = st.text_input("Nome")
        cnpj = st.text_input("CNPJ")
        endereco = st.text_input("Endereço")
        sindico = st.text_input("Síndico")
        telefone = st.text_input("Telefone")
        email = st.text_input("Email")
        descricao = st.text_area("Descrição")

        submit = st.form_submit_button("Cadastrar")

    if submit:
        criar_condominio(nome, cnpj, endereco, sindico, telefone, email, descricao)
        st.success("Condomínio cadastrado com sucesso!")

    st.subheader("🏢 Condomínios Cadastrados")
    condominios = listar_condominios()
    st.dataframe(condominios)
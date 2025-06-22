# services.py

from supabase import create_client, Client
from dotenv import load_dotenv
import os
from datetime import datetime

# Carrega variáveis de ambiente
load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_ANON_KEY")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# ---- Login ----
def login(numero_apto: str):
    response = supabase.table("vagas").select("*").eq("apto_proprietario", numero_apto).execute()
    return response.data[0] if response.data else None

# ---- Condomínio ----
def criar_condominio(nome, cnpj, endereco, sindico, telefone, email, descricao):
    data = {
        "nome": nome,
        "cnpj": cnpj,
        "endereco": endereco,
        "sindico": sindico,
        "telefone": telefone,
        "email": email,
        "descricao": descricao
    }
    return supabase.table("parkcondo_table").insert(data).execute().data

def listar_condominios():
    return supabase.table("parkcondo_table").select("*").execute().data

# ----------------- PEDIDOS -----------------

def criar_pedido(condominio_id: str, solicitante: str, visitante: str, placa: str, modelo: str,
                 entrada: datetime, saida: datetime, price: float):
    data = {
        "condominio_id": condominio_id,
        "solicitante": solicitante,
        "visitante": visitante,
        "placa": placa,
        "modelo": modelo,
        "entrada": entrada.isoformat(),
        "saida": saida.isoformat(),
        "status": "open",
        "price": price
    }
    response = supabase.table("pedidos").insert(data).execute()
    return response.data


def listar_pedidos(condominio_id: str = None, status: str = None, dia: str = None):
    query = supabase.table("pedidos").select("*")
    if condominio_id:
        query = query.eq("condominio_id", condominio_id)
    if status:
        query = query.eq("status", status)
    if dia:
        query = query.eq("dia", dia)  # formato: 'YYYY-MM-DD'

    response = query.order("entrada", desc=True).execute()
    return response.data


def atualizar_pedido(pedido_id: str, campos_para_atualizar: dict):
    response = supabase.table("pedidos").update(campos_para_atualizar).eq("id", pedido_id).execute()
    return response.data


def deletar_pedido(pedido_id: str):
    response = supabase.table("pedidos").delete().eq("id", pedido_id).execute()
    return response.data


# ----------------- VAGAS -----------------

def criar_vaga(condominio_id: str, vaga: str, proprietario_1: str, bloco: str,
               apto_proprietario: str, telefone_1: str,
               proprietario_2: str = None, telefone_2: str = None):
    data = {
        "condominio_id": condominio_id,
        "vaga": vaga,
        "proprietario_1": proprietario_1,
        "proprietario_2": proprietario_2,
        "bloco": bloco,
        "apto_proprietario": apto_proprietario,
        "telefone_1": telefone_1,
        "telefone_2": telefone_2
    }
    response = supabase.table("vagas").insert(data).execute()
    return response.data


def listar_vagas(condominio_id: str = None):
    query = supabase.table("vagas").select("*")
    if condominio_id:
        query = query.eq("condominio_id", condominio_id)

    response = query.order("vaga", desc=False).execute()
    return response.data


def atualizar_vaga(vaga_id: str, campos_para_atualizar: dict):
    response = supabase.table("vagas").update(campos_para_atualizar).eq("id", vaga_id).execute()
    return response.data


def deletar_vaga(vaga_id: str):
    response = supabase.table("vagas").delete().eq("id", vaga_id).execute()
    return response.data

import os
from dotenv import load_dotenv
from supabase import create_client, Client

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")  # sua anon key (ou como você nomeou)

# ✅ mantém o client global (não quebra imports antigos)
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# ✅ cria um client autenticado por request (para RLS)
def supabase_for_user(access_token: str) -> Client:
    client: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
    client.postgrest.auth(access_token)  # injeta JWT no PostgREST
    return client
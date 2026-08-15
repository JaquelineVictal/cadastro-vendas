"""Configuracao do Supabase lida de variaveis de ambiente (.env local).

Usado tanto pela interface Gradio quanto pela Tkinter, para que nenhuma
das duas precise saber como as credenciais chegam ate aqui.
"""

import os

from dotenv import load_dotenv

load_dotenv()


def supabase_config() -> dict:
    return {
        "url": os.environ.get("SUPABASE_URL", "").strip(),
        "key": os.environ.get("SUPABASE_KEY", "").strip(),
        "table": os.environ.get("SALES_TABLE", "vendas"),
    }

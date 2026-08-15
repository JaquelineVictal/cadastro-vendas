"""Camada de acesso a dados: sabe falar com o Supabase e nada mais.

Nao conhece Gradio, Tkinter nem regras de negocio - apenas conecta,
le e escreve na tabela de vendas.
"""

import sys

from supabase import create_client


class SalesRepository:
    def __init__(self, url: str, key: str, table: str = "vendas"):
        if not url or not key:
            print("Configure SUPABASE_URL e SUPABASE_KEY (veja .env.example).")
            sys.exit(1)
        self.table = table
        self._client = create_client(url, key)

    @classmethod
    def from_config(cls, cfg: dict) -> "SalesRepository":
        return cls(url=cfg["url"], key=cfg["key"], table=cfg.get("table", "vendas"))

    def insert_sale(self, data: dict) -> None:
        self._client.table(self.table).insert(data).execute()

    def list_sales(self) -> list:
        response = self._client.table(self.table).select("*").order("id", desc=True).execute()
        return response.data or []

    def search_sales(self, term: str, field: str = "produto") -> list:
        response = (
            self._client.table(self.table)
            .select("*")
            .order("id", desc=True)
            .ilike(field, f"%{term}%")
            .execute()
        )
        return response.data or []

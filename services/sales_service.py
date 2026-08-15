"""Regras de negocio do cadastro de vendas.

Validacao do formulario e consultas. Nao sabe se quem chamou foi o
Gradio ou o Tkinter, nem como os dados chegam ate o Supabase.
"""

from repositories.sales_repository import SalesRepository


class SalesService:
    def __init__(self, repository: SalesRepository):
        self._repository = repository

    def register_sale(self, produto: str, quantidade, valor_unitario, cliente: str) -> None:
        produto = (produto or "").strip()
        cliente = (cliente or "").strip()

        if not produto:
            raise ValueError("Informe o nome do produto.")
        if quantidade is None or quantidade <= 0:
            raise ValueError("A quantidade precisa ser maior que zero.")
        if valor_unitario is None or valor_unitario <= 0:
            raise ValueError("O valor unitário precisa ser maior que zero.")

        self._repository.insert_sale({
            "produto": produto,
            "quantidade": int(quantidade),
            "valor_unitario": float(valor_unitario),
            "cliente": cliente or None,
        })

    def list_sales(self) -> list:
        return self._repository.list_sales()

    def search_sales(self, term: str, field: str = "produto") -> list:
        term = (term or "").strip()
        if not term:
            return self.list_sales()
        return self._repository.search_sales(term, field)

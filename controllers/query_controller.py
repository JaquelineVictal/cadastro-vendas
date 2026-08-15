"""Controller usado exclusivamente pela interface Tkinter (consulta/leitura).

So expoe listagem e busca - nenhum metodo de escrita existe aqui, o que
torna impossivel a interface de consulta inserir, editar ou excluir dados
por engano.
"""

from services.sales_service import SalesService

COLUMNS = ("id", "produto", "quantidade", "valor_unitario", "cliente", "data_venda")


def _format_currency(value) -> str:
    try:
        return f"R$ {float(value):,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    except (TypeError, ValueError):
        return value or ""


def _format_datetime(value) -> str:
    if not value:
        return ""
    return str(value).replace("T", " ")[:19]


def _as_row(sale: dict) -> tuple:
    return (
        sale.get("id", ""),
        sale.get("produto", ""),
        sale.get("quantidade", ""),
        _format_currency(sale.get("valor_unitario")),
        sale.get("cliente") or "",
        _format_datetime(sale.get("data_venda")),
    )


class SalesQueryController:
    columns = COLUMNS

    def __init__(self, service: SalesService):
        self._service = service

    def list_all(self) -> list:
        return [_as_row(sale) for sale in self._service.list_sales()]

    def search(self, term: str, field: str = "produto") -> list:
        return [_as_row(sale) for sale in self._service.search_sales(term, field)]

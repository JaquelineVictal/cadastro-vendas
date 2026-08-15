"""Controller usado exclusivamente pela interface Gradio (cadastro/escrita).

Nao expoe nenhum metodo de leitura - a interface de consulta usa o
QueryController, nunca este.
"""

from services.sales_service import SalesService


class SalesRegistrationController:
    def __init__(self, service: SalesService):
        self._service = service

    def register(self, produto, quantidade, valor_unitario, cliente) -> str:
        try:
            self._service.register_sale(produto, quantidade, valor_unitario, cliente)
        except ValueError as error:
            return str(error)
        except Exception as error:
            return f"Erro ao salvar: {error}"
        return "Venda registrada com sucesso!"

"""View (Gradio): interface web para cadastrar vendas.

So sabe renderizar o formulario e chamar o RegistrationController -
nao conhece Supabase nem regras de validacao.
"""

import gradio as gr

from config import supabase_config
from controllers.registration_controller import SalesRegistrationController
from repositories.sales_repository import SalesRepository
from services.sales_service import SalesService

repository = SalesRepository.from_config(supabase_config())
controller = SalesRegistrationController(SalesService(repository))

with gr.Blocks(title="Cadastro de Vendas") as app:
    gr.Markdown("# Cadastro de Vendas")
    gr.Markdown("Preencha os campos abaixo para registrar uma nova venda.")

    with gr.Row():
        produto = gr.Textbox(label="Produto", placeholder="Ex.: Notebook")
        cliente = gr.Textbox(label="Cliente", placeholder="Nome do cliente")

    with gr.Row():
        quantidade = gr.Number(label="Quantidade", value=1, minimum=1, precision=0)
        valor_unitario = gr.Number(label="Valor unitário (R$)", value=0.0, minimum=0)

    mensagem = gr.Textbox(label="Status", interactive=False)
    botao_salvar = gr.Button("Salvar venda", variant="primary")

    botao_salvar.click(
        controller.register,
        inputs=[produto, quantidade, valor_unitario, cliente],
        outputs=mensagem,
    )

if __name__ == "__main__":
    app.launch()

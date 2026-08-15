"""View (Tkinter): interface desktop para consultar vendas (somente leitura).

So sabe montar a janela e chamar o QueryController - que nem sequer
expoe um metodo de escrita.
"""

import tkinter as tk
from tkinter import messagebox, ttk

from config import supabase_config
from controllers.query_controller import SalesQueryController
from repositories.sales_repository import SalesRepository
from services.sales_service import SalesService

repository = SalesRepository.from_config(supabase_config())
controller = SalesQueryController(SalesService(repository))

LABELS = {
    "id": "ID",
    "produto": "Produto",
    "quantidade": "Qtd",
    "valor_unitario": "Valor unit.",
    "cliente": "Cliente",
    "data_venda": "Data",
}


def load_rows(rows) -> None:
    tree.delete(*tree.get_children())
    for row in rows:
        tree.insert("", "end", values=row)
    status_var.set(f"{len(rows)} registro(s) encontrado(s).")


def search() -> None:
    try:
        rows = controller.search(search_input.get(), search_type.get())
    except Exception as error:
        messagebox.showerror("Erro", f"Não foi possível buscar os dados:\n{error}")
        status_var.set("Erro na consulta.")
        return
    load_rows(rows)


def refresh_list() -> None:
    search_input.delete(0, tk.END)
    try:
        rows = controller.list_all()
    except Exception as error:
        messagebox.showerror("Erro", f"Não foi possível buscar os dados:\n{error}")
        status_var.set("Erro na consulta.")
        return
    load_rows(rows)


window = tk.Tk()
window.title("Consulta de Vendas")
window.geometry("900x480")
window.minsize(760, 420)

top_frame = tk.Frame(window)
top_frame.pack(fill="x", padx=10, pady=10)

tk.Label(top_frame, text="Buscar por:").pack(side="left")

search_type = tk.StringVar(value="produto")
tk.Radiobutton(top_frame, text="Produto", variable=search_type, value="produto").pack(
    side="left", padx=(6, 4)
)
tk.Radiobutton(top_frame, text="Cliente", variable=search_type, value="cliente").pack(
    side="left", padx=(0, 12)
)

search_input = tk.Entry(top_frame, width=28)
search_input.pack(side="left", padx=(0, 8))
search_input.bind("<Return>", lambda _event: search())

tk.Button(top_frame, text="Consultar", command=search).pack(side="left", padx=(0, 8))
tk.Button(top_frame, text="Atualizar lista", command=refresh_list).pack(side="left")

table_frame = tk.Frame(window)
table_frame.pack(fill="both", expand=True, padx=10, pady=(0, 6))

scroll_y = ttk.Scrollbar(table_frame, orient="vertical")
scroll_x = ttk.Scrollbar(table_frame, orient="horizontal")

tree = ttk.Treeview(
    table_frame,
    columns=controller.columns,
    show="headings",
    yscrollcommand=scroll_y.set,
    xscrollcommand=scroll_x.set,
)

scroll_y.config(command=tree.yview)
scroll_x.config(command=tree.xview)

for column in controller.columns:
    tree.heading(column, text=LABELS[column])
    width = 180 if column == "produto" else 110
    tree.column(column, width=width, anchor="center")

tree.grid(row=0, column=0, sticky="nsew")
scroll_y.grid(row=0, column=1, sticky="ns")
scroll_x.grid(row=1, column=0, sticky="ew")

table_frame.rowconfigure(0, weight=1)
table_frame.columnconfigure(0, weight=1)

status_var = tk.StringVar(value="Carregando...")
tk.Label(window, textvariable=status_var, anchor="w").pack(fill="x", padx=10, pady=(0, 10))

if __name__ == "__main__":
    refresh_list()
    window.mainloop()

-- Execute no SQL Editor do Supabase (o Table Editor tambem funciona).
-- Esta e a "migration" de referencia da tabela usada pelas duas interfaces.

create table vendas (
    id bigint generated always as identity primary key,
    produto text not null,
    quantidade integer not null,
    valor_unitario numeric(10, 2) not null,
    cliente text,
    data_venda timestamp with time zone default now()
);

-- Para esta atividade didatica: desative o RLS na tabela pelo Table Editor
-- (Table Editor > vendas > ... > Disable RLS), ou crie policies de
-- select/insert para o papel anon. Sem isso, o Gradio nao consegue
-- gravar e o Tkinter nao consegue ler.

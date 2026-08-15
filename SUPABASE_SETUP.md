# Passo a passo: Supabase

## 1. Criar a conta e o projeto

1. Acesse https://supabase.com e crie uma conta gratuita (pode usar login com GitHub ou Google).
2. Clique em **New project**, escolha um nome (ex.: `cadastro-vendas`), defina uma senha forte para
   o banco (anote-a — é diferente da API key) e escolha uma região (ex.: South America - São Paulo).
3. Aguarde alguns instantes enquanto o Supabase provisiona o banco.

## 2. Criar a tabela `vendas`

No menu lateral, abra **SQL Editor** e execute o conteúdo de [`db/schema.sql`](db/schema.sql):

```sql
create table vendas (
    id bigint generated always as identity primary key,
    produto text not null,
    quantidade integer not null,
    valor_unitario numeric(10, 2) not null,
    cliente text,
    data_venda timestamp with time zone default now()
);
```

## 3. Desativar o RLS (Row Level Security)

Por padrão, o Supabase ativa o RLS, que bloqueia qualquer leitura ou escrita até existir uma policy.
Para esta atividade didática, a forma mais simples é:

**Table Editor → tabela `vendas` → menu "..." → Disable RLS**

Se preferir a abordagem mais correta (mas mais avançada), crie policies de `select` e `insert` para o
papel `anon` em vez de desativar o RLS.

> Se aparecer o erro `new row violates row-level security policy`, é exatamente isso — volte a este
> passo.

## 4. Obter a URL e a chave (anon key)

1. No menu lateral: **Project Settings → API**.
2. Copie o **Project URL** (algo como `https://xxxxxxxx.supabase.co`).
3. Copie a **anon public** key (chave longa, formato JWT) — **não** a `service_role`, que é secreta e
   não deve ser usada em código cliente.

## 5. Configurar o projeto local

```bash
cp .env.example .env
```

Edite `.env`:

```
SUPABASE_URL=https://xxxxxxxx.supabase.co
SUPABASE_KEY=sua_anon_key_aqui
SALES_TABLE=vendas
```

Esse arquivo não é versionado (está no `.gitignore`).

## 6. Testar

```bash
python cadastro_vendas_app.py
```

Cadastre uma venda de teste e confira em **Table Editor → vendas** no painel do Supabase se o
registro apareceu. Depois rode `python consulta_vendas_app.py` e clique em "Atualizar lista" para
ver o mesmo registro na interface desktop.

## Erros comuns

| Erro | Causa | Solução |
|---|---|---|
| `new row violates row-level security policy` | RLS ativo sem policy | Desative o RLS (passo 3) |
| `invalid API key` | Chave errada ou com espaços | Confira se copiou a `anon public`, não a `service_role` |
| Tkinter abre mas a tabela fica vazia | Tabela vazia ou nome de coluna diferente | Confira no Table Editor; nomes de coluna são case-sensitive |
| Erro de conexão / timeout | Projeto pausado por inatividade | Acesse o painel do Supabase para reativar o projeto |

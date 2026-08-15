# Cadastro de Vendas — Gradio + Tkinter + Supabase

Atividade Aula 2: evolução do Sistema de Cadastro de Vendas (antes em SQLite local) para um banco
central na nuvem no [Supabase](https://supabase.com), acessado por **duas interfaces
independentes**:

- **Gradio** (web): cadastra novas vendas — somente escrita.
- **Tkinter** (desktop): consulta as vendas já cadastradas — somente leitura.

Ambas conversam com o mesmo banco Postgres gerenciado pelo Supabase, exatamente como
aplicações distintas (site, app, sistema interno) acessam uma fonte de dados única em sistemas
profissionais.

## Arquitetura

Mesma separação em camadas usada no projeto do dashboard de COVID, adaptada para duas views
em vez de uma:

```
config.py                          # le as credenciais do Supabase de variaveis de ambiente
repositories/
  sales_repository.py              # acesso a dados: conecta, le e escreve na tabela vendas
services/
  sales_service.py                 # regras de negocio: validacao do cadastro e consultas
controllers/
  registration_controller.py       # usado SO pelo Gradio - so expoe register()
  query_controller.py              # usado SO pelo Tkinter - so expoe list_all()/search()
cadastro_vendas_app.py             # view (Gradio): formulario de cadastro
consulta_vendas_app.py             # view (Tkinter): tela de consulta
db/schema.sql                      # migration de referencia da tabela vendas
```

- **repository**: só sabe falar com o Supabase. Não conhece Gradio, Tkinter nem regras de negócio.
- **service**: validação (produto obrigatório, quantidade e valor > 0) e consultas. Não sabe quem chamou.
- **controllers**: aqui a separação é o ponto central da atividade — `SalesRegistrationController`
  só expõe `register()` (usado pelo Gradio) e `SalesQueryController` só expõe `list_all()`/`search()`
  (usado pelo Tkinter). Não é só uma convenção: a interface de consulta **não tem, no código, como**
  inserir, editar ou excluir — o método simplesmente não existe naquele controller.
- **views**: `cadastro_vendas_app.py` e `consulta_vendas_app.py` só montam a UI e chamam o
  controller correspondente.

## Pré-requisitos

- Conta no [Supabase](https://supabase.com) (plano gratuito)
- Python 3.11+

## 1. Configurar o Supabase

Veja o passo a passo detalhado em [`SUPABASE_SETUP.md`](SUPABASE_SETUP.md).

Resumo:
1. Criar projeto no Supabase.
2. Rodar [`db/schema.sql`](db/schema.sql) no SQL Editor para criar a tabela `vendas`.
3. Desativar o RLS da tabela (ou criar policies de `select`/`insert` para `anon`).
4. Copiar a URL do projeto e a `anon public key` em Project Settings → API.

## 2. Preparar o ambiente local

```bash
python3 -m venv .venv
source .venv/bin/activate      # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env            # preencha SUPABASE_URL e SUPABASE_KEY
```

## 3. Rodar as duas interfaces

```bash
python cadastro_vendas_app.py   # abre em http://localhost:7860 - cadastra vendas
python consulta_vendas_app.py   # abre uma janela desktop - consulta vendas
```

Cadastre algumas vendas pelo Gradio e clique em "Atualizar lista" no Tkinter para confirmar que as
duas interfaces enxergam o mesmo banco.

## Entregáveis desta atividade

- Código-fonte completo em Python (este repositório).
- URL e `anon key` do projeto Supabase, entregues ao professor **fora do Git** (ver
  `CREDENCIAIS_ENTREGA.txt`, que é gerado localmente e está no `.gitignore` — nunca é commitado).

> Por que fora do Git? Em projetos reais, credenciais nunca vão para um repositório, mesmo
> privado. Para esta atividade didática o próprio guia autoriza enviar URL + anon key ao professor,
> mas por um canal separado do código-fonte — é esse hábito que vale carregar para projetos reais.

# ZeloAtivo - Frontend MVP

O **ZeloAtivo** é um aplicativo focado na gestão de medicamentos com foco em acessibilidade e segurança para idosos e seus cuidadores.

## Stack Tecnológica
* **Linguagem:** Python 3.10+
* **Framework:** [Flet](https://flet.dev/) (Motor Flutter com sintaxe Python)
* **Backend:** FastAPI (Python)
* **Banco de Dados:** Supabase

## Pré-requisitos para a Equipe
Antes de começar, certifique-se de ter o Python instalado. Recomendamos o uso de um ambiente virtual (venv):

1.  **Clone o repositório:**
    `git clone https://github.com/sua-equipe/zeloativo-app.git`
2.  **Crie o ambiente virtual:**
    `python -m venv venv`
3.  **Ative o venv:**
    * Windows: `.\venv\Scripts\activate`
    * Linux/Mac: `source venv/bin/activate`
4.  **Instale as dependências:**
    `pip install -r requirements.txt`

## Funcionalidades do MVP
- [ ] **Fluxo de Autenticação:** Login e Cadastro com Telefone.
- [ ] **Home Inteligente:** Botão SOS persistente e lista de doses em cards de alto contraste.
- [ ] **Gestão de Doses:** Bottom sheet para registro de tomada ou adiamento (15min/1h).
- [ ] **Monitoramento:** Tela de histórico semanal e "Semáforo de Saúde" para dependentes compartilhados.
- [ ] **Configurações:** Vínculo de cuidador via código de 6 dígitos.

## Guia de Estilo (UI/UX)
* **Cores:** Vermelho Vivo (#FF0000) para SOS, Verde para "Tomei", Amarelo para "Atenção".
* **Contraste:** Priorizar textos grandes e elementos com alta legibilidade.
* **Navegação:** Menu inferior fixo para fácil alcance com o polegar.

## Como rodar o projeto
Para iniciar o app em modo de desenvolvimento (com hot reload):
`flet run src/main.py`
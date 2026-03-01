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
    `git clone https://github.com/Arthur-Monteir0/zeloativo-app`
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

## 🎨 Guia de Estilo & Acessibilidade (WCAG)

Como o foco do **ZeloAtivo** é o público 60+, a escolha das cores segue critérios rigorosos de contraste e legibilidade:

| Cor | Hexadecimal | Papel no App | Observação de Acessibilidade |
| :--- | :--- | :--- | :--- |
| **Principal** | `#5CC6BA` | Áreas decorativas / Detalhes | **Cuidado:** Contraste baixo (~2.2:1). **Não usar** texto branco sobre esta cor. |
| **Fundo** | `#FFFFFF` | Telas e Cards | Mantém o visual limpo e facilita o descanso visual. |
| **Texto/Secundária**| `#092C4C` | Títulos e Textos | **Cor ideal para leitura.** Alto contraste com o fundo branco. |
| **Alerta/SOS** | `#FF222D` | Botão SOS e Atrasos | Alta visibilidade. Usada para ações críticas e urgências. |

### ⚠️ Regras de Ouro para o Front-end:
* **Tamanho de Fonte:** Mínimo de `18px` para textos de corpo e `24px` para títulos.
* **Toque Facilitado:** Botões devem ter altura mínima de `55px` para facilitar o clique de pessoas com tremores leves ou dificuldade motora.
* **Ícones:** Sempre acompanhados de texto (ex: Ícone de engrenagem + palavra "Ajustes").
* **Contraste:** Sempre que usar a cor **Verde Água (#5CC6BA)** em um fundo, o texto sobre ele deve ser o **Azul Marinho (#092C4C)**, nunca branco.


## Como rodar o projeto
Para iniciar o app em modo de desenvolvimento (com hot reload):
`flet run src/main.py`

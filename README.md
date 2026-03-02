ZeloAtivo - Frontend MVP
O ZeloAtivo é um aplicativo focado na gestão de medicamentos com foco em acessibilidade e segurança para idosos e seus cuidadores.

Stack Tecnológica
Linguagem: Python 3.10+
Framework: Flet (Motor Flutter com sintaxe Python)
Backend: FastAPI (Python)
Banco de Dados: Supabase
Pré-requisitos para a Equipe
Antes de começar, certifique-se de ter o Python instalado. Recomendamos o uso de um ambiente virtual (venv):

Clone o repositório: git clone https://github.com/Arthur-Monteir0/zeloativo-app
Crie o ambiente virtual: python -m venv venv
Ative o venv:
Windows: .\venv\Scripts\activate
Linux/Mac: source venv/bin/activate
Instale as dependências: pip install -r requirements.txt
Funcionalidades do MVP
 Fluxo de Autenticação: Login e Cadastro com Telefone.
 Home Inteligente: Botão SOS persistente e lista de doses em cards de alto contraste.
 Gestão de Doses: Bottom sheet para registro de tomada ou adiamento (15min/1h).
 Monitoramento: Tela de histórico semanal e "Semáforo de Saúde" para dependentes compartilhados.
 Configurações: Vínculo de cuidador via código de 6 dígitos. Guia de Estilo & Acessibilidade (WCAG) Como o foco do ZeloAtivo é o público 60+, a escolha das cores e componentes segue critérios rigorosos de contraste e legibilidade, visando reduzir a carga cognitiva e facilitar a navegação.
Cor,Hexadecimal,Papel no App,Observação de Acessibilidade Principal,#5CC6BA,Áreas decorativas e detalhes,Contraste baixo (~2.2:1). Nunca usar texto branco sobre ela. Secundária,#092C4C,Títulos e Textos,Cor base para leitura. Alto contraste sobre o fundo branco. Terciária,#FF7F50,Botões de Ação (CTA),Cor de destaque para ações principais que não são urgências. Alerta/SOS,#FF222D,Botão SOS e Atrasos,Alta visibilidade. Exclusiva para ações críticas e emergências. Fundo,#FFFFFF,Telas e Cards,Mantém o visual limpo e evita fadiga visual.

⚠️ Regras de Ouro para o Front-end Para garantir a conformidade com as normas de acessibilidade, todo o desenvolvimento deve seguir estas diretrizes:

Tipografia: * Corpo de texto: Mínimo de 18px.

Títulos: Mínimo de 24px (chegando a 32px em destaques).

Toque Facilitado (Target Size): * Botões devem ter altura mínima de 55px para facilitar o clique de pessoas com tremores leves ou dificuldades motoras finas.

Acessibilidade Visual (Contraste):

Sobre Verde Água (#5CC6BA): Usar sempre texto Azul Marinho (#092C4C).

Sobre Coral (#FF7F50): Recomenda-se o uso de texto Azul Marinho para garantir o contraste AA em ações importantes.

Semântica de Ícones:

Ícones nunca devem estar sozinhos. Devem ser sempre acompanhados de rótulos de texto (ex: ⚙️ + "Ajustes").

Trecho do theme.py
color_scheme=ft.ColorScheme( primary=AppColors.PRIMARY, secondary=AppColors.SECONDARY, error=AppColors.ALERT, surface=AppColors.BACKGROUND, tertiary=AppColors.TERTIARY # Nova cor de destaque )

🛠️ Implementação Técnica (Flet) A lógica de cores está centralizada no arquivo theme.py, garantindo que todo o app respeite a identidade visual e os padrões de acessibilidade:

Como rodar o projeto
Para iniciar o app em modo de desenvolvimento (com hot reload): flet run src/main.py
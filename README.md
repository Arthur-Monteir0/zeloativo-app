ZeloAtivo - Frontend MVP
O ZeloAtivo é uma solução focada na gestão de medicamentos, desenhada especificamente para garantir acessibilidade e segurança para idosos (60+) e seus cuidadores.

Stack Tecnológica

Tecnologia	Descrição
Linguagem	Python 3.10+
Framework	Flet (Motor Flutter com sintaxe Python)
Backend	FastAPI
Banco de Dados	Supabase

Guia de Estilo & Acessibilidade (WCAG)
Para atender ao público sênior, utilizamos cores de alto contraste e elementos visuais que reduzem a carga cognitiva.
Paleta de Cores

Amostra,Cor,Hexadecimal,Papel no App,Observação de Acessibilidade
🟢,Principal,#5CC6BA,Áreas decorativas,Baixo contraste. Nunca usar texto branco sobre ela.
🔵,Secundária,#092C4C,Títulos e Textos,Cor base para leitura. Alto contraste sobre fundo branco.
🟠,Terciária,#FF7F50,Botões (CTA),Destaque para ações principais não urgentes.
🔴,Alerta/SOS,#FF222D,Emergências,Alta visibilidade. Exclusiva para ações críticas.
⚪,Fundo,#FFFFFF,Telas e Cards,Mantém o visual limpo e evita fadiga visual.

Regras de Ouro para o Front-end
Diretrizes obrigatórias para manter a conformidade com as normas de acessibilidade:

Tipografia: * Corpo de texto: Mínimo de 18px.

Títulos: Entre 24px e 32px.

Toque Facilitado (Target Size): * Botões devem ter altura mínima de 55px (ideal para usuários com tremores leves).

Contraste Visual:

Sobre Verde Água (#5CC6BA): Usar sempre texto Azul Marinho (#092C4C).

Sobre Coral (#FF7F50): Usar texto Azul Marinho para garantir contraste AA.

Semântica de Ícones:

Ícones nunca aparecem sozinhos. Devem sempre ter rótulos (Ex: ⚙️ + "Ajustes").

Funcionalidades do MVP
 Fluxo de Autenticação: Login e Cadastro simplificado via Telefone.

 Home Inteligente: Botão SOS persistente e lista de doses em cards de alto contraste.

 Gestão de Doses: Registro de tomada ou adiamento inteligente (15min/1h).

 Monitoramento: Histórico semanal e "Semáforo de Saúde" para dependentes.

 Configurações: Vínculo de cuidador via código de 6 dígitos.

 Implementação Técnica (Flet)
A lógica de cores e temas está centralizada no arquivo theme.py. Abaixo, um trecho da configuração do ColorScheme:

# Trecho do theme.py
color_scheme = ft.ColorScheme(
    primary=AppColors.PRIMARY,
    secondary=AppColors.SECONDARY,
    error=AppColors.ALERT,
    surface=AppColors.BACKGROUND,
    tertiary=AppColors.TERTIARY # Cor de destaque para CTAs
) 
Como Rodar o Projeto
Clone o repositório:
git clone https://github.com/Arthur-Monteir0/zeloativo-app
cd zeloativo-app

Configure o ambiente virtual:
python -m venv venv
# Windows:
.\venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

Instale as dependências:
pip install -r requirements.txt

Inicie o app (com Hot Reload):
flet run src/main.py

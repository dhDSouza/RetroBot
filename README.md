# RetroBot - Bot de Conquistas RetroAchievements para Discord

RetroBot é um bot para Discord que permite que os membros de um servidor de Discord registrem seus nomes de usuário da plataforma RetroAchievements, acompanhem suas conquistas de jogos retrô.

## Funcionalidades

- Comando `!registrar <seu_usuario_retroachievements>` para registrar o seu nome de usuário do RetroAchievements.
- Comando `!conquistas` para buscar as conquistas mais recentes do RetroAchievements.
  
## Pré-requisitos

Antes de começar, você precisará das seguintes ferramentas instaladas/configuradas:

- [Python 3.8+](https://www.python.org/downloads/)
- [Discord Account & Bot Token](https://discord.com/developers/applications)
- Uma conta no [RetroAchievements](https://retroachievements.org/)

Além disso, é recomendável usar um ambiente virtual para gerenciar suas dependências.

## Instalação

1. Clone este repositório para sua máquina local:

    ```bash
    git clone https://github.com/seuusuario/RetroBot.git
    cd RetroBot
    ```

2. Crie e ative um ambiente virtual (opcional, mas recomendado):

    No Linux/macOS:

    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

    No Windows:

    ```bash
    python -m venv venv
    venv\Scripts\activate
    ```

3. Instale as dependências do projeto:

    ```bash
    pip install -r requirements.txt
    ```

4. Crie um arquivo `.env` na raiz do projeto e adicione suas variáveis de ambiente. Este arquivo armazena o token do Discord e a chave da API do RetroAchievements:

    ```bash
    DISCORD_TOKEN=seu_token_do_discord
    RA_API_KEY=sua_chave_da_api_do_retroachievements
    ```

5. Inicialize o banco de dados SQLite:

    O bot irá criar o banco automaticamente ao iniciar. Certifique-se de que a função `create_tables` está sendo chamada no evento `on_ready` no arquivo `main.py`. Nenhuma ação adicional é necessária.

## Como Usar

1. **Iniciar o bot**:

    Para iniciar o bot, rode o seguinte comando:

    ```bash
    python3 main.py
    ```

    Você verá uma mensagem no terminal confirmando que o bot está pronto:

    ```bash
    RetroBot#7626 está pronto!
    ```

2. **Comandos**:

    Dentro do servidor Discord, os membros podem digitar o comando:

    ```bash
    !registrar <seu_usuario_retroachievements>
    ```

    O bot registrará o seu usuário do RetroAchievements.

    ```bash
    !conquistas
    ```

    O bot responderá com as conquistas mais recentes do usuário especificado.

## Licença

Este projeto é licenciado sob os termos da [GNU General Public License v3.0](https://www.gnu.org/licenses/gpl-3.0.html).

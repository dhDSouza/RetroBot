# RetroBot - Bot de Conquistas RetroAchievements para Discord

RetroBot é um bot para Discord que permite que os membros de um servidor registrem seus nomes de usuário da plataforma RetroAchievements e acompanhem suas conquistas de jogos retrô.

## Funcionalidades

- Registrar um usuário do RetroAchievements no servidor Discord.
- Buscar as conquistas mais recentes de um usuário do RetroAchievements.
- Sortear um desafio aleatório de jogo retrô.
- Atualizar o desafio caso não tenha gostado do sorteado.
- Exibir perfil do usário no RetroAchievements.
- Exibir a atividade dos jogadores nos jogos retrô.

## Pré-requisitos

Antes de começar, você precisará das seguintes ferramentas instaladas/configuradas:

- [Python 3.10+](https://www.python.org/downloads/)
- [Discord Account & Bot Token](https://discord.com/developers/applications)
- Uma conta no [RetroAchievements](https://retroachievements.org/)

## Instalação

1. Clone este repositório para sua máquina local:

    ```bash
    git clone https://github.com/dhDSouza/RetroBot.git
    cd RetroBot
    ```

2. Instale o `pipenv` se ainda não estiver instalado:

    ```bash
    pip install pipenv
    ```

3. Crie e ative o ambiente virtual com `pipenv`:

    ```bash
    pipenv install
    pipenv shell
    ```

4. Crie um arquivo `.env` na raiz do projeto e adicione suas variáveis de ambiente:

    ```bash
    DISCORD_TOKEN=seu_token_do_discord
    RA_API_KEY=sua_chave_da_api_do_retroachievements
    CHANNEL=seu_canal_do_discord
    ```

## Como Usar

**Iniciar o bot**:

Para iniciar o bot, rode o seguinte comando:

```bash
pipenv run start
```

## Comandos Disponíveis

- **`!registrar <username do RetroAchievements>`**: Registra o seu nome de usuário do RetroAchievements para acompanhar suas conquistas.
- **`!conquistas`**: Exibe as conquistas do usuário registrado nas últimas 24 horas.
- **`!desafio`**: Sorteia um novo desafio de jogo retrô e exibe os detalhes.
- **`!atualizar_desafio`**: Atualiza o desafio atual com um novo, caso o usuário deseje.
- **`!perfil`**: Exibe o perfil do usuário.
- **`!atividade`**: Exibe a última atividade do usuário.
- **`!ajuda`**: Exibe a lista de comandos disponíveis e uma breve descrição de cada um.

## Documentação e Políticas

- [Termos de Uso](./TERMS_OF_USE.md)
- [Política de Privacidade](./PRIVACY_POLICY.md)

## Licença

Este projeto é licenciado sob os termos da [GNU General Public License v3.0](https://www.gnu.org/licenses/gpl-3.0.html). Você é livre para usar, modificar e distribuir o software, desde que mantenha os créditos e a licença original.

## Referência ao RetroAchievements

O RetroBot utiliza a API do [RetroAchievements](https://retroachievements.org/) para obter dados sobre conquistas e atividades de jogos retrô. Agradecemos ao RetroAchievements por disponibilizar a API e permitir que a comunidade desenvolva ferramentas como esta.

## Como Contribuir

Contribuições são sempre bem-vindas! Siga os passos abaixo para contribuir:

1. Faça um fork deste repositório.
2. Crie uma nova branch para sua feature ou correção:

    ```bash
    git checkout -b minha-feature
    ```

3. Faça as modificações desejadas e commit:

    ```bash
    git commit -m "Adiciona nova funcionalidade"
    ```

4. Envie para o seu fork:

    ```bash
    git push origin minha-feature
    ```

5. Abra um Pull Request descrevendo as mudanças feitas.

## Contato

Se você tiver dúvidas, sugestões ou problemas, fique à vontade para abrir um *issue* ou entrar em contato diretamente através do [dhs.danielsouza@gmail.com](mailto:dhs.danielsouza@gmail.com).

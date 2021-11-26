* # PT-BR 

Calax é um bot de diversão craiado na [comunidade Ballerini](https://discord.gg/wagxzStdcR) inspirado na famosa brincadeira de verdade ou desafio. Seu nome é baseado no personagem demoníaco do filme [Truth or Dare](https://pt.wikipedia.org/wiki/Truth_or_Dare_(2018)). 

&nbsp;
## Configuração
### CONFIGURAÇÕES DO BOT NO DISCORD DEVELOPER PORTAL
Para utilizar o bot, você precisa criar um bot no [Discord Developer Portal](https://discordapp.com/developers/applications/me) e seguir os passos:

`Aplications > New Aplication`

* Dê um nome e crie a aplicação

Pronto você tem uma aplicação criada, agora é só configurar ela, para isso siga os passos:

`Bot > Add Bot`

* Clique em "Yes, do it!"

Agora o seu bot está criado. Para configurá-lo corretamente, siga os passos:

`Bot > Privileged Gateway Intents`

* Habilite as funções PRESENCE INTENT e SERVER MEMBERS INTENT

&nbsp;
### CRIANDO SALAS PARA USAR O BOT
As salaS necessárias para o bot são basicamente 3, uma para autenticação, onde apenas as pessoas com cargo de `bot-master` terão permissão para disparar comandos. Também são necessárias uma sala de texto, onde os usuários podem conversar com o bot. Por fim, uma sala de voz, onde os usuários podem interagir entre si. Dependendo da sua demanda, podem ser criadas muitas outras mais salas de texto e voz.

&nbsp;
### CONFIGURAÇÕES DAS SALAS

Autenticação
* @everyone
    * Permissões habilitadas: 
        * Visualizar canal
        * Ler histórico de mensagens
    * Permissões desabilitadas:
        * Gerenciar canal
        * Gerenciar permissões
        * Gerenciar webhooks
        * Enviar mensagens
        * Enviar mensagens em threads
        * Criar threads públicas
        * Criar threads privadas
        * Embutir links
        * Anexar arquivos
        * Adicionar reações
        * Gerenciar mensagens
        * Gerenciar threads
        * Usar comandos de aplicação

* @bot-master
    * Permissões habilitadas: 
        * Todas as permissões

Canais de Texto:
* @everyone
    * Permissões habilitadas: 
        * Visualizar canal
        * Ler histórico de mensagens
        * Enviar mensagens
        * Enviar mensagens em threads
        * Adicionar reações
        * Usar emojis externos
        * Usar figurinhas externas

    * Permissões desabilitadas:
        * Gerenciar canal
        * Gerenciar permissões
        * Gerenciar webhooks
        * Criar threads públicas
        * Criar threads privadas
        * Embutir links
        * Anexar arquivos
        * Gerenciar mensagens
        * Gerenciar threads
        * Usar comandos de aplicação

* @bot-master
    * Permissões habilitadas: 
        * Todas as permissões

Canais de voz:
* @everyone
    * Permissões habilitadas:
        * Conectar-se ao canal
        * Falar
        * Vídeo
    
* @bot-master
    * Permissões habilitadas:
        * Todas as permissões

&nbsp;
### CONFIGURAÇÕES DO CÓDIGO

Para que o código funcione corretamente, é necessário que você tenha instalado as bibliotecas [Discord.py](https://pypi.org/project/discord.py/),  [Pandas](https://pypi.org/project/pandas/) e [openpyxl](https://pypi.org/project/openpyxl/).

No arquivo de [credenciais](https://github.com/MateusSantosMeuBem/calax_v_python/blob/main/modules/credentials/__init__.py) você deve informar o token do bot, o ID da sala de autenticação, o ID da sala de texto e o ID da sala e ID do mestre do bot para cada sala de voz como dado inteiro. Por exemplo:

```python
bot_token = 'Okklvnkjgnjkgkjeg.bkhb1d5f6sd6'
auth_channel_id = 123456789123456
auth_msg_id = 123456789123456

# Each key is a voice channel id and the values are informations about the channel
channels_ids = {
                # First voice channel
                123456789123456 :
                  {
                  # Persons who are playing in the channel
                  'mem_play_id' : [], 
                  # Persons who are in the voice channel
                  'mem_vc_id' : [],
                  # Persons who just voted
                  'votes' : [],
                  'txt_channel_id' : 123456789123456,
                  'vote_msg_id' : None,
                  'auth_channel_id' : auth_channel_id,
                  'auth_msg_id' : auth_msg_id,
                  'last_ctx' : None,
                  # Context of the First iniciar()
                  'master_ctx' : None,
                  'bot_master' : 123456789123456,
                  'asker' : None,
                  'victim' : None,
                  # This variable controlls in which turn the game is
                  'ctrl' : 0,
                  # Pointer that point to the player of the time in mem_play_id
                  'turn' : 0,
                  # Option choosed by the player
                  'switch' : None,
                  'g' : None,
                  # How many times they choose the same option
                  'truth' : {}
                  }
                }
```
Caso precise criar mais salar, basta duplicar o dicionário dentro de `channels_ids` e informar os IDs necessários.

### CONFIGURAÇÃO DO BANCO DE DADOS DE PERGUNTAS E DESAFIOS

Para que qualquer pessoa possa adicionar ou excluir perguntas e desafios sem um conhecimento prévio de banco de dados, utilizuou-se uma tabela Excel, onde a primeira coluna corresponde às perguntas e a segunda aos desafios.

&nbsp;
## COMANDOS

Para chamar qualquer comando, basta digitar `??` antes do comando. Por exemplo, para chamar o comando `iniciar`, basta digitar `??iniciar`.
Os comandos disponíveis são:
* `show_list` - Mostra os participantes do jogo na sala do mestre.
* `iniciar` - Inicia o jogo.\
Semelhantes: `inicia`, `começa`, `comeca`, `play`
* `girar` - Determina quem vai responder verdade ou consequência.\
Semelhantes: gira, roda, rodar, spin
* `op` + `<opção>` - Determina qual opção o jogador escolheu, `v` se for verdade ou `c` se for consequência. Por exemplo, `??op v` ou `??op c`.\
Semelhantes: `opção`, `opcao`, `option`
* `ajuda` - Escolhe uma pergunta ou um desafio aleatório.\
Semelhantes: `ajd`, `help`
* `feito` - Comando usado quando a vítima responde. Após ele inicia-se a votação.\
Semelhantes: `done`
* `reload` - Reinicia a rodada.
* `proximo` - Passa a vez para o próximo jogador.\
Semelhantes: `next`
* `info` - Mostra no terminal informações sobre o jogo em todas as salas.
* `exitPlayer` + `<id_jogador>` + `<opção>` - Remove o jogador. Se `<opção>` for 1, remove da lista de jogagores que estão jogando, se for 2, remove da lista de voz, se for 3, remove de ambas. Por exemplo, `??exitPlayer 123456789123456 1` ou `??exitPlayer 123456789123456 2`.
* `setBotMaster` + `<id_canal_de_voz>` + `<id_novo_bot_master>` - Define o novo bot master. Por exemplo, `??setBotMaster 123456789123456 123456789123456`.
* `regras` - Mostra as regras do jogo.
Semelhantes: `regra`, `rules`, `rule`
* `add_message` - Adciona a mensagem de autenticação.

Na primeira vez que o bot é iniciado, você deve chamar o comando `??add_message` no canal de autenticação, adicionar o id da mensagem ao código e reiniciar o bot.

&nbsp;
## REGRAS DO JOGO

1. Para participar do jogo, o jogador precisa se autenticar no canal de autenticação reagindo com o emoji de autenticação.
2. Para se autenticar, o jogador deve estar em um canal de voz da brincadeira.
3. Na sala de texto, o bot master deve digitar `??iniciar` para iniciar o jogo e o bot irá escolher alguém para girar.
4. Após girar, o bot irá escolher um jogador para responder e essa pessoa precisa escolher entre verdade ou consequência.
5. Após responder, essa pessoa deve digitar `??feito` para iniciar a votação.
6. Após a votação, o bot irá indicar a próxima pessoa a girar. A ordem é definida pela ordem de autenticação.
7. Quando a última pessoa da sala girar, o bot recomeça do início.


&nbsp;
* # EN-US 

Calax is a fun bot made in [Ballerini](https://discord.gg/wagxzStdcR) inspired by the famous game called truth or dare. Its name is from the demonic character in [Truth or Dare](https://pt.wikipedia.org/wiki/Truth_or_Dare_(2018)). 

&nbsp;
## CONFIGURATION
### BOT CONFIGURATIONS IN DISCORD DEVELOPER PORTAL
To use it, you should make a bot in [Discord Developer Portal](https://discordapp.com/developers/applications/me) and to fallow the steps:

`Aplications > New Aplication`

* Give it a name and create application

Now you have a application created, now it's time to configure it, follow the steps:

`Bot > Add Bot`

* Click on "Yes, do it!"

Now your bot is created. To configure it correctly, follow the steps:

`Bot > Privileged Gateway Intents`

* Set on PRESENCE INTENT and SERVER MEMBERS INTENT

&nbsp;
### MAKING CHANNELS TO USE THE BOT
The necessary channels to use the bot are basically 3, one for authentication, where only people with the `bot-master` role will be able to use commands. Also, there is a text channel, where users can talk with the bot. Finally, a voice channel, where users can interact with each other. Depending on your demand, you can create more text and voice channels.

&nbsp;
### CHANNELS CONFIGURATIONS

Authentication
* @everyone
    * Allowed permissions:
        * View channel
        * Read message history
    * Unallowed permissions:
        * Menage channel
        * Menage permissions
        * Menage webhooks
        * Send messages
        * Send messages in thread
        * Create public threads
        * Create private threads
        * Emebed links
        * Attach files
        * Add reactions
        * Mesange messages
        * Menage threads
        * Use application Commands

* @bot-master
    * Allowed permissions: 
        * All permissions 

Text channels:
* @everyone
    * Allowed permissions: 
        * View channel 
        * Read message history
        * Send messages
        * Send messages in thread
        * Add reactions
        * Use external emojis
        * Use external stickers

    * Unallowed permissions:
        * Menage channel
        * Menage permissions
        * Menage webhooks
        * Create public threads
        * Create private threads
        * Emebed links
        * Attach files
        * Menage messages
        * Menage threads 
        * Use application Commands

* @bot-master
    * Allowed permissions: 
        * All permissions

Voice channels:
* @everyone
    * Allowed permissions:
        * Connect
        * Speak
        * Video
    
* @bot-master
    * Allowed permissions:
        * All permissions

&nbsp;
### CODE CONFIGURATIONS


For code to work correctly, you need to install [Discord.py](https://pypi.org/project/discord.py/) and [Pandas](https://pypi.org/project/pandas/) and [Openpyxl](https://pypi.org/project/openpyxl/).

In file [credenciais](https://github.com/MateusSantosMeuBem/calax_v_python/blob/main/modules/credentials/__init__.py) you should set bot token, authentication channel ID, text channel ID and bot master ID for each voice channel as integer. For example:

```python
bot_token = 'Okklvnkjgnjkgkjeg.bkhb1d5f6sd6'
auth_channel_id = 123456789123456
auth_msg_id = 123456789123456

# Each key is a voice channel id and the values are informations about the channel
channels_ids = {
                # First voice channel
                123456789123456 :
                  {
                  # Persons who are playing in the channel
                  'mem_play_id' : [], 
                  # Persons who are in the voice channel
                  'mem_vc_id' : [],
                  # Persons who just voted
                  'votes' : [],
                  'txt_channel_id' : 123456789123456,
                  'vote_msg_id' : None,
                  'auth_channel_id' : auth_channel_id,
                  'auth_msg_id' : auth_msg_id,
                  'last_ctx' : None,
                  # Context of the First iniciar()
                  'master_ctx' : None,
                  'bot_master' : 123456789123456,
                  'asker' : None,
                  'victim' : None,
                  # This variable controlls in which turn the game is
                  'ctrl' : 0,
                  # Pointer that point to the player of the time in mem_play_id
                  'turn' : 0,
                  # Option choosed by the player
                  'switch' : None,
                  'g' : None,
                  # How many times they choose the same option
                  'truth' : {}
                  }
                }
```
If you need to create more channels, just duplicate the dictionary inside `channels_ids` and inform the IDs necessary.

### QUESTIONS AND ANSWERS DATABASE CONFIGURATION

To any person be able to add or delete questions and challenges without a previous knowledge about database, we used an Excel table, where the first column corresponds to the questions and the second to the challenges.

&nbsp;
## COMMAND LIST

To call any command, just type `??` before the command. For example, to call the command `iniciar`, just type `??iniciar`.
* `show_list` - Shows the players in the game in the master channel.
* `play` - Starts the game.\
Similar: `iniciar`, `inicia`, `começa`, `comeca`
* `spin` - Determines who will answer the truth or consequence.\
Similar: `gira`, `roda`, `rodar`, `girar`
* `op` + `<opção>` - Determines which option the player chose, `v` if it's the truth or `c` if it's the consequence. For example, `??op v` or `??op c`.\
Similar: `opção`, `opcao`, `option`
* `help` - Choose a question or a random challenge.
Similar: `ajd`, `ajuda`
* `done` - Command used when the victim responds. After it starts the voting.\
Similar: `feito`
* `reload` - Restarts the round.
* `next` - Skip the current player.\
Similar: `proximo`
* `info` - Shows in terminal informations about the game in all channels.
* `exitPlayer` + `<id_player>` + `<option>` - Removes the player. If `<option>` is 1, removes from the list of players playing, if it's 2, removes from the list of voice, if it's 3, removes from both. For example, `??exitPlayer 123456789123456 1` or `??exitPlayer 123456789123456 2`.
* `setBotMaster` + `<id_canal_de_voz>` + `<id_novo_bot_master>` - Define o novo bot master. Por exemplo, `??setBotMaster 123456789123456 123456789123456`.
* `setBotMaster` + `<id_voice_channel>` + `<id_new_bot_master>` - Defines the new bot master. For example, `??setBotMaster 123456789123456 123456789123456`.
* `rules` - Shows the rules of the game.\
Similar: `regra`, `regras`, `rule`
* `add_message` - Adds the authentication message.

First time you start the bot, you must call the command `??add_message` in the authentication channel, add the id of the message to the code and restart the bot.

&nbsp;
## GAME RULES

1. To play, the player must authenticate in the authentication channel reacting with the authentication emoji.
2. To authenticate, the player must be in a voice channel of the game.
3. In the text channel, the bot master must type `??play` to start the game and the bot will choose someone to spin.
4. After spinning, the bot will choose a player to answer and this person must choose between truth or consequence.
5. After answering, this person must type `??done` to start the voting.
6. After the voting, the bot will indicate the next person to spin. The order is defined by the order of authentication.
7. When the last person spin, the bot restarts from the beginning.

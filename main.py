import discord, pandas as pd
from modules.utils import *
from modules.credentials import *
from random import randint
from discord.ext import commands
from time import sleep


# VICTIM = person who needs to answer
# ASKER = persin who needs to ask

# Matan's solutions for the problem with not seeing
# the members in the channel
intents = discord.Intents().all()

client = commands.Bot(command_prefix = '??', case_insensitive = True, intents = intents, help_command = None)

# Challenges and questions sugestions
global qtn_df
qtn_df = pd.read_excel('questoes.xlsx')
# How many challenges or questions sugestions
global h_qtn_df
h_qtn_df = len(list(qtn_df.index))
# dct = {'response': <CIMultiDictProxy('Date': 'Tue, 16 Nov 2021 15:08:32 GMT', 'Content-Type': 'application/json', 'Content-Length': '45', 'Connection': 'keep-alive', 'strict-transport-security': 'max-age=31536000; includeSubDomains; preload', 'x-ratelimit-bucket': '6dbc69cfc052415b46209f835f11e3c0', 'x-ratelimit-limit': '5', 'x-ratelimit-remaining': '4', 'x-ratelimit-reset': '1637075317.395', 'x-ratelimit-reset-after': '5.000', 'x-envoy-upstream-service-time': '28', 'Via': '1.1 google', 'Alt-Svc': 'h3=":443"; ma=86400, h3-29=":443"; ma=86400, h3-28=":443"; ma=86400, h3-27=":443"; ma=86400', 'CF-Cache-Status': 'DYNAMIC', 'Expect-CT': 'max-age=604800, report-uri="https://report-uri.cloudflare.com/cdn-cgi/beacon/expect-ct"', 'Report-To': '{"endpoints":[{"url":"https:\\/\\/a.nel.cloudflare.com\\/report\\/v3?s=ozEysyK6j9Bg88KNFv%2Fd%2FR6%2F8UmSzNlP3TDxJyYIdpyjZjFZygQR0MIhYP7f%2B0Rk2wt1DjjmzP6wflp%2Fqxat23PwS2N19KdqH3I7uO2I6UabfVqWodRu%2B%2FIPOViB"}],"group":"cf-nel","max_age":604800}', 'NEL': '{"success_fraction":0,"report_to":"cf-nel","max_age":604800}', 'X-Content-Type-Options': 'nosniff', 'Server': 'cloudflare', 'CF-RAY': '6af1a29dfe3ff677-GRU')>, 'status': 404, 'code': 10008, 'text': 'Unknown Message'}

# Shows when bot is ready to be used (hehe)
@client.event
async def on_ready():
  for _, v in channels_ids.items():
    auth_msg_id = v['auth_msg_id']
    auth_channel_id = v['auth_channel_id']
    try:
      channel = client.get_channel(auth_channel_id)
      message = await channel.fetch_message(auth_msg_id)
      await message.clear_reaction("👍")
      await message.add_reaction("👍")
    except Exception as e:
      code = eval(str(e.response._body).replace("b", "").replace(r"'", ""))['code']
      if code == 10008:
        print("Auth-message not found")
        continue

  print(f'{client.user} has connected to Discord!')
  for n_vc_channel_id in channels_ids.keys():
    # It get the channel with id informed
    voice_channel = client.get_channel(n_vc_channel_id)
    # Get members in the voice channel
    members = voice_channel.members

    for member in members:
      if member.id not in channels_ids[n_vc_channel_id]['mem_vc_id']:
        channels_ids[n_vc_channel_id]['mem_vc_id'].append(member.id)


  print(f'Tamo dentro.\nP.s.: {client.user}')

@client.event
async def close():
  for _, v in channels_ids.items():
    auth_msg_id = v['auth_msg_id']
    auth_channel_id = v['auth_channel_id']
    try:
      channel = client.get_channel(auth_channel_id)
      message = await channel.fetch_message(auth_msg_id)
      await message.clear_reaction("👍")
      await message.add_reaction("👍")
    except Exception as e:
      code = eval(str(e.response._body).replace("b", "").replace(r"'", ""))['code']
      if code == 10008:
        print("Auth-message not found")
        continue
    print('ME DERRUBARAM AQUI!')


@client.event
async def on_message(message):
  user = message.author.id
  user_name = client.get_user(user)
  n_vc_channel_id = returnChannelIdByUserId(message.author.id, 'mem_vc_id')
  bot_master = returnChannelIdByBotMaterId(message.author.id, 'bot_master')
  # If user is in voice channel and the channel is the game channel
  if n_vc_channel_id:
    if channels_ids[n_vc_channel_id]['txt_channel_id'] == message.channel.id:
      if message.channel.id == channels_ids[n_vc_channel_id]['txt_channel_id']:
        if user not in channels_ids[n_vc_channel_id]['mem_play_id'] and not message.author.bot:
          await message.delete()
          await user_name.send(f'<@{user}>, você só pode mandar mensagem nesse chat se estiver jogando.')
        await client.process_commands(message)
      elif user == channels_ids[n_vc_channel_id]['bot_master']:
          await client.process_commands(message)

  if bot_master and channels_ids[bot_master]['auth_channel_id'] == message.channel.id:
    await client.process_commands(message)
    
          

@client.event
async def on_raw_reaction_add(payload):
  user = client.get_user(payload.user_id)
  n_vc_channel_id = returnChannelIdByUserId(payload.user_id, 'mem_vc_id')
  n_channel_id = payload.channel_id
  # If user is in voice channel and the channel is the game channel
  if n_vc_channel_id and payload.user_id in channels_ids[n_vc_channel_id]['mem_vc_id']:
    voice_channel = client.get_channel(n_vc_channel_id)
    # Get members in the voice channel
    members = voice_channel.members
    channel = client.get_channel(payload.channel_id)
    message = await channel.fetch_message(payload.message_id)

    if payload.message_id == channels_ids[n_vc_channel_id]['auth_msg_id']:
      if payload.user_id not in channels_ids[n_vc_channel_id]['mem_play_id'] and payload.user_id != client.user.id:
        channels_ids[n_vc_channel_id]['mem_play_id'].append(payload.user_id)
        await user.send(f'<@{payload.user_id}>, agora você está no jogo.')

    # VOTES FOR THE GAME
    if payload.message_id == channels_ids[n_vc_channel_id]['vote_msg_id'] and payload.user_id != client.user.id:
      # If the user is in the game, it haven't voted yet and it is not the victim
      if payload.user_id in channels_ids[n_vc_channel_id]['mem_play_id'] and payload.user_id not in channels_ids[n_vc_channel_id]['votes'] and payload.user_id != channels_ids[n_vc_channel_id]['victim']:
        channels_ids[n_vc_channel_id]['votes'].append(payload.user_id)
      # if is not in the play, it can't vote
      else:
        try:
          await message.remove_reaction(payload.emoji.name, user)
        except:
          await message.remove_reaction(payload.emoji.name, user)
          
      # If the user is the victim, it can't vote
      if payload.user_id == channels_ids[n_vc_channel_id]['victim']:
        try:
          await message.remove_reaction(payload.emoji.name, user)
        except:
          await message.remove_reaction(payload.emoji.name, user)
  else:
    if payload.channel_id in TXT_CHANNELS_IDS:
      if payload.user_id != client.user.id:
        channel = client.get_channel(payload.channel_id)
        message = await channel.fetch_message(payload.message_id)
        await message.remove_reaction("👍", user)
        await user.send(f'<@{payload.user_id}>, você precisa estar no canal de voz para participar.')
    else:
      print('Alguém reagiu em um canal que não é de jogo.')



@client.event
async def on_raw_reaction_remove(payload):
  user = client.get_user(payload.user_id)
  n_vc_channel_id = returnChannelIdByUserId(payload.user_id, 'mem_vc_id')
  # If user is in voice channel and the channel is the game channel
  if n_vc_channel_id and payload.user_id in channels_ids[n_vc_channel_id]['mem_vc_id']:
    # If it is auth message
    if payload.message_id == channels_ids[n_vc_channel_id]['auth_msg_id']:
      # If user is in the voice channel
      if payload.user_id in channels_ids[n_vc_channel_id]['mem_play_id']:
        channels_ids[n_vc_channel_id]['mem_play_id'].remove(payload.user_id)
        await user.send(f'<@{payload.user_id}>, você não pode sair do jogo. Vai pagar por isso!😈')
  
    if payload.message_id == channels_ids[n_vc_channel_id]['vote_msg_id'] and payload.user_id != client.user.id:
      if payload.emoji.name in ["👍", "👎"] and payload.user_id in channels_ids[n_vc_channel_id]['votes']:
        channels_ids[n_vc_channel_id]['votes'].remove(payload.user_id)
      


@client.event
async def on_voice_state_update(ctx, before, after):
    if before.channel != None:
      b_current_channel_id = before.channel.id

    if after.channel != None:
      a_current_channel_id = after.channel.id


    user = ctx.id
    b = str(before.channel)
    a = str(after.channel)
    # Get inside
    # print(f'Before:{before}', f'\nAfter:{after}')
    if ((b == 'None' and a != 'None') or (b != 'None' and a != 'None')) and (a != b) and after.channel.id in channels_ids.keys():

        if user not in channels_ids[after.channel.id]['mem_vc_id']:
          channels_ids[after.channel.id]['mem_vc_id'].append(user)

        if before.channel and after.channel is not None and before.channel.id != after.channel.id:
          auth_msg_id = channels_ids[before.channel.id]['auth_msg_id']
          txt_channel_id = channels_ids[before.channel.id]['txt_channel_id']
          txt_channel   = client.get_channel(txt_channel_id)
          # Remove reaction from auth message and user from the list
          if user in channels_ids[before.channel.id]['mem_vc_id']:
            channels_ids[before.channel.id]['mem_vc_id'].remove(user)
            channel = client.get_channel(channels_ids[before.channel.id]['auth_channel_id'])
            message = await channel.fetch_message(auth_msg_id)
            user_g  = client.get_user(user)
            await message.remove_reaction("👍", user_g)

          # If this user is in the players list, it takes
          # it off
          if user in channels_ids[before.channel.id]['mem_play_id']:
            channels_ids[before.channel.id]['mem_play_id'].remove(user)
            await ctx.send(f'<@{user}>, você não pode sair do jogo. Vai pagar por isso!😈')

            # If person who left is the victim, it
            # restart round
            try:
              victim = channels_ids[before.channel.id]['victim']
              asker = channels_ids[before.channel.id]['asker']
              if user == victim:
                await txt_channel.send(f'Nossa vítima <@{user}> saiu da sala. Vamos reiniciar a rodada.')
                channels_ids[before.channel.id]['ctrl']   = 0
                channels_ids[before.channel.id]['turn']  -= 1
                channels_ids[before.channel.id]['victim'] = None
                await iniciar(channels_ids[before.channel.id]['master_ctx'])
                  
              elif user == asker:
                await txt_channel.send(f'A pessoa que pergunta saiu da sala. Vamos reiniciar a rodada.')
                channels_ids[before.channel.id]['ctrl']   = 0
                channels_ids[before.channel.id]['asker'] = None
                await iniciar(channels_ids[before.channel.id]['master_ctx'])
            except:
              pass

    # before.channel is not None and after.channel is not None and before.channel.id != after.channel.id
    # Get out
    elif before.channel is not None and after.channel is None and before.channel.id in channels_ids.keys():

      auth_msg_id = channels_ids[before.channel.id]['auth_msg_id']
      txt_channel_id = channels_ids[before.channel.id]['txt_channel_id']
      txt_channel   = client.get_channel(txt_channel_id)
      # Remove reaction from auth message and user from the list
      if user in channels_ids[before.channel.id]['mem_vc_id']:
        channels_ids[before.channel.id]['mem_vc_id'].remove(user)
        channel = client.get_channel(channels_ids[before.channel.id]['auth_channel_id'])
        message = await channel.fetch_message(auth_msg_id)
        user_g  = client.get_user(user)
        await message.remove_reaction("👍", user_g)

      # If this user is in the players list, it takes
      # it off
      if user in channels_ids[before.channel.id]['mem_play_id']:
        channels_ids[before.channel.id]['mem_play_id'].remove(user)
        await ctx.send(f'<@{user}>, você não pode sair do jogo. Vai pagar por isso!😈')

        # If person who left is the victim, it
        # restart round
        try:
          victim = channels_ids[before.channel.id]['victim']
          asker = channels_ids[before.channel.id]['asker']
          if user == victim:
            await txt_channel.send(f'Nossa vítima <@{user}> saiu da sala. Vamos reiniciar a rodada.')
            channels_ids[before.channel.id]['ctrl']   = 0
            channels_ids[before.channel.id]['turn']  -= 1
            channels_ids[before.channel.id]['victim'] = None
            await iniciar(channels_ids[before.channel.id]['master_ctx'])
              
          elif user == asker:
            await txt_channel.send(f'A pessoa que pergunta saiu da sala. Vamos reiniciar a rodada.')
            channels_ids[before.channel.id]['ctrl']   = 0
            channels_ids[before.channel.id]['asker'] = None
            await iniciar(channels_ids[before.channel.id]['master_ctx'])
        except:
          pass
        
# Starts the turn
@client.command()
async def show_list(ctx):
  caller = ctx.author.id
  n_vc_channel_id = returnChannelIdByUserId(ctx.author.id, 'mem_play_id')
  if caller == channels_ids[n_vc_channel_id]['bot_master']:
    # Shows which people are in the game
    string = 'Pessoas participando da brincadeira:\n'
    for id in channels_ids[n_vc_channel_id]['mem_play_id']:
      string += f' - <@{id}>\n'
    await ctx.send(f'{string}')

# Starts the turn
@client.command()
async def iniciar(ctx):
  print('Iniciando a partida...')
  n_vc_channel_id = returnChannelIdByUserId(ctx.author.id, 'mem_play_id')
  caller = ctx.author.id
  if caller == channels_ids[n_vc_channel_id]['bot_master']:
    channels_ids[n_vc_channel_id]['master_ctx'] = ctx
    if channels_ids[n_vc_channel_id]['ctrl'] == 0:
      if len(channels_ids[n_vc_channel_id]['mem_play_id']) > 1:
        turn = channels_ids[n_vc_channel_id]['turn']
        asker = channels_ids[n_vc_channel_id]['mem_play_id'][turn]
        channels_ids[n_vc_channel_id]['asker'] = asker
        # Every new game goes to the next player;
        # if the next player is the last one, it goes
        # to the first one
        if turn < len(channels_ids[n_vc_channel_id]['mem_play_id'])-1:
          channels_ids[n_vc_channel_id]['turn'] += 1
        else:
          channels_ids[n_vc_channel_id]['turn'] = 0

        # Shows which people are in the game
        string = 'Pessoas participando da brincadeira:\n'
        for id in channels_ids[n_vc_channel_id]['mem_play_id']:
          string += f' - <@{id}>\n'
        string += f'\n<@{asker}> gire a garrafa.'
        await ctx.send(f'{string}')
        channels_ids[n_vc_channel_id]['ctrl'] += 1
      else:
        await ctx.send(f'A partida não pode começar com menos de 2 jogadores.')      
    else:
      await ctx.send(f'<@{caller}>, você não pode iniciar um novo jogo nesse momento.')
  else:
      await ctx.send(f'<@{caller}>, você não pode iniciar um novo jogo.')
    
# Iniciar aliases ########################
@client.command()
async def inicia(ctx):
  await iniciar(ctx)

@client.command()
async def começa(ctx):
  await iniciar(ctx)

@client.command()
async def comeca(ctx):
  await iniciar(ctx)

@client.command()
async def play(ctx):
  await iniciar(ctx)
##########################################

@client.command()
async def girar(ctx):
  n_vc_channel_id = returnChannelIdByUserId(ctx.author.id, 'mem_play_id')
  caller = ctx.author.id
  if caller in channels_ids[n_vc_channel_id]['mem_play_id']:
    if channels_ids[n_vc_channel_id]['ctrl'] == 1:
      # The person who called this command hasn't to
      # be the asker
      asker = channels_ids[n_vc_channel_id]['asker']
      if caller == asker:
        channels_ids[n_vc_channel_id]['g'] = False
        # Raffles a person different to the arker to be
        # the victim
        while not channels_ids[n_vc_channel_id]['g']:
          index = randint(0, len(channels_ids[n_vc_channel_id]['mem_play_id']) - 1)
          if channels_ids[n_vc_channel_id]['mem_play_id'][index] != asker:
            channels_ids[n_vc_channel_id]['victim'] = channels_ids[n_vc_channel_id]['mem_play_id'][index]
            victim = channels_ids[n_vc_channel_id]['victim']
            channels_ids[n_vc_channel_id]['g'] = True

        # Show the bottle spining
        index = randint(0, len(channels_ids[n_vc_channel_id]['mem_play_id']) - 1)
        message = await ctx.send(f"Girando a garrafa: <@{channels_ids[n_vc_channel_id]['mem_play_id'][index]}>")
        for i in range(10):
          index = randint(0, len(channels_ids[n_vc_channel_id]['mem_play_id']) - 1)
          await message.edit(content=f"Girando a garrafa: <@{channels_ids[n_vc_channel_id]['mem_play_id'][index]}>")
        await message.edit(content=f"Girando a garrafa: <@{victim}>")
        await message.delete()

        await ctx.send(f'<@{caller}> pergunta para <@{victim}>. Verdade ou consequência?')
        channels_ids[n_vc_channel_id]['ctrl'] += 1
      else:
        await ctx.send(f'<@{caller}>, não é sua vez de rodar.')
    else:
        await ctx.send(f'<@{caller}>, você não pode girar a garrafa nesse momento.')

# Iniciar aliases ########################
@client.command()
async def gira(ctx):
  await girar(ctx)

@client.command()
async def rodar(ctx):
  await girar(ctx)

@client.command()
async def roda(ctx):
  await girar(ctx)

@client.command()
async def spin(ctx):
  await girar(ctx)
##########################################

# Command to choose if it's verdade or consequencia
@client.command()
async def op(ctx, op):
  # global channels_ids, ctrl
  n_vc_channel_id = returnChannelIdByUserId(ctx.author.id, 'mem_play_id')
  op = op.lower()
  caller = ctx.author.id
  if caller in channels_ids[n_vc_channel_id]['mem_play_id']:
    if channels_ids[n_vc_channel_id]['ctrl'] == 2:
      caller = ctx.author.id
      victim = channels_ids[n_vc_channel_id]['victim']
      asker = channels_ids[n_vc_channel_id]['asker']
      if caller == victim:
        if op == 'v':
          try:
            channels_ids[n_vc_channel_id]['truth'][caller] += 1
          except:
            channels_ids[n_vc_channel_id]['truth'][caller] = 1
          if channels_ids[n_vc_channel_id]['truth'][caller] < 4:
            await ctx.send(f'<@{asker}>, faça sua pergunta.')
            asker = channels_ids[n_vc_channel_id]['switch'] = 'verdade'
            channels_ids[n_vc_channel_id]['ctrl'] += 1
          else:
            await ctx.send(f'<@{caller}> você escolheu 3 vezes verdade. Escolha consequência.')
        elif op == 'c':
          await ctx.send(f'<@{asker}>, faça seu desafio.')
          asker = channels_ids[n_vc_channel_id]['switch'] = 'consequencia'
          channels_ids[n_vc_channel_id]['ctrl'] += 1
          try:
            if channels_ids[n_vc_channel_id]['truth'][caller] > 3 :
              channels_ids[n_vc_channel_id]['truth'][caller] = 0
          except:
            pass
        else:
          await ctx.send(f'<@{victim}>, você escolheu uma opção incorreta.')
      else:
        await ctx.send(f'<@{caller}>, não é sua vez de escolher.')
    else:
      await ctx.send(f'<@{caller}>, você não pode escolher uma opção agora.')
# op aliases ########################
@client.command()
async def option(ctx, opt):
  await op(ctx, opt)

@client.command()
async def opção(ctx, opt):
  await op(ctx, opt)

@client.command()
async def opcao(ctx, opt):
  await op(ctx, opt)
####################################

# Command to be used when asker doesn't know what to ask
@client.command()
async def ajuda(ctx):
  global qtn_df, h_qtn_df
  n_vc_channel_id = returnChannelIdByUserId(ctx.author.id, 'mem_play_id')
  caller = ctx.author.id
  if caller in channels_ids[n_vc_channel_id]['mem_play_id']:
    if channels_ids[n_vc_channel_id]['ctrl'] == 3:
      asker = channels_ids[n_vc_channel_id]['asker']
      if asker == caller:
        df_index = randint(0, h_qtn_df - 1)

        # Looking for a not nan question or challenge
        while str(qtn_df.loc[df_index, channels_ids[n_vc_channel_id]['switch']]).lower() == 'nan':
          df_index = randint(0, h_qtn_df - 1)

        await ctx.send(f'{qtn_df.loc[df_index, channels_ids[n_vc_channel_id]["switch"]]}')
      else:
        await ctx.send(f'<@{caller}>, você não pode pedir ajuda agora.')
    else:
      await ctx.send(f'<@{caller}>, você não pode pedir ajuda agora.')
# ajuda aliases ########################
@client.command()
async def ajd(ctx):
  await ajuda(ctx)

@client.command()
async def help(ctx):
  await ajuda(ctx)
########################################

# Command to be used when the challenge or the answer is done
@client.command()
async def feito(ctx):
  n_vc_channel_id = returnChannelIdByUserId(ctx.author.id, 'mem_play_id')
  caller = ctx.author.id
  if caller in channels_ids[n_vc_channel_id]['mem_play_id']:
    if channels_ids[n_vc_channel_id]['ctrl'] == 3:
      victim = channels_ids[n_vc_channel_id]['victim']
      if caller == victim:
        # Starts the vote to see if people believe in the victim
        message = await ctx.send("Vocês acreditam nessa pessoa?")
        await message.add_reaction("👍")
        await message.add_reaction("👎")
        channels_ids[n_vc_channel_id]['vote_msg_id'] = message.id

        # Wait 10 seconds to finish the vote
        reactions_count = ["0️⃣", "1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣", "6️⃣", "7️⃣", "8️⃣", "9️⃣", "🔟"]
        for i in range(len(reactions_count)-1, -1, -1):
          await message.add_reaction(reactions_count[i])
          # if all the players already voted, stop votes 
          if len(channels_ids[n_vc_channel_id]['votes']) == len(channels_ids[n_vc_channel_id]['mem_play_id']) - 1:
            try:
              await message.clear_reaction(reactions_count[i])
              break
            except:
              await message.clear_reaction(reactions_count[i])
              break
          sleep(1)
          await message.clear_reaction(reactions_count[i])

        updated_message = await ctx.channel.fetch_message(message.id)

        positive = negative = 0 
        # Counts the votes
        for r in updated_message.reactions:
            if str(r) == "👍":
                positive = r.count
            elif str(r) == "👎":
                negative = r.count

        # Verifies results
        if positive > negative:
              await ctx.send(f'<@{victim}>, as pessoas acreditaram em você.\nMuito bem! Ganhou uma estrelinha.⭐')
        elif negative > positive:
              await ctx.send(f'<@{victim}>, as pessoas não acreditaram em você.\nVocê vai pagar por isso!😈')
        else:
              await ctx.send(f'<@{victim}>, as pessoas ficaram na Dúvida.\nVocê falhou.')
        channels_ids[n_vc_channel_id]['ctrl'] = 0
        channels_ids[n_vc_channel_id]['votes'] = []
        # Starts a new round after 1s
        sleep(1)
        await iniciar(channels_ids[n_vc_channel_id]['master_ctx'])
      else:
        await ctx.send(f'<@{caller}>, você não pode responder agora.')
    else:
      await ctx.send(f'<@{caller}>, você não pode responder agora.')
# feito aliases ########################
@client.command()
async def done(ctx):
  await feito(ctx)
########################################

# Restarts the game
@client.command()
async def reload(ctx):
  await ctx.message.delete()
  caller = ctx.author.id
  n_vc_channel_id = returnChannelIdByUserId(ctx.author.id, 'mem_play_id')
  if caller == channels_ids[n_vc_channel_id]['bot_master']:
    channels_ids[n_vc_channel_id]['ctrl']  , channels_ids[n_vc_channel_id]['turn']  = 0, 0
    channels_ids[n_vc_channel_id]['victim'], channels_ids[n_vc_channel_id]['asker'] = None, None
    message = await ctx.send("Reloading")
    for j in range(3):
      for i in range(3):
        await message.edit(content='Reloading' + '. ' * (i + 1))
        sleep(.2)
    await message.edit(content="Done!")
    sleep(.2)
    await message.delete()

@client.command()
async def proximo(ctx):
  caller = ctx.author.id
  n_vc_channel_id = returnChannelIdByUserId(ctx.author.id, 'mem_play_id')
  if caller == channels_ids[n_vc_channel_id]['bot_master'] and channels_ids[n_vc_channel_id]['ctrl'] > 0:
    await ctx.send('Pulando para o próximo participante...')
    channels_ids[n_vc_channel_id]['ctrl'] = 0
    await iniciar(channels_ids[n_vc_channel_id]['master_ctx'])
      
# proximo aliases ########################
@client.command()
async def next(ctx):
  await proximo(ctx)
########################################

@client.command()
async def info(ctx):
  caller = ctx.author.id
  n_vc_channel_id = returnChannelIdByUserId(ctx.author.id, 'mem_play_id')
  if caller == channels_ids[n_vc_channel_id]['bot_master']:
    for channel_id, channel_info in channels_ids.items():
      print(f'Channel_id : {channel_id}')
      for channel_info_key, channel_info_value in channel_info.items():
        print(f'\t{channel_info_key:.<30} : {channel_info_value}')
      print('-'*70)

@client.command()
async def exitPlayer(ctx, player, op = '3'):
  caller = ctx.author.id
  n_vc_channel_id = returnChannelIdByUserId(ctx.author.id, 'mem_vc_id')
  def option1():
    if int(player) in channels_ids[n_vc_channel_id]['mem_play_id']:
        channels_ids[n_vc_channel_id]['mem_play_id'].remove(int(player))

  def option2():
    if int(player) in channels_ids[n_vc_channel_id]['mem_vc_id']:
        channels_ids[n_vc_channel_id]['mem_vc_id'].remove(int(player))

  def option3():
    option1()
    option2()

  if caller == channels_ids[n_vc_channel_id]['bot_master']:
    options = [option1, option2, option3]
    for pos, option in enumerate(options):
      if op == str(pos + 1):
        option()
        break
      

@client.command()
async def setBotMaster(ctx, voice_channel, new_master):
  user = ctx.author.id
  voice_channel = int(voice_channel)
  if voice_channel in channels_ids.keys():
    if user == channels_ids[voice_channel]['bot_master']:
      channels_ids[voice_channel]['bot_master'] = int(new_master)
      dm_user = client.get_user(int(new_master))
      await dm_user.send(f'<@{new_master}> agora é o novo Master do canal <#{voice_channel}>.')
    else:
      dm_user = client.get_user(int(user))
      await dm_user.send(f'<@{user}>, você não é o Master do canal <#{voice_channel}>.')

# Just the game rules
@client.command()
async def regras(ctx):
  n_vc_channel_id = returnChannelIdByUserId(ctx.author.id, 'mem_play_id')
  rules = 'Olá! Vamos brincar de uma brincadeira bem divertida? 😈\n'
  rules += 'Prefixo: `??`'
  rules += 'Comandos:\n\n'
  rules += f'` {"iniciar | comeca | começa | play ":>35}` - Inicia uma nova partida. Não é possível iniciar enquanto uma outra estiver acontecendo.\n'
  rules += f'` {"girar | gira | rodar | roda ":>35}` - Sorteia quem irá desafiar quem.\n'
  rules += f'` {"op | opcao | opção | option ":>35}` - Escolhe qual das opções a vítima quer. Use `v` ou `c` para escolher.\n'
  rules += f'` {"ajuda | ajd | help ":>35}` - Não sabe o que perguntar? Use esse comando que Calux vai te ajudar.\n'
  rules += f'` {"feito | done ":>35}` - A vítima deve usar esse comando quando tiver respondido ou cumprido seu desafio\n'
  rules += f'` {"regras | regra | rule | rules ":>35}` - Mostra os como jogar e os comandos do bot.\n\n'
  rules += 'Lembrando que os desafios podem ser provados com uma fotinha, um vídeo curto ou mostrando na call. As pessoas decidirão se acreditam ou não.\n\n'
  rules += 'Vamos começar! 😈'
  caller = ctx.author.id
  if caller in channels_ids[n_vc_channel_id]['mem_play_id']:
    await ctx.send(f'{rules}')

# regras aliases ########################
@client.command()
async def regra(ctx):
  await regras(ctx)

@client.command()
async def rules(ctx):
  await regras(ctx)

@client.command()
async def rule(ctx):
  await regras(ctx)
########################################


@client.command()
async def add_message(ctx):
  await ctx.message.delete()
  caller = ctx.author.id
  print('Enviando imagem...')
  n_vc_channel_id = returnChannelIdByBotMaterId(ctx.author.id, 'bot_master')
  if caller == channels_ids[n_vc_channel_id]['bot_master']:
    with open('src/calax_banner.png', 'rb') as f:
      picture = discord.File(f)

    message = await ctx.send(file=picture)
    await message.add_reaction("👍")  


client.run(bot_token)

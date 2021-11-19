global channels_ids

bot_token = ''
auth_channel_id = 
auth_msg_id = 

# Each key is a voice channel id and the values are informations about the channel
channels_ids = {
                # First voice channel
                 :
                  {
                  # Persons who are playing in the channel
                  'mem_play_id' : [], 
                  # Persons who are in the voice channel
                  'mem_vc_id' : [],
                  # Persons who just voted
                  'votes' : [],
                  'txt_channel_id' : ,
                  'vote_msg_id' : None,
                  'auth_channel_id' : auth_channel_id,
                  'auth_msg_id' : auth_msg_id,
                  'last_ctx' : None,
                  # Context of the First iniciar()
                  'master_ctx' : None,
                  'bot_master' : ,
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

TXT_CHANNELS_IDS = []
for channel in channels_ids.values():
    TXT_CHANNELS_IDS.append(channel['txt_channel_id'])
<<<<<<< HEAD
TXT_CHANNELS_IDS.append(auth_channel_id)
=======
TXT_CHANNELS_IDS.append(auth_channel_id)
>>>>>>> b1cfe4d7f0a84176d9642e2ac0a746e9d4fec209

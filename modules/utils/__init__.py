from .. import credentials as crdt

global channels_ids
channels_ids = crdt.channels_ids

def returnChannelIdByBotMaterId(user_id, where):
  for key in channels_ids.keys():
    if user_id == channels_ids[key][where]:
      return key

  return False



def returnChannelIdByUserId(user_id, where):
  for key in channels_ids.keys():
    if user_id in channels_ids[key][where]:
      return key

  return False



def returnChannelIdByAuthChannel(auth_channel_id):
  for key in channels_ids.keys():
    if auth_channel_id == channels_ids[key]['auth_channel_id']:
      return key

  return False



def returnChannelIdByTextChannel(txt_channel_id):
  for key in channels_ids.keys():
    if txt_channel_id == channels_ids[key]['txt_channel_id']:
      return key

  return False
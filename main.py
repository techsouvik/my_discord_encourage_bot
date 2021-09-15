import os
import discord
import requests as req
import json
import random 
from replit import db
from keep_alive import keep_alive

client = discord.Client()

sad_words = ['sad', 'depressed', 'unhappy', 'angry', 'miserable', 'depressing']

starter_encouragements = [
  "Cheer up !",
  "Hang in there.",
  "You are a great person /bot !"
]

if "responding" not in db.keys():
  db["responding"] = True

def get_quote():
  res = req.get("https://zenquotes.io/api/random")
  json_data = json.loads(res.text)
  quote = json_data[0]['q'] + "  -" + json_data[0]['a']
  return (quote)

def update_encouragements(encouraging_message):
  if "encouragements" in db.keys():
    encouragements = db["encouragements"]
    encouragements.append(encouraging_message)
    db["encouragemnts"] = encouragements
  else:
    db["encouragements"] = [encouraging_message]
     
def delete_encouragement(index):
  encouragements = db["encouragements"]
  if len(encouragements) > index:
    del encouragements[index]
    db["encouragements"] = encouragements

@client.event
async def on_ready():
  print('We have logged on {0.user}'.format(client))

@client.event
async def on_message(message):
  if(message.author == client.user):
    return
  
  msg = message.content

  if message.content.startswith('$hello'):
    await message.channel.send('Hello !')

  if message.content.startswith('$inspire'):
    quote = get_quote()
    await message.channel.send(quote)

  if db["responding"]:
    options = starter_encouragements
    if "encouragements" in db.keys():
      options.extend(db["encouragements"])
    if any(word in msg for word in sad_words):
      await message.channel.send(random.choice(options))
  
  if msg.startswith("$new"):
    encouraging_message = msg.split("$new ",1)[1]
    update_encouragements(encouraging_message)
    await message.channel.send("New Encouraging message added.")

  if msg.startswith("$del"):
    encouragemnts = []
    if "encouragements" in db.keys():
      index = int(msg.split("$del",1)[1])
      delete_encouragement(index)
      encouragements = db["encouragements"]
    await message.channel.send(encouragements)
  
  if msg.startswith("$list"):
    encouragements = []
    if "encouragements" in db.keys():
      encouragements = db["encouragements"]
    await message.channel.send(encouragements)
  
  if msg.startswith("$responding"):
    value = msg.split("$responding ",1)[1]
    if value.lower() == "true":
      db["responding"] = True
      await message.channel.send("Responding is ON.....")
    else:
      db["responding"] = False
      await message.channel.send("Responding is OFF.....")

keep_alive()

my_secret = os.environ['TOKEN']
client.run(my_secret) 

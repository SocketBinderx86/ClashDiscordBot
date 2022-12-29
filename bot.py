import discord
import clash
import random
import json
from threading import Thread


async def send_message(channel, message):
    try:
        await channel.send(message)
    except Exception as e:
        print(f'error: {e}')

def valid_channel(discord_channel) -> bool:
    channel = str(discord_channel)
    direct_message = channel.find('Direct Message')
    if channel != 'admin-bot-area' and channel != 'bottesting' and channel != 'bot-commands' and direct_message == -1:
        return False
    return True

async def handle_message(message, user_message, guild):
    p_message = user_message.lower()
    direct_message = str(message.channel).find('Direct Message')

    if not valid_channel(message.channel):
        return

    if "!verify" in p_message:
        if direct_message == -1:
            await message.author.send(content="Please message this bot directly to verify your account, posting your api token in public threads is not advised. I deleted your" +
            " post for you to avoid any privacy concerns. If this wasn't suppose to happen, please message your server admin. Here is the post in question:\n\n" + user_message)
            await message.delete()
            return
        parse = p_message.split()
        while("" in parse):
            parse.remove("")
        if len(parse) == 3 and parse[0] == "!verify":
            results = await clash.verify(parse[1], parse[2], str(message.author))
            if results[0]:
                v_role_id = 1057767884161556610
                role = guild.get_role(v_role_id)
                member = guild.get_member_named(str(message.author))
                if role is None or member is None:
                    await send_message(message.channel, "critical error please message admin")
                    return
                await member.add_roles(role)
                await send_message(channel=message.channel, message="Success, please ensure that you now have the 'Verified' role, if not, contact server admin")
            else:
                await send_message(channel=message.channel, message=results[1])
                    


    if p_message == '!list members':
         await send_message(channel=message.channel, message=clash.get_member_list())

    if p_message == 'roll':
        await send_message(channel=message.channel, message=str(random.randint(1,10)))
        
    if p_message == '!help':
        await send_message(channel=message.channel, message="`This is a temp help message`")

def run_discord_bot():
    file = open('tokens.json')
    tokens = json.load(file)

    print(tokens['clash_token'] + "\n\n")
    print(tokens['discord_token'])
    # TOKEN = 
    intents = discord.Intents.all()
    intents.message_content = True
    client = discord.Client(intents=intents)

    @client.event
    async def on_ready():
        print(f'{client.user} is now running!')

    @client.event
    async def on_message(message):
        if message.author == client.user:
            return
        username = str(message.author)
        user_message = str(message.content)
        channel = str(message.channel)
        guild_id = 945714787810156634
        guild = client.get_guild(guild_id)
        print(f"{username} said: '{user_message}' ({channel})")
        await handle_message(message=message, user_message=user_message, guild=guild)

    client.run(TOKEN)
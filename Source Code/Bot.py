import discord
import mysql.connector
from mysql.connector import Error
import asyncio

client = discord.Client()

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    commands = {
        '.iam': SetTeam,
        '.trivia': Trivia
    }

    if not message.author == client.user:
        for k, v in commands.items():
            if message.content.lower().startswith(k):
                await commands[k](message)

@client.event
async def SetTeam(message):
    team_list = ["Mystic", "Instinct", "Valor"]
    entered_team = message.content[5:]
    role = discord.utils.get(message.guild.roles, name=entered_team)
    roles = [
        718316185598296126,
        718317541943935016,
        718317616439230466
    ]
    for r in message.author.roles:
        if r.id in roles:
            await message.channel.send("You already have a team. Please PM admin if you wish to change your current team")
            return
    if role is None or role.name not in team_list:
        await message.channel.send("Invalid team name. Please choose one of: Mystic, Instinct, Valor")
    elif role in message.author.roles:
        await message.channel.send("You're already in " + entered_team)
    else:
        try:
            await message.author.add_roles(role)
            await message.channel.send("Added to {0}".format(role.name))
        except discord.Forbidden:
            await message.channel.send("Unable to set team. Please PM admin")

@client.event
async def Trivia(message):
    bot_msg = await message.channel.send("```Please pick a category\n"
                                         "A. Animal\n"
                                         "B. Country```")
    await bot_msg.add_reaction('\U0001f1e6')
    await bot_msg.add_reaction('\U0001f1e7')

    def check_user_react(reaction, user):
        return user == message.author and str(reaction.emoji)

    try:
        reaction, user = await client.wait_for('reaction_add', timeout=30.0, check=check_user_react)
    except asyncio.TimeoutError:
        await message.channel.send("Cancel trivia")
    else:
        #Connect to Database
        try:
            connection = mysql.connector.connect(host='localhost',
                                                 database='triviadb',
                                                 user='root',
                                                 password='Conga1234!@')
            if connection.is_connected():
                if str(reaction) == "🇦":
                    await message.channel.send("You picked Animal")
                elif str(reaction) == '🇧':
                    await message.channel.send("You picked Country")
        except Error as e:
            print("Error while connecting to database", e)
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

if __name__ == '__main__':
    client.run('NzYxNzM0ODEwMTUwMjQwMjk2.X3e60w.n2aQrRbDq-wFF9RGl6KQiE-2lF0')

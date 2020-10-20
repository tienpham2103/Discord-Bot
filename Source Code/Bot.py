import discord
import mysql.connector
from mysql.connector import Error
import asyncio
from discord.ext import commands
import random

#client = discord.Client()
bot = commands.Bot(command_prefix='.')
bot.__running = False
bot.__question_list_id = []

@bot.command()
async def iam(ctx, arg):
    team_list = ["Mystic", "Instinct", "Valor"]
    role = discord.utils.get(ctx.guild.roles, name=arg)
    roles = [
        718316185598296126,
        718317541943935016,
        718317616439230466
    ]
    for r in ctx.author.roles:
        if r.id in roles:
            await ctx.send("You already have a team. Please PM admin if you wish to change your current team")
            return
    if role is None or role.name not in team_list:
        await ctx.send("Invalid team name. Please choose one of: Mystic, Instinct, Valor")
    elif role in ctx.author.roles:
        await ctx.send("You're already in " + entered_team)
    else:
        try:
            await ctx.author.add_roles(role)
            await ctx.send("Added to {0}".format(role.name))
        except discord.Forbidden:
            await ctx.send("Unable to set team. Please PM admin")

@bot.command()
async def trivia(ctx):
    bot_msg = await ctx.send("```Please pick a category\n"
                                         "A. Animal\n"
                                         "B. Country```")
    await bot_msg.add_reaction('\U0001f1e6')
    await bot_msg.add_reaction('\U0001f1e7')

    def check_user_react(reaction, user):
        return user == ctx.author and str(reaction.emoji)

    try:
        reaction, user = await bot.wait_for('reaction_add', timeout=30.0, check=check_user_react)
    except asyncio.TimeoutError:
        await ctx.send("Cancel trivia")
    else:
        bot.__question_list_id = [iter+1 for iter in range(12)]
        bot.__running = True
        if str(reaction) == "🇦":
            if bot.__running:
                await ctx.send('```You picked Animal, Quiz starts in 5 seconds```')
                await asyncio.sleep(5)
                await ctx.invoke(bot.get_command('AskQuestion'), query='animal_vietnamese')
        elif str(reaction) == '🇧':
            await ctx.send("You picked Country")

@bot.command()
async def AskQuestion(ctx, *, query: str):
    if bot.__running:
        await bot.send("")
        question_id = random.randint(1, len(bot.__question_list_id))
        connection = mysql.connector.connect(host='us-cdbr-east-02.cleardb.com',
                                             database='heroku_adf1e70662c9fe5',
                                             user='bb997b5cf47a4c',
                                             password='50cafacf')
        sql_select_question_query = "select question, answer_a, answer_b, answer_c, answer_d, correct_answer from " \
                                    + query + " where question_id = " + str(question_id)

        cursor = connection.cursor()
        cursor.execute(sql_select_question_query)
        records = cursor.fetchall()

        question_string = str(records[0][0])
        answer_a_string = str(records[0][1])
        answer_b_string = str(records[0][2])
        answer_c_string = str(records[0][3])
        answer_d_string = str(records[0][4])
        correct_answer_string = str(records[0][5])

        bot_question_string = "```" + question_string \
                              + ":\nA. " + answer_a_string \
                              + "\nB. " + answer_b_string \
                              + "\nC. " + answer_c_string \
                              + "\nD. " + answer_d_string + "```"
        bot_question_msg = await ctx.send(bot_question_string)

        await bot_question_msg.add_reaction('\U0001f1e6')
        await bot_question_msg.add_reaction('\U0001f1e7')
        await bot_question_msg.add_reaction('\U0001f1e8')
        await bot_question_msg.add_reaction('\U0001f1e9')

        await asyncio.sleep(7)

        await ctx.invoke(bot.get_command('ShowAnswer'), query=correct_answer_string)

        if (connection.is_connected()):
            cursor.close()
            connection.close()

        await ctx.invoke(bot.get_command('NextQuestion'), query=query)

@bot.command()
async def ShowAnswer(ctx, *, query: str):
    prompt = 'Correct answer is ' + query.upper()
    await ctx.send(prompt)
    await ctx.invoke(bot.get_command('ShowScoreBoard'))

@bot.command()
async def NextQuestion(ctx, *, query: str):
    if bot.__running:
        await ctx.invoke(bot.get_command('AskQuestion'), query=query)

@bot.command()
async def ShowScoreBoard(ctx):

    await ctx.send('Score Board')

@bot.command()
async def end(ctx):
    if bot.__running:
        bot.__running = False
        await ctx.send('Quiz ended')
        await ctx.invoke(bot.get_command('ShowScoreBoard'))


if __name__ == '__main__':
    client.run('Your-Token-Here')

import discord

client = discord.Client()

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith(".iam "):
        team_list = ["Mystic", "Instinct", "Valor"]
        entered_team = message.content[5:]
        #await message.channel.send("Your team is: " + enetered_team)
        role = discord.utils.get(message.guild.roles, name=entered_team)
        roles = [
            718316185598296126,
            718317541943935016,
            718317616439230466
        ]
        for r in message.author.roles:
            if r.id in roles:
                await message.channel.send("Bạn đã có team, vui lòng inbox admin nếu muốn chuyển team")
                return
        if role is None or role.name not in team_list:
            await message.channel.send("Team không tồn tại. Vui lòng chọn 1 trong 3 team: Mystic, Instinct, Valor")
        elif role in message.author.roles:
            await message.channel.send("Bạn đã ở team " + entered_team)
        else:
            try:
                await message.author.add_roles(role)
                await message.channel.send("Đã thêm vào team {0}".format(role.name))
            except discord.Forbidden:
                await message.channel.send("Không thể chia team. Vui lòng inbox admin")

client.run('Your Token Here')

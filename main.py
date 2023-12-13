# This example requires the 'members' and 'message_content' privileged intents to function.

import disnake
from disnake.ext import commands
from disnake.utils import get

import io
import aiohttp

from aiohttp import ClientSession

import random

import json

from datetime import date

from operator import itemgetter

import pprint

import api2ch

intents = disnake.Intents.default()
intents.members = True
intents.message_content = True

# command_sync_flags = commands.CommandSyncFlags.all()
# command_sync_flags.sync_commands_debug = True
# command_sync_flags.sync_commands = True
#command_sync_flags.allow_command_deletion = True

command_sync_flags = commands.CommandSyncFlags.default()
command_sync_flags.sync_commands_debug = True

bot = commands.Bot(command_prefix='?', command_sync_flags=command_sync_flags, intents=disnake.Intents.all(), activity= disnake.Streaming(name="Battle for Sorteer", url="https://no-synchro-swim.nethouse.ru"))



#events
@bot.event
async def on_ready():
    print(f"{bot.user} has pokaked!")
    print("-----")

@bot.event
async def on_message(ctx):
    if ctx.channel.type == disnake.ChannelType.private:
        user_id = ctx.author.id
        userlistObj = []
        print("message_on")
        print(ctx)

        with open("json_data/dm_user_guilds.json") as ft:
            userlistObj = json.load(ft)

        if user_id in map(itemgetter('user_id'), userlistObj):
            print("user in list")
            for dictionary in userlistObj:
                if dictionary.get('user_id') == user_id:
                    print("user equal")
                    for guild_id in dictionary['guild_ids']:
                        chlistObj = []
                        with open("json_data/dm_channels.json") as fp:
                            chlistObj = json.load(fp)

                            if guild_id in map(itemgetter('guild_id'), chlistObj):
                                for dict in chlistObj:
                                    if dict.get('guild_id') == guild_id:
                                        dict_channel = dict.get('dm_channel_id')
                                        channel = bot.get_channel(dict_channel)

                                        embed = disnake.Embed(
                                            title= "Прослушка " + ctx.author.name,
                                            description= ctx.content,
                                            color=disnake.Colour.yellow(),
                                        )
                                        embed.set_author(
                                            name= ctx.author.name,
                                            url="https://no-synchro-swim.nethouse.ru/",
                                            icon_url= ctx.author.avatar,
                                        )
                                        botter = bot.get_user(1127659374928740362)
                                        embed.set_footer(
                                            text= ctx.id,
                                            icon_url= botter.avatar,
                                        )
                                        embed.set_thumbnail(url=ctx.author.avatar)

                                        sent_message = await channel.send(embed=embed)
                                        files_st = [await f.to_file() for f in ctx.attachments]
                                        if files_st:
                                            await sent_message.reply("", files= files_st)


#cmds

# @bot.command(description="slash cmds sync")
# async def synchro(ctx):
#     if ctx.author.id == 706059736579178536: #owner ID
#         command_sync_flags.sync_global_commands = True
#         commands.CommandSyncFlags.all()
#         print('Commands synced.')
#     else:
#         await ctx.reply('You must be the owner to use this command!')

@bot.slash_command(description="secretly leaves drist message")
async def sping(inter, messageg: str, reply_message: commands.String[str, 19, 19] = "-1", file: commands.String[str, 1, ...] = "-1"):
    await inter.response.send_message("✔",ephemeral=True)
    #await inter.response.is_done
    #disnake.ApplicationCommandInteraction.delete_original_message
    channel = inter.channel

    if file == "-1":
        if reply_message == "-1":
            await channel.send(f"{messageg}")
        else:
            message = await channel.fetch_message(int(reply_message))
            await message.reply(f"{messageg}")
    else:
        async with aiohttp.ClientSession() as session:
            async with session.get(file) as resp:
                if resp.status != 200:
                    return await inter.response.send_message("Could not download file...", ephemeral=True)
                data = io.BytesIO(await resp.read())
                if reply_message == "-1":
                    await channel.send(f"{messageg}", file=disnake.File(data, 'picrelated.png'))
                else:
                    message = await channel.fetch_message(int(reply_message))
                    await message.reply(f"{messageg}", file=disnake.File(data, 'picrelated.png'))




@bot.slash_command(description="Рассчитает ваше сопротивление стабилитрона")
async def stablethrone(inter, u_input: float, u_stable: float, i_supress: float, i_stable: float):
    resistance_stablethrone = (u_input-u_stable)/(i_supress+i_stable)
    await inter.response.send_message(f"Ваше сопротивление стабилитрона = {resistance_stablethrone} Ом")

@bot.slash_command(description="Возвращает значение деда")
async def zeexl(inter):
    owners = [
        891743041071743098, #pricel
        841565162673799188, #beaver
        642771569440981042, #scoden
        706059736579178536 #svineld
    ]
    drister_id = 438714973657497600
    if inter.author.id in owners:
        await inter.response.send_message("✔", ephemeral=True)
        channel = inter.channel
        guild = inter.guild
        await channel.send(f"<@{drister_id}>, нам сообщили, что вы насрали!")
        member = guild.get_member(drister_id) #438714973657497600 = zeexl
        if member:
            await member.edit(roles=[])
    else:
        channel = inter.channel
        if inter.author.id != drister_id:
            await inter.response.send_message("А не слишком-ли мал, такое делать?", ephemeral=True)
        await channel.send(f"Гений, миллиардер, плэйбой, филантроп")

@bot.slash_command(description="Возвращает значение гейства")
async def gay(inter, member: disnake.Member):
    member_id = member.id
    gay_lvl = random.randint(0,100)
    today = str(date.today())
    listObj = []
    with open("json_data/gay.json") as fh:
        listObj = json.load(fh)

    print(listObj)
    print(type(listObj))

    if member_id in map(itemgetter('member_id'), listObj):
        for dictionary in listObj:
            if dictionary.get('member_id') == member_id:
                db_date = dictionary.get('date')
                if db_date == today:
                    gay_lvl_output = dictionary.get('gay_lvl')
                    await inter.response.send_message(f"Уровень гейства участника <@{member_id}> равен {gay_lvl_output}%. Возвращайтесь завтра!")
                else:
                    await inter.response.send_message(f"Уровень гейства участника <@{member_id}> равен {gay_lvl}%")
                    dictionary["gay_lvl"] = gay_lvl
                    dictionary["date"] = today
                    with open("json_data/gay.json", 'w') as json_file:
                        json.dump(listObj, json_file,
                                  indent=4,
                                  separators=(',', ': '))
                break
    else:
        listObj.append({
            "member_id": member_id,
            "gay_lvl": gay_lvl,
            "date": today
        })
        await inter.response.send_message(f"Уровень гейства участника <@{member_id}> равен {gay_lvl}%")
        with open("json_data/gay.json", 'w') as json_file:
            json.dump(listObj, json_file,
                      indent=4,
                      separators=(',', ': '))

@bot.slash_command(description="Устанавливает текстовый канал личной переписки")
async def set_dm_channel(inter):
    guild_id = inter.guild.id
    channel_id = inter.channel.id
    channel = inter.channel
    dmlistObj = []

    await inter.response.send_message("Текущий канал установлен каналом личной переписки")
    #await channel.create_webhook()

    with open("json_data/dm_channels.json") as fp:
        dmlistObj = json.load(fp)

    if guild_id in map(itemgetter('guild_id'), dmlistObj):
        for dictionary in dmlistObj:
            if dictionary.get('guild_id') == guild_id:
                dictionary["dm_channel_id"] = channel_id
                with open("json_data/dm_channels.json", 'w') as json_file:
                    json.dump(dmlistObj, json_file,
                                indent=4,
                                separators=(',', ': '))
            break
    else:
        dmlistObj.append({
            "guild_id": guild_id,
            "dm_channel_id": channel_id
        })

        with open("json_data/dm_channels.json", 'w') as json_file:
            json.dump(dmlistObj, json_file,
                      indent=4,
                      separators=(',', ': '))

@bot.slash_command(description="Добавляет сервер в список рассылки ответа пользователя")
async def add_reply_user(inter, user: disnake.User):
    guild_id = inter.guild.id
    channel_id = inter.channel.id
    user_id = user.id
    dmulistObj = []

    await inter.response.send_message("Теперь ответ пользователя будет приходить и сюда")

    with open("json_data/dm_user_guilds.json") as ft:
        dmulistObj = json.load(ft)

    if user_id in map(itemgetter('user_id'), dmulistObj):
        for dictionary in dmulistObj:
            if dictionary.get('user_id') == user_id:
                if not guild_id in dictionary.get('guild_ids'):
                    guild_ids = dictionary['guild_ids']
                    guild_ids.append(guild_id)
                    dictionary['guild_ids'] = guild_ids
                with open("json_data/dm_user_guilds.json", 'w') as json_file:
                    json.dump(dmulistObj, json_file,
                                indent=4,
                                separators=(',', ': '))
            break
    else:
        guild_ids = [guild_id]
        dmulistObj.append({
            "user_id": user_id,
            "guild_ids": guild_ids
        })

        with open("json_data/dm_user_guilds.json", 'w') as json_file:
            json.dump(dmulistObj, json_file,
                      indent=4,
                      separators=(',', ': '))


@bot.slash_command(description="Отправляет личное сообщение указанному пользователю")
async def dm(inter, text: str, user: disnake.User, reply_message: commands.String[str, 19, 19] = "-1", file: commands.String[str, 1, ...] = "-1"):
    #await user.send(f"{text}")

    guild_id = inter.guild.id
    channel_id = inter.channel.id
    visible = True
    dmlistObj = []

    with open("json_data/dm_channels.json") as fp:
        dmlistObj = json.load(fp)

    if guild_id in map(itemgetter('guild_id'), dmlistObj):
        for dictionary in dmlistObj:
            if dictionary.get('guild_id') == guild_id:
                if dictionary["dm_channel_id"] == channel_id:
                    visible = False

    await inter.response.send_message("✔",ephemeral=visible)

    channel = inter.channel

    if file == "-1":
        if reply_message == "-1":
            await user.send(f"{text}")
        else:
            message = await user.fetch_message(int(reply_message))
            await message.reply(f"{text}")
    else:
        async with aiohttp.ClientSession() as session:
            async with session.get(file) as resp:
                if resp.status != 200:
                    return await inter.response.send_message("Could not download file...", ephemeral=True)
                data = io.BytesIO(await resp.read())
                if reply_message == "-1":
                    await user.send(f"{text}", file=disnake.File(data, 'picrelated.png'))
                else:
                    message = await user.fetch_message(int(reply_message))
                    await message.reply(f"{text}", file=disnake.File(data, 'picrelated.png'))

@bot.slash_command(description="глобально переименовывает участников; 0 = set default, 1 = full, 2 = pref + name, 3 = name + postf")
async def global_rename(inter, name: str, type: commands.Range[int, 0, 3] = 1):
    guild = inter.guild
    members = guild.members
    await inter.response.send_message("✔ Участники сервера успешно переименованы!")
    for member in members:
        if type == 1:
            try:
                await member.edit(nick=name)
            except disnake.errors.Forbidden:
                print("forbidden")
        elif type == 2:
            if member.nick == None:
                m_name = member.global_name
            else:
                m_name = member.nick
            if " " in m_name:
                a_name = name + " " + m_name[m_name.index(" "): ]
                if len(a_name) > 32:
                    a_name = name
            else:
                a_name = name + " " + m_name
                if len(a_name) > 32:
                    a_name = name

            try:
                await member.edit(nick=a_name)
            except disnake.errors.Forbidden:
                print("forbidden")
        elif type == 3:
            if member.nick == None:
                m_name = member.global_name
            else:
                m_name = member.nick
            if " " in m_name:
                a_name = m_name[0:m_name.index(" ", 1)] + " " + name
                if len(a_name) > 32:
                    a_name = name
            else:
                a_name = m_name + " " + name
                if len(a_name) > 32:
                    a_name = name

            try:
                await member.edit(nick=a_name)
            except disnake.errors.Forbidden:
                print("forbidden")
        elif type == 0:
            try:
                n_name = member.global_name
                if member.nick is not None:
                    await member.edit(nick=None)
            except disnake.errors.Forbidden:
                print("forbidden")

@bot.slash_command(description="глобально срет пастой")
async def global_spam(inter, text: str, file: commands.String[str, 1, ...] = "-1"):
    #await user.send(f"{text}")

    guild_id = inter.guild.id
    channel_id = inter.channel.id
    visible = True

    guild = inter.guild
    members = guild.members

    await inter.response.send_message("✔",ephemeral=visible)

    channel = inter.channel

    for user in members:
        try:
            if file == "-1":
                await user.send(f"{text}")
            else:
                async with aiohttp.ClientSession() as session:
                    async with session.get(file) as resp:
                        if resp.status != 200:
                            return await inter.response.send_message("Could not download file...", ephemeral=True)
                        data = io.BytesIO(await resp.read())
                        await user.send(f"{text}", file=disnake.File(data, 'picrelated.png'))
        except disnake.errors.HTTPException:
            print("Насрано! Пользователь обиженка!")
        except Exception as ex_:
            print("насрано " + ex_)

@bot.slash_command(description="хаха минус роль")
async def role_delete(inter, member_id: commands.String[str, 1, ...], role_id: commands.String[str, 1, ...], guild_id: commands.String[str, 1, ...]):
    guildd = bot.get_guild(int(guild_id))
    member = guildd.get_member(int(member_id))
    role = guildd.get_role(int(role_id))
    await member.remove_roles(role)
    await inter.response.send_message("Роль удалена))", ephemeral=True)

@bot.slash_command(description="хаха минус роль")
async def role_delete_mu(inter, member_id: commands.String[str, 1, ...], guild_id: commands.String[str, 1, ...]):
    guildd = bot.get_guild(int(guild_id))
    member = guildd.get_member(int(member_id))
    for role in member.roles:
        await member.remove_roles(role)
    await inter.response.send_message("Роль удалена))", ephemeral=True)

token = "sus"
try:
    with open ("json_data/token.json") as json_file:
        TokenDict = json.load(json_file)
    token = TokenDict["token"]
except FileNotFoundError:
    print("You need to create 'token.json' file in 'json_data' directory! There is a template for you!")
bot.run(token)
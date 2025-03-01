# modules
import discord
import asyncio
import datetime
import time

from discord.errors import *
from discord.ext import commands
from discord.ext.commands import *

intents = discord.Intents(messages=True, members=True, guilds=True)

# var
token = "token"
cid = "client_id"
owner = "anuryx."
oid = "706697300872921088"

# prefix and status setup
bot = commands.Bot(command_prefix='42!', intents=intents)

client = discord.Client()

@client.event
async def on_message(message):
    if message.author == bot.user:
        return
        
# when ready
@bot.event
async def on_ready():
    print(f'\n> {bot.user} HAS CONNECTED TO DISCORD.\n> OWNER:')
    print(f"{owner}")
    print("OWNER\'S ID:")
    print(f"{oid}\n")
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=f"{str(len(bot.guilds))} guilds | 42!help"))
    print(f'[log] Log is loading...')
    print(f'[log] {bot.user} changed its activity.')

@bot.event
async def on_guild_join(guild):
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=f"{str(len(bot.guilds))} guilds | 42!help"))
    print(f'[log] {bot.user} changed its activity.')

@bot.event
async def on_guild_remove(guild):
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=f"{str(len(bot.guilds))} guilds | 42!help"))
    print(f'[log] {bot.user} changed its activity.')
# end of startup

# error handler
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('Missing required argument(s).')
        print(f'[log] {ctx.author} returned an error: {error}.')
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("You dont have the permission to do that. :eyes:")
        print(f'[log] {ctx.author} returned an error: {error}.')
    if isinstance(error, BotMissingPermissions):
        await ctx.send('I don\'t have the required permissions to use this.')
        print(f'[log] {ctx.author} returned an error: {error}.')
    if isinstance(error, BadArgument):
        await ctx.send('Invalid argument')
        print(f'[log] {ctx.author} returned an error: {error}.')
    if isinstance(error, commands.CommandOnCooldown):
        if math.ceil(error.retry_after) < 60:
            await ctx.reply(f'This command is on cooldown. Please try after {math.ceil(error.retry_after)} seconds')
            print(f'[log] {ctx.author} returned an error: {error}.')
        elif math.ceil(error.retry_after) < 3600:
            ret = math.ceil(error.retry_after) / 60
            await ctx.reply(f'This command is on cooldown. Please try after {math.ceil(ret)} minutes')
            print(f'[log] {ctx.author} returned an error: {error}.')
        elif math.ceil(error.retry_after) >= 3600:
            ret = math.ceil(error.retry_after) / 3600
            if ret >= 24:
                r = math.ceil(ret) / 24
                await ctx.reply(f"This command is on cooldown. Please try after {r} days")
                print(f'[log] {ctx.author} returned an error: {error}.')
            else:
                await ctx.reply(f'This command is on cooldown. Please try after {math.ceil(ret)}')
                print(f'[log] {ctx.author} returned an error: {error}.')

# help cmd
bot.remove_command("help")

@bot.command(aliases=['help'])
async def helplist(ctx):
    embed=discord.Embed(title="**help list for Monitor42**", description="my prefix is: `42!`", color=discord.Color.blue())
    embed.add_field(name='moderating:', value="kick, ban, unban, purge, mute, unmute, warn, lock, unlock", inline=False)
    embed.add_field(name='others:', value="invite, ping", inline=False)
    embed.set_footer(text="42: type 42!help to get this list.\n(Information requested by :{})".format(ctx.author))
    await ctx.send(embed=embed)
    print(f'[log] {ctx.author} requested 42!help.')

@bot.command()
@commands.cooldown(1, 1, commands.BucketType.user)
@commands.has_permissions(kick_members=True)
async def kick(ctx, member: discord.Member, *, reason=None):
    await member.kick(reason=reason)
    await ctx.send(f'User {member} has kicked successfully.')
    print(f'[log] {ctx.author} requested 42!kick.')

@bot.command(pass_context=True, aliases=['purge', 'clear'])
@commands.cooldown(1, 1, commands.BucketType.user)
@commands.has_permissions(administrator=True)
async def clean(ctx, limit: int):
    await ctx.channel.purge(limit=limit)
    print(f'[log] {ctx.author} requested 42!purge.')
    await ctx.send('Cleared by {}'.format(ctx.author.mention))
    await ctx.message.delete()
@clean.error
async def clear_error(ctx,error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("You can not do that!")
        print(f'[log] {ctx.author} returned an error: {error}.')

@bot.command(aliases=['shutup'])
@commands.cooldown(1, 1, commands.BucketType.user)
@commands.has_permissions(manage_messages=True)
async def mute(ctx, member: discord.Member, *, reason=None):
    guild = ctx.guild
    mutedRole = discord.utils.get(guild.roles, name="Muted")

    if not mutedRole:
        mutedRole = await guild.create_role(name="Muted")

        for channel in guild.channels:
            await channel.set_permissions(mutedRole, speak=False, send_messages=False, read_message_history=True, read_messages=False)
    embed = discord.Embed(title="muted", description=f"{member.mention} was muted successfully.", colour=discord.Colour.light_gray())
    embed.add_field(name="reason:", value=reason, inline=False)
    await ctx.send(embed=embed)
    print(f'[log] {ctx.author} requested 42!mute.')
    await member.add_roles(mutedRole, reason=reason)
    await member.send(f" you have been muted from: {guild.name}\n reason: {reason}")
    print(f'[log] {ctx.author} \'s DM has successfully sent.')

@bot.command()
@commands.cooldown(1, 1, commands.BucketType.user)
@commands.has_permissions(manage_messages=True)
async def unmute(ctx, member: discord.Member):
   mutedRole = discord.utils.get(ctx.guild.roles, name="Muted")

   await member.remove_roles(mutedRole)
   await member.send(f" you have unmuted from: - {ctx.guild.name}")
   print(f'[log] {ctx.author} \'s DM has successfully sent.')
   embed = discord.Embed(title="unmute", description=f" unmuted-{member.mention}",colour=discord.Colour.light_gray())
   await ctx.send(embed=embed)
   print(f'[log] {ctx.author} requested 42!unmute.')

@bot.command()
@commands.cooldown(1, 1, commands.BucketType.user)
@commands.has_permissions(ban_members = True)
async def ban(ctx, member : discord.Member, *, reason = None):
    await member.ban(reason = reason)
    await ctx.send(f'User {member} has been banned successfully.')
    print(f'[log] {ctx.author} requested 42!ban.')

@bot.command()
@commands.cooldown(1, 1, commands.BucketType.user)
async def unban(ctx, id: int):
    user = await bot.fetch_user(id)
    await ctx.guild.unban(user)
    print(f'[log] {ctx.author} requested 42!unban.')

@bot.command()
async def invite(ctx):
	await ctx.reply('invite me to moderate your servers!\nhttps://discord.com/oauth2/authorize?client_id=733589280437436478&permissions=8&scope=bot', mention_author=False)
	print(f'[log] {ctx.author} requested 42!invite.')

@bot.command()
@commands.cooldown(1, 5, commands.BucketType.user)
async def ping(ctx):
    await ctx.send(f'Client Latency: {round(bot.latency * 1000)}ms')
    print(f'[log] {ctx.author} requested 42!ping.')

# start
bot.run(token)

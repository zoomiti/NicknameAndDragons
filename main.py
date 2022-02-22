import discord
from discord.ext import tasks, commands
from discord.ext.commands import has_permissions, MissingPermissions
from discord import Forbidden
import os
import traceback

uptime=0
client = discord.Client()
bot = commands.Bot(command_prefix='$')

@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="for $"), afk=True)
    global uptime
    uptime = -1
    update_nicks.start()

@bot.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$hello'):
        await message.channel.send('Hello world!')
        await message.author.edit(nick='Mr. Poopy Buttface')

    await bot.process_commands(message)

@bot.command(name="nick", pass_context=True)
@has_permissions(manage_nicknames=True)
async def _nick(ctx, nickname:str):
    print("Changing %s to %s" % (ctx.message.author.display_name, nickname))
    try:
        await ctx.message.author.edit(nick=nickname);
    except MissingPermissions as exc:
        ctx.send('{}'.format(exc.missing_perms))
    except Forbidden as err:
        print ('{}'.format(err.text))

@tasks.loop(hours=1)
async def update_nicks():
    global uptime
    uptime = uptime+1
    print('%i hours of uptime' % uptime)


#@_nick.error
#async def nick_error(ctx, error):
#    if isinstance(error, MissingPermissions):
#        text = "Sorry {}, you do not have permission to do that!".format(ctx.message.author)
#        await bot.send_message(ctx.message.channel, text)

@bot.command()
async def ping(ctx):
    '''Pong! Get the bot's response time'''
    em = discord.Embed(color=discord.Color.green())
    em.title = "Pong!"
    em.description = f'{bot.latency * 1000} ms'
    print("Ping = {}".format(em.description))
    await ctx.send(embed=em)

async def send_cmd_help(ctx):
    cmd = ctx.command
    em = discord.Embed(title=f'Usage: {ctx.prefix + cmd.signature}')
    em.color = discord.Color.green()
    em.description = cmd.help
    return em

@bot.event
async def on_command_error(ctx, error):

    send_help = (commands.MissingRequiredArgument, commands.BadArgument, commands.TooManyArguments, commands.UserInputError)

    if isinstance(error, commands.CommandNotFound):  # fails silently
        pass

    elif isinstance(error, send_help):
        _help = await send_cmd_help(ctx)
        await ctx.send(embed=_help)

    elif isinstance(error, commands.CommandOnCooldown):
        await ctx.send(f'This command is on cooldown. Please wait {error.retry_after:.2f}s')

    elif isinstance(error, commands.MissingPermissions):
        await ctx.send('You do not have the permissions to use this command.')
    
    elif isinstance(error, commands.BotMissingPermissions):
        await ctx.send('{} does not have the permission to use this command.'.format(bot.display_name))

# If any other error occurs, prints to console.
    else:
        print(''.join(traceback.format_exception(type(error), error, error.__traceback__)))

#client.run('ODU5MjY1MTQwNTk4NjM2NTQ1.YNqLBQ.5wNf22Ry4OVIXK-F8Yw7cac8Mz0')
bot.run('ODU5MjY1MTQwNTk4NjM2NTQ1.YNqLBQ.5wNf22Ry4OVIXK-F8Yw7cac8Mz0')

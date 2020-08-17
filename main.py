import os
from dotenv import load_dotenv
import discord
from discord.ext import commands

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix = '!')

# Permissions needed for the bot:
# - View Channels
# - Send Messages
# - Manage Messages
# - Embed Links
# - Read Message History

@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.playing, name='!help'))
    print(f'{bot.user} has connected to Discord!')

# Create Poll
@bot.command()
async def poll(ctx, *, input):
    # Delete called command
    await ctx.message.delete()

    # Separate title and options
    splitted = input.split('" ')
    title = splitted[0].replace('"', '')
    options = splitted[1:]
    for i in range(len(options)):
        options[i] = options[i].replace('"', '')

    # Check if there is more than 1 option
    if len(options) <= 1:
        embed = discord.Embed(
            description = ':x: There must be at least 2 options to make a poll!',
            colour = discord.Colour.red(),
        )
        await ctx.send(embed=embed)
        return
    # Check if there are less than 20 options (because of Discord limits)
    if len(options) > 20:
        embed = discord.Embed(
            description = ':x: There can\'t be more than 20 options',
            colour = discord.Colour.red(),
        )
        await ctx.send(embed=embed)
        return

    # Checks wether poll is a Yes/No Question or a Multiple Choice Question
    if len(options) == 2 and options[0].lower() == 'yes' and options[1].lower() == 'No':
        reactions = ['✅', '❌']
    else:
        # Regional Indicators
        reactions = [ '🇦', '🇧', '🇨', '🇩', '🇪', '🇫', '🇬', '🇭', '🇮', '🇯', '🇰', '🇱', '🇲', '🇳', '🇴', '🇵', '🇶', '🇷', '🇸', '🇹']

    # Create embed response
    description = []
    for x, option in enumerate(options):
        description += '{}  {}\n\n'.format(reactions[x], option)
    embed = discord.Embed(
        title=title, 
        description=''.join(description),
        colour = discord.Colour.blue()
    )
    message = await ctx.send(embed=embed)
    
    for reaction in reactions[:len(options)]:
        await message.add_reaction(reaction)


@bot.command()
async def help(ctx):
    embed = discord.Embed(
        title='Polling Bot | Help', 
        description='A simple Discord bot that allows you to easily create polls using reactions',
        colour = discord.Colour.gold()
    )
    embed.add_field(name='Usage', 
                    value='''The BOT has a unique command that allows you to generate a poll. Example usage: 
                                            !poll "Poll Title" "Option 1" "Option 2" ...
                                            This command allows a maximum of 20 options (because of Discord limitations).\n\n
                                            Alternatively, if the only options given to the BOT are "Yes" and "No", it will generate a Yes/No Poll. Example sage:
                                            !poll "Poll Title" "Yes" "No"''',
                    inline=True
                    )
    await ctx.send(embed=embed)



# Error Management
@poll.error
async def poll_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        embed = discord.Embed(
            description = ':x: You must specify a title and at least two options!',
            colour = discord.Colour.red(),
        )
        await ctx.send(embed=embed)
    if isinstance(error, commands.MissingRole):
        embed = discord.Embed(
            description = ':x: You don\'t have the permission to use this command!',
            colour = discord.Colour.red(),
        )
        await ctx.send(embed=embed)

bot.run(TOKEN)
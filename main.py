import discord
import os
from discord.ext import commands
from stay_awake import stay_awake

bot = commands.Bot(command_prefix = '$')

stay_awake()
# bot = discord.Client()

bot.add_cog(Points(bot))
bot.add_cog(HallPass(bot))

# Commands

async def on_message(message):
  # Ignore messages from bot itself
  if message.author == bot:
    return
  
  # Create a new channel (i.e. assignments, discussion groups,...)
  if message.content.startswith('$create'):
    channel_name = message.content[7:].strip()
    await message.channel.category.create_text_channel(channel_name)


# Repeat message in the Question channel
@bot.command()
async def question(ctx, *, arg):
  channel = client.get_channel(838130738729189448)
  await channel.send(arg)


# Points
class Points(commands.Cog):
  def __init__(self, bot):
      self.bot = bot
  
  @commands.command()
  async def add(self, ctx, student: discord.Member):
    """ Add 1 point to student's total points. 
    """
    if "teacher" or "mod" in [x.name.lower() for x in ctx.message.author.roles]:
      if student.id not in users:
        # confirm that student is in users
      # edit student.id's points in file	
    else:
      await message.channel.send("You don't have permission to access this command!")

  @commands.command()
  async def remove(self, ctx, student: discord.Member):
    """ Subtract 1 point from student's total points.
    """
    if "teacher" or "mod" in [x.name.lower() for x in ctx.message.author.roles]:
      # edit student.id's points in file
    else:
      await message.channel.send("You don't have permission to access this command!")

  @commands.command()
  async def mypoints(self, ctx):
    id = message.author.id
    if id in users:
      await message.channel.send("<@" + str(id) + "has {0.pts}.".format(users[id]['points'])) # tentative lmao
    else:
      await message.channel.send("You don't have any points yet! Ask your teacher to set up your profile.")
    

# Take attendance from Students
@bot.event
async def on_ready():
  channel = client.get_channel(xxx)
  text = "Attendance! React to let the teach know you are here!"
  moji = await bot.send_message(channel, text)
  await client.add_reaction(moji, emoji='✅')

@bot.event
async def on_reaction_add(reaction, user):
  channel = client.get_channel(xxx)
  if reaction.message.channel.id != channel:
    return
  if reaction.emoji == "✅":
    role = discord.utils.get(user.server.roles, name="Present")
    await client.add_roles(user, role)

# hall pass
class HallPass(commands.Cog):
  def __init__(self, bot):
      self.bot = bot

  @commands.command()
  async def away(self, ctx):
    """ Send message to alert that this user is away. This will also move the user into a muted voice channel.
    """
    student = message.author.id
    voice_channel = discord.utils.find(lambda x: x.name.lower() == 'hall channel', message.server.channels)
    await bot.move_to(student, voice_channel)
    await 
    

  @commands.command()
  async def back(self, ctx):
    """Send message to alert that this user has returned. This will also move the user back into the classroom voice channel. 
    """

bot.run(os.envrion['BOT_TOKEN'])


import discord
import os
from discord.ext import commands
from stay_awake import stay_awake

# intents = discord.Intents().all()
# client = discord.Bot(prefix='', intents=intents)
bot = commands.Bot(command_prefix = '$')

stay_awake()
# bot = discord.Client()

# Bot Setup
@bot.event
async def on_ready():
  print('We have logged in as {0.user}'.format(bot))

# Messages
async def on_message(message):
  # Ignore messages from bot itself
  if message.author == bot:
    return
  
# Create a new channel (i.e. assignments, discussion groups,...)
@bot.command()
async def create(ctx, channelName):
  guild = ctx.guild
  await guild.create_text_channel(name='{}'.format(channelName), category=int(837874749211541506))

@bot.command()
async def new(ctx, category, name):
  guild = ctx.message.guild
  if category == "assignment":
    await guild.create_text_channel(name)
  elif category == "q":

# Repeat message in the Question channel
@bot.command()
async def question(ctx, *, arg):
  channel = bot.get_channel(838130738729189448)
  await channel.send(arg)


# Points
@bot.event
async def add(self, ctx, student: discord.Member):
    """ Add 1 point to student's total points. 
    """
    if "teacher" or "mod" in [x.name.lower() for x in ctx.message.author.roles]:
      if student.id not in users:
        print("")# confirm that student is in users
        # edit student.id's points in file	
    else:
      await message.channel.send("You don't have permission to access this command!")

@bot.event
async def remove(self, ctx, student: discord.Member):
  """ Subtract 1 point from student's total points.
  """
  if "teacher" or "mod" in [x.name.lower() for x in ctx.message.author.roles]:
    print("")# edit student.id's points in file
  else:
    await message.channel.send("You don't have permission to access this command!")

@bot.event
async def mypoints(self, ctx):
  id = message.author.id
  if id in users:
    await message.channel.send("<@" + str(id) + "has {0.pts}.".format(users[id]['points'])) # tentative lmao
  else:
    await message.channel.send("You don't have any points yet! Ask your teacher to set up your profile.")
    

# Take attendance from Students
@bot.event
async def attendance():
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


HALLWAY = bot.get_channel(838153995319115796)
CLASSROOM = bot.get_channel(838130302512922676)
TEACHER_TEXT = bot.get_channel(838184342999924776)

# hall pass
@bot.command()
async def away(ctx):
  """ Move the user into the hallway voice channel."""
  student = ctx.author
  
  # if student.voice is None or student.voice.channel != CLASSROOM:
  #   return await ctx.send("<@" + str(student.id) + ">, you aren't in the classroom right now!")
  await student.move_to(HALLWAY)
  await TEACHER_TEXT.send("<@" + str(student.id) + '> is away from their computer.')

@bot.command()
async def back(ctx):
  """ Move the user back into the classroom voice channel."""
  student = ctx.author
  await student.move_to(CLASSROOM)
  await TEACHER_TEXT.send("<@" + str(student.id) + '> is back in the classroom.')


bot.run(os.environ['BOT_TOKEN'])


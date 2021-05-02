import discord
import os
import json

from discord.ext import commands
from stay_awake import stay_awake

from random import randint

# intents = discord.Intents().all()
# client = discord.Bot(prefix='', intents=intents)
bot = commands.Bot(command_prefix = '$')
permissions = discord.Permissions.all()

stay_awake()
# bot = discord.Client()

# Bot Setup
@bot.event
async def on_ready():
  print('We have logged in as {0.user}'.format(bot))

# JSON files
async def on_member_join(member):
  # attendance file
  with open('attendance.json', 'r') as attendance_file:
    users_attendance = json.load(attendance_file)

  await add_user_attendance(users_attendance, member)

  with open('attendance.json', 'w') as attendance_file:
    json.dump(users_attendance, attendance_file)

  # points file
  with open('points.json', 'r') as points_file:
    users_points = json.load(points_file)

  await add_new_user_points(users_points, member)

  with open('points.json', 'w') as points_file:
    json.dump(users_points, points_file)


# Messages
async def on_message(message):
  # Ignore messages from bot itself
  if message.author == bot:
    return
  
# Create a new channel (i.e. assignments, discussion groups,...)
@bot.command()
async def new(ctx, category, name):
  guild = ctx.message.guild
  # New Assignment
  if category == "assignment":
    await guild.create_text_channel(name=name, category=guild.get_channel(838202673047535637))
  # New Quiz
  elif category == "quiz":
    await guild.create_text_channel(name=name, category=guild.get_channel(838202818045280336))
  # New Discussion
  elif category == "discussion":
    await guild.create_text_channel(name=name, category=guild.get_channel(838203620125048874))

# Repeat message in the Question channel
@bot.command()
async def question(ctx, *, arg):
  channel = bot.get_channel(838130738729189448)
  await channel.send(arg)


# POINTS HELL YEAH

# --- variables for POINTS --- #
add_point_msgs = [", great job! You just got 1 point!", ", we're impressed. Here's 1 point!", ", you just got 1 point! :tada: :tada: :tada:"]
remove_point_msgs = []
reward_cost = 5

async def add_new_user_points(users_points, user: discord.Member):
  if not user.id in users_points:
    users_points[user.id]['current points'] = 0

async def add_point(users_points, student: discord.Member):
  users_points[student.id]['current points'] += 1


@bot.command()
async def add(ctx, student: discord.Member):
  """ Add 1 point to student's total points. """
  if ctx.message.author.server_permissions.administrator:
    add_point(student)
    return await ctx.channel.send(str(student.id) + add_point_msgs[randint(0, len(add_point_msgs - 1))])

  await ctx.channel.send("Oops! You don't have permission to access this command.")

@bot.command()
async def remove(ctx, student: discord.Member):
  """ Subtract 1 point from student's total points. """
  if ctx.message.author.server_permissions.administrator:
    print("")# edit student.id's points in file
  
  await ctx.channel.send("Oh no! You don't have permission to access this command.")

@bot.command()
async def setrewardvalue(ctx, value:int):
  """ Let an administrator set the number of points needed for a reward. Default value is 5 points. """
  if ctx.message.author.server_permissions.administrator:
    reward_cost = value
    await ctx.message.author.send("You have set the cost of a reward in server " +  + )
  pass

@bot.command()
async def mypoints(ctx):
  id = message.author.id
  if id in users:
    await message.channel.send("<@" + str(id) + "has {0.pts}.".format(users[id]['points'])) # tentative lmao
  else:
    await ctx.channel.send("You don't have any points yet! Ask your teacher to set up your profile.")
    

# Take attendance from Students
@bot.command()
async def test(ctx):

  embed_message = discord.Embed(color = discord.Color.dark_gold())
  embed_message.set_author(name="Daily Attendance")
  embed_message.add_field(name="Please react to this message with '\U0001f642' to let the teacher know you're here!", value='Click the emoji below.')

  channel = bot.get_channel(838218145600241674)
  message = await channel.send(embed=embed_message)
  await bot.add_reaction(message, emoji='\U0001f642')

@bot.event
async def on_reaction_add(reaction, user):
  if reaction.message.channel.id != '838218145600241674':
    return
  if reaction.emoji == "\U0001f642":
    role = discord.utils.get(user.server.roles, name="Present")
    await bot.add_roles(user, role)



# hall pass
@bot.command()
async def away(ctx):
  """ Move the user into the hallway voice channel."""
  student = ctx.message.author
  classroom = ctx.guild.get_channel(838229414499319858)
  hallway = ctx.guild.get_channel(838153995319115796)
  teachers_text_channel = ctx.guild.get_channel(838184342999924776)
  
  if student.voice is None or student.voice.channel != classroom:
    return await ctx.send("<@" + str(student.id) + ">, you aren't in the classroom right now!")
  
  else:
    await student.move_to(hallway)
    await teachers_text_channel.send("<@" + str(student.id) + '> is away from their computer.')
    await student.send('You are now in the hallway.')
  
  return


@bot.command()
async def back(ctx):
  """ Move the user back into the classroom voice channel."""
  student = ctx.message.author
  classroom = ctx.guild.get_channel(838229414499319858)
  hallway = ctx.guild.get_channel(838153995319115796)
  teachers_text_channel = ctx.guild.get_channel(838184342999924776)

  if student.voice is None or student.voice.channel != hallway:
    return await ctx.send("<@" + str(student.id) + ">, you must be in the hallway to use this command.")

  else:
    await student.move_to(classroom)
    await teachers_text_channel.send("<@" + str(student.id) + '> is back in the classroom.')
    await student.send('You are now back in the classroom.')
  
  return


bot.run(os.environ['BOT_TOKEN'])


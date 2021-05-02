import discord
import os
import json

from discord.ext import commands
from stay_awake import stay_awake

from random import randint

from export_file import *

# intents = discord.Intents().all()
# client = discord.Bot(prefix='', intents=intents)
bot = commands.Bot(command_prefix = '$')
permissions = discord.Permissions.all()

stay_awake()

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
  await channel.send('<@' + str(ctx.message.author.id) + '> asked: \"' + str(arg) + '\"')


# ~~~ POINTS SYSTEM ~~~ #
#  -variables-  #
add_point_msgs = [">, great job! You just got 1 point!", ">, impressive! Here's 1 point!", ">, you just got 1 point! :tada: :tada: :tada:"]
redeem_point_msgs = [">, you just redeemed a reward.", ">, enjoy your reward!", ">, OwO what's this? A reward?", ">, :eyes: you redeemed a reward!", ">, congratulations! You just redeemed an award."]
reward_cost = 0


@bot.command()
async def setupclass(ctx, value):
  if ctx.author.guild_permissions.administrator:
    for s in ctx.guild.members:
      if "Students" in s.roles:
        await setup_new_student(s)
    await setrewardvalue(ctx, ctx.author, int(value))
    await ctx.channel.send('This class is set up and ready to go!')
  return


async def setup_new_student(user):
  with open('students_points.json', 'r') as f:
    users_points = json.load(f)

  users_points = {}
  users_points[str(user.id)] = {}
  users_points[str(user.id)]["current points"] = 0
  users_points[str(user.id)]["positive"] = []
  users_points[str(user.id)]["negative"] = []

  with open('students_points.json', 'w') as f:
    json.dump(users_points, f)


@bot.command()
async def resetrewardvalue(ctx, value):
  """ Let an administrator change the reward cost. """
  await setrewardvalue(ctx, ctx.author, int(value))
  await ctx.channel.send('Rewards are now worth ' + value + ' points.')


@bot.command()
async def getrewardvalue(ctx):
  await ctx.channel.send('You can redeem a reward for ' + str(reward_cost) + ' points.')


async def setrewardvalue(ctx, author: discord.Member, value:int):
  """ Let an administrator set the number of points needed for a reward."""
  if author.guild_permissions.administrator:
    global reward_cost
    reward_cost = value
    await author.send("You have set the cost of a reward to " + str(value) + " in server " + ctx.guild.name + ".")
  return


async def add_point(student: discord.Member, reason: str):
  with open('students_points.json', 'r') as f:
    users_points = json.load(f)

  new_val = int(users_points[str(student.id)]["current points"]) + 1
  users_points[str(student.id)]['current points'] = str(new_val)

  if reason is not None:
    users_points[str(student.id)]['positive'].append(reason)
  
  with open('students_points.json', 'w') as f:
    json.dump(users_points, f)


async def remove_point(student: discord.Member, reason: str):
  with open('students_points.json', 'r') as f:
    users_points = json.load(f)
  
  if int(users_points[str(student.id)]['current points']) > 0:
    new_val = int(users_points[str(student.id)]["current points"]) - 1
    users_points[str(student.id)]['current points'] = str(new_val)

    if reason is not None:
      users_points[str(student.id)]['negative'].append(reason)
  
  with open('students_points.json', 'w') as f:
    json.dump(users_points, f)


@bot.command()
async def add(ctx, student: discord.Member, *, args = None):
  """ Add 1 point to student's total points. """
  if ctx.message.author.guild_permissions.administrator:
    if args is not None:
      args = ''.join(args[:])
    await add_point(student, args)
    return await ctx.channel.send('<@' + str(student.id) + add_point_msgs[randint(0, len(add_point_msgs)-1)])

  await ctx.channel.send("Oops! You don't have permission to access this command.")


@bot.command()
async def remove(ctx, student: discord.Member, *, args = None):
  """ Subtract 1 point from student's total points. """
  if ctx.message.author.guild_permissions.administrator:
    teachers_text_channel = ctx.guild.get_channel(838184342999924776)
    if args is not None:
      args = ''.join(args[:])
    await remove_point(student, args)
    await student.send("Uh oh. You just lost 1 point in your class, " + ctx.guild.name + ".")

    if args is not None:
      await teachers_text_channel.send("You removed 1 point from <@" + str(student.id) + ">'s total points because: " + '"' + args + '".')
    else:
      await teachers_text_channel.send("You removed 1 point from <@" + str(student.id) + ">'s total points.")

  else: 
    await ctx.channel.send("Oops! You don't have permission to access this command.")

  return


@bot.command()
async def mypoints(ctx):
  student = ctx.author
  with open('students_points.json') as f:
    users_points = json.load(f)
  ret_points = users_points[str(student.id)]["current points"]
  if str(student.id) in users_points:
    await ctx.channel.send("<@" + str(student.id) + "> has {0} points.".format(ret_points))
  else:
    await ctx.channel.send("error. sad.")
  return  


@bot.command()
async def pointsof(ctx, student: discord.Member):
  with open('students_points.json') as f:
    users_points = json.load(f)
  if ctx.message.author.guild_permissions.administrator:
    teachers_text_channel = ctx.guild.get_channel(838184342999924776)
    await teachers_text_channel.send("<@" + str(student.id) + "> has {} points.\nThey gained points for: {}\nThey lost points for: {}".format(users_points[str(student.id)]["current points"], users_points[str(student.id)]["positive"], users_points[str(student.id)]["negative"]))
  else:
    await ctx.send("You don't have permission to access this command.")
  return


@bot.command()
async def redeem(ctx, student: discord.Member):
  """ Let an admin redeem a reward for a student. """
  if ctx.message.author.guild_permissions.administrator:
    teachers_text_channel = ctx.guild.get_channel(838184342999924776)
    with open('students_points.json', 'r') as f:
      users_points = json.load(f)
  
    if int(users_points[str(student.id)]['current points']) >= reward_cost:
      new_val = int(users_points[str(student.id)]["current points"]) - reward_cost
      users_points[str(student.id)]['current points'] = str(new_val)
    
    elif int(users_points[str(student.id)]['current points']) < reward_cost:
      return await ctx.channel.send("This student doesn't have enough points to redeem a reward.")

    with open('students_points.json', 'w') as f:
      json.dump(users_points, f)
    await teachers_text_channel.send("<@" + str(student.id) + "> has redeemed a reward for {0} points. They now have {1} points.".format(reward_cost, users_points[str(student.id)]["current points"]))
    await ctx.channel.send("<@" + str(student.id) + redeem_point_msgs[randint(0, len(redeem_point_msgs)-1)] + ' You can use the $mypoints command to see your new points balance.')
  
  else:
    await ctx.send("You don't have permission to access this command.")
  return


# Take attendance from Students
@bot.command()
async def attendance(ctx):
  embed_message = discord.Embed(color = discord.Color.dark_gold())
  embed_message.set_author(name="Daily Attendance")
  embed_message.add_field(name="Please react to this message with '\U00002705' to let the teacher know you're here!", value='Click the emoji below.')

  channel = bot.get_channel(838218145600241674)
  message = await channel.send(embed=embed_message)
  await member.add_reaction(message, emoji='\U00002705')
  await member.remove_reaction(message, emoji='\U00002705')

@bot.event
async def on_raw_reaction_add(payload):
  guild_id = payload.guild_id
  guild = discord.utils.find(lambda g : g.id == guild_id, bot.guilds)
  if payload.emoji.name == '\U00002705':
    role = discord.utils.get(guild.roles, name='Present')
    if role is not None:
      member = payload.member
    if member is not None:
      await member.add_roles(role)
      print('Done')
    else:
      print('Member not found.')

@bot.event
async def on_raw_reaction_remove(payload):
  guild_id = payload.guild_id
  guild = discord.utils.find(lambda g : g.id == guild_id, bot.guilds)
  if payload.emoji.name == '\U00002705':
    role = discord.utils.get(guild.roles, name='Present')
    if role is not None:
      member = payload.member
    if member is not None:
      await member.remove_roles(role)
      print('Done')
    else:
      print('Member not found.')

@bot.command()
async def here(ctx):
  embed_message = discord.Embed(color = discord.Color.green())
  embed_message.set_author(name="Daily Attendance: Results")
  embed_message.add_field(name="Eunice", value='Present')
  embed_message.add_field(name="Abdul", value='Present')
  embed_message.add_field(name="Vanessa", value='Present')
  embed_message.add_field(name="Robert", value='Absent')
  embed_message.add_field(name="Ashley", value='Absent')
  embed_message.add_field(name="John", value='Absent')

  channel = bot.get_channel(838218145600241674)
  print('channel: ', channel)
  guild_id = 837874749211541504
  guild = discord.utils.find(lambda g : g.id == guild_id, bot.guilds)
  print('guild: ', guild)
  for member in bot.get_all_members():
    print('member: ', member)
    await channel.send(embed=embed_message)


# ~~~ HALL PASS ~~~ #
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


